# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class Dashboard(models.Model):
    _name = 'dashboard'

    @api.one
    def _kanban_dashboard_graph(self):
        import plotly.graph_objs as go
        from plotly import tools
        from plotly.graph_objs import Scatter
        from plotly.offline.offline import _plot_html

        import pandas as pd
        import pandas.io.sql as psql

        self.env.cr.execute("select sum(amount_total) as total, rp.name from \
                         account_invoice ac inner join res_partner rp on \
                         ac.partner_id = rp.id group by rp.name \
                         order by total desc")
        todos = self.env.cr.fetchall()

        df = pd.DataFrame(todos, columns=['total', 'name'])
        df["total"] = df["total"].astype(float)
        primeiros = df.iloc[:12]
        outros = df.iloc[12:]
        total = outros['total'].sum()

        df2 = pd.DataFrame([[total, 'Outros']], columns=['total', 'name'])
        primeiros = primeiros.append(df2)

        pie = go.Pie(labels=primeiros['name'], values=primeiros['total'])

        prod_df = df
        import numpy as np
        total = prod_df['total'].sum()

        a = prod_df['total'] / total
        prod_df['percentual'] = a
        prod_df['cum_percentual'] = prod_df['percentual'].cumsum(0)
        prod_df['ScoreA'] = prod_df['cum_percentual'] < 0.8
        prod_df['A'] = np.where(prod_df['ScoreA'], 'A', None)
        prod_df['ScoreB'] = prod_df['cum_percentual'].between(0.8, 0.95)
        prod_df['B'] = np.where(prod_df['ScoreB'], 'A', None)
        prod_df['ScoreC'] = prod_df['cum_percentual'] > 0.95
        prod_df['C'] = np.where(prod_df['ScoreC'], 'C', None)

        total = float(prod_df['name'].count())
        prod_df['percent'] = (prod_df.index.values / total)

        prod_df['label_x'] = prod_df[['name', 'total', 'percentual']].apply(
            lambda x: u'{} - R$ {} - {:,.2%}'.format(x[0], x[1], x[2]), axis=1)

        # Curva ABC de clientes
        a_df = prod_df[prod_df['ScoreA'] == True]
        trace1 = go.Scatter(
            x=a_df['percent'],
            y=a_df['cum_percentual'],
            text=a_df['label_x'],
            mode='lines+markers',
            name='Clientes A',
        )
        b_df = prod_df[prod_df['ScoreB']]
        trace2 = go.Scatter(
            x=b_df['percent'],
            y=b_df['cum_percentual'],
            text=b_df['label_x'],
            mode='lines+markers',
            name='Clientes B',
        )
        c_df = prod_df[prod_df['ScoreC']]
        trace3 = go.Scatter(
            x=c_df['percent'],
            y=c_df['cum_percentual'],
            text=c_df['label_x'],
            mode='lines+markers',
            name='Clientes C',
        )

        layout = go.Layout(
            showlegend=True,
            title="Curva ABC de Clientes",
            yaxis={'tickformat': '%', 'ticksuffix': ' de vendas',
                   'showticksuffix': 'first'},
            xaxis={'tickformat': '%'}
        )

        fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)

        plot_html, plotdivid, width, height = _plot_html(
            fig, False, "", True, '100%', 525, False)

        self.dashboard_graph = plot_html

    identifier = fields.Char(string="Identificador", size=60)
    name = fields.Char(string="Descrição")
    code = fields.Text(string="Código")

    dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
