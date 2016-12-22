# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import logging

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
from odoo.addons.website_portal.controllers.main import website_account

_logger = logging.getLogger(__name__)


class PilotController(website_account):

    @http.route(['/my/servers/', '/my/quotes/page/<int:page>'], type='http',
                auth="user", website=True)
    def my_servers(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        ServerEnv = request.env['pilot.server'].sudo()

        domain = [
            ('partner_id', '=', partner.commercial_partner_id.id),
        ]
        archive_groups = self._get_archive_groups('pilot.server', domain)

        # count for pager
        server_count = ServerEnv.search_count(domain)
        # make pager
        pager = request.website.pager(
            url="/my/servers",
            total=server_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        servers = ServerEnv.search(domain, limit=self._items_per_page,
                                   offset=pager['offset'])
        values.update({
            'servers': servers,
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/servers',
        })
        return request.render("odoo_pilot.portal_my_server", values)

    @http.route(['/my/server/<int:server>'], type='http',
                auth="user", website=True)
    def view_server(self, server=None, **kw):
        server = request.env['pilot.server'].browse([server])
        try:
            server.check_access_rights('read')
            server.check_access_rule('read')
        except AccessError:
            return request.render("website.403")

        return request.render("odoo_pilot.portal_server_view", {
            'server': server, 'error': {},
        })

    @http.route(['/my/servers/new'], type='http',
                auth="user", website=True, methods=['GET', 'POST'])
    def crete_server(self, **kw):

        # POST
        if "ip_address" in kw:
            partner = request.env.user.partner_id
            server = request.env['pilot.server'].sudo().create({
                'partner_id': partner.id,
                'name': kw["ip_address"],
                'root_password': kw["root_password"],
            })
            return request.redirect("/my/server/%d" % server.id)
        return request.render("odoo_pilot.portal_server_edit", {'error': {}})
