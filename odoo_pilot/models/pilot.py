# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import jinja2
from tempfile import NamedTemporaryFile

#from ansible.playbook import PlayBook
#from ansible.inventory import Inventory
#from ansible import callbacks
#from ansible import utils

from odoo import api, fields, models


class PilotDomain(models.Model):
    _name = 'pilot.domain'

    name = fields.Char('Domínio', size=120)
    instance_id = fields.Many2one('pilot.instance', "Instância")


class PilotInstance(models.Model):
    _name = 'pilot.instance'

    name = fields.Char(string="Nome", size=50)
    port_to_run = fields.Integer(string="Porta", default=8069)
    server_id = fields.Many2one('pilot.server', string="Servidor")
    domain_ids = fields.One2many('pilot.domain', 'instance_id',
                                 string="Domínios")


class PilotServer(models.Model):
    _name = 'pilot.server'

    name = fields.Char(string="Endereço IP", size=80)
    root_password = fields.Char(string="Senha Root", size=20)
    partner_id = fields.Many2one('res.partner', string="Parceiro")
    instance_ids = fields.One2many('pilot.instance', 'server_id',
                                   string="Instâncias")

    @api.multi
    def action_install_odoo(self):
        # Boilerplace callbacks for stdout/stderr and log output
        utils.VERBOSITY = 0
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        stats = callbacks.AggregateStats()
        runner_cb = callbacks.PlaybookRunnerCallbacks(
            stats, verbose=utils.VERBOSITY)

        # Dynamic Inventory
        # We fake a inventory file and let Ansible load if it's a real file.
        # Just don't tell Ansible that, so we don't hurt its feelings.
        inventory = """
        [customer]
        {{ public_ip_address }}

        [customer:vars]
        domain={{ domain_name }}
        customer_id={{ customer_id }}
        customer_name={{ customer_name }}
        customer_email={{ customer_email }}
        """
        inventory_template = jinja2.Template(inventory)
        rendered_inventory = inventory_template.render({
            'public_ip_address': '111.222.333.444',
            'domain_name': 'some.domainname.com'
            # and the rest of our variables
        })
        # Create a temporary file and write the template string to it
        hosts = NamedTemporaryFile(delete=False)
        hosts.write(rendered_inventory)
        hosts.close()

        pb = PlayBook(
            playbook='run-odoo.yml',
            host_list=hosts.name,     # Our hosts, the rendered inventory file
            remote_user='some_user',
            callbacks=playbook_cb,
            runner_callbacks=runner_cb,
            stats=stats,
            private_key_file='/path/to/key.pem'
        )
        results = pb.run()

        # Ensure on_stats callback is called
        # for callback modules
        playbook_cb.on_stats(pb.stats)
        os.remove(hosts.name)
        print results
