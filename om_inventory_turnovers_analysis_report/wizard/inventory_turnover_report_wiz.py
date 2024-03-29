from odoo import api, fields, models, _
from odoo.exceptions import UserError

import datetime
import calendar


class InventoryTurnoverReportWizard(models.TransientModel):
    _name = 'inventory.turnover.report'
    _description = "Inventory Turnover Report Wizard"

    start_date = fields.Datetime(string="Opening Date",
                                 default=lambda self: datetime.datetime.combine(datetime.date.today().replace(day=1, month=1), datetime.time.min) - datetime.timedelta(hours=7))
    end_date = fields.Datetime(string="Closing Date",
                               default=lambda self: datetime.datetime.combine(datetime.date.today().replace(day=31, month=12), datetime.time.max) - datetime.timedelta(hours=7))
    product_ids = fields.Many2many('product.product', string="Products", domain_filter=[('categ_id', 'child_of', lambda self: self.category_ids._ids)])
    category_ids = fields.Many2many('product.category', string="Categories",
                                    default=lambda self: self.env['product.category'].search([], limit=1),
                                    required=True)
    company_ids = fields.Many2one('res.company', string="Company",
                                  default=lambda self: self.env.user.company_id,
                                  required=True)
    warehouse_ids = fields.Many2one('stock.warehouse', string="Warehouse",
                                    required=True)
   
    @api.onchange('start_date')
    def _onchange_start_date_(self):
            self.end_date = self.end_date.replace(year=self.start_date.year + 1)
    

    def _get_stock_start_and_end(self, product_id):        
        locations = self.env["stock.location"].search(
            [("id", "child_of", [self.warehouse_ids.view_location_id.id])]
        )        

        self._cr.execute(
            """
                SELECT move.date, move.product_id, move.product_qty,
                    move.product_uom_qty, move.product_uom, move.reference,
                    move.location_id, move.location_dest_id,
                    case when move.location_dest_id in %s
                        then move.product_qty end as product_in,
                    case when move.location_id in %s
                        then move.product_qty end as product_out,
                    case when move.date < %s then True else False end as is_initial,
                    move.picking_id
                FROM stock_move move
                WHERE (move.location_id in %s or move.location_dest_id in %s)
                    and move.state = 'done' and move.product_id in %s
                    and CAST(move.date AS date) <= %s
                ORDER BY move.date, move.reference
            """,
            (
                tuple(locations.ids),
                tuple(locations.ids),
                self.start_date,
                tuple(locations.ids),
                tuple(locations.ids),
                tuple(product_id),
                self.end_date,
            ),
        )

        stock_card_results = self._cr.dictfetchall()
        initial = 0
        balance = 0
        for stock in stock_card_results:
            if stock['is_initial']:
                initial += ((stock['product_in'] if stock['product_in'] else 0) - (stock['product_out'] if stock['product_out'] else 0))
            else:
                balance += ((stock['product_in'] if stock['product_in'] else 0) - (stock['product_out'] if stock['product_out'] else 0))

        return {'initial': initial, 'balance': balance + initial}
        

    def _get_receipts_deliveries_order(self, product_id):
        outgoing = 0
        incoming = 0

        pickings = self.env['stock.move.line'].search([('product_id', '=', product_id),
                                                      ('picking_id.picking_type_id.code', 'in', ['incoming', 'outgoing']),
                                                      ('date', '>=', self.start_date),
                                                      ('date', '<=', self.end_date),
                                                      ('state', '=', 'done')])
        
        for picking in pickings:
            if picking.picking_id.picking_type_id.code == 'incoming':
                incoming += picking.qty_done
            elif picking.picking_id.picking_type_id.code == 'outgoing':
                outgoing += picking.qty_done
            else:
                pass

        return {'sale': outgoing, 'purchase': incoming}
    

    def _cal_cost_of_sales(self, initial, incoming, balance):
        return (initial + incoming) - balance
    
    def _inventory_turnover_ratio(self, cos, stock_avg):
        try:
            return cos / stock_avg
        except ZeroDivisionError:
            return 0
    
    def _avg_inventory_period(self, inv_turnover):        
        try:
            return 365 / inv_turnover
        except ZeroDivisionError:
            return 0 
    
        # delta_days = self._get_distance_between_days()
        # try:
        #     cal_period = delta_days / inv_turnover
        #     if cal_period < 0:
        #         return 0
        #     else:
        #         return delta_days / inv_turnover
        # except ZeroDivisionError:
        #     return 0       
    
    def _get_distance_between_days(self):
        delta = self.end_date - self.start_date
        if delta.days < 0:
            raise UserError('Please check the start and end date values for accuracy.')
        else:
            return delta.days
        
    
    def _get_dataset(self, product_ids):
        context = []

        for rec in product_ids:
            stock = self._get_stock_start_and_end([rec.id])
            picking_list = self._get_receipts_deliveries_order(rec.id)

            try:
                stock_avg = (stock['initial'] + stock['balance']) / 2
            except ZeroDivisionError:
                stock_avg = 0
                
            cost_of_sales = self._cal_cost_of_sales(stock['initial'], picking_list['purchase'], stock['balance'])
            inv_turnover = self._inventory_turnover_ratio(cost_of_sales, stock_avg)
            avg_inventory_period = self._avg_inventory_period(inv_turnover)            

            context.append({'product_id': f"{rec.display_name}",
                            'initial': f"{stock['initial']:,.0f}",
                            'balance': f"{stock['balance']:,.0f}",
                            'stock_avg': f"{stock_avg:,.2f}",
                            'sale': f"{picking_list['sale']:,.0f}",
                            'purchase': f"{picking_list['purchase']:,.0f}",
                            'inv_turnover': "-" if inv_turnover < 0 else f"{inv_turnover:,.2f}",
                            'avg_inventory_period': "-" if inv_turnover < 0 else f"{avg_inventory_period:,.0f}"                            
                            })
            
        return context
    

    def btn_inventory_turnover_export_pdf(self):
        if self.product_ids:
            report_dataset = self._get_dataset(self.product_ids)
        else:
            product_ids = self.env['product.product'].search([('categ_id', 'child_of', self.category_ids._ids)])
            report_dataset = self._get_dataset(product_ids)

        data = {
            'from_date': self.start_date.date(),
            'to_date': self.end_date.date(),
            'category': " / ".join([ca.name for ca in self.category_ids]),
            'warehouse': self.warehouse_ids.name,
            'turnover_lists': sorted(report_dataset, key=lambda r: float(0 if r['inv_turnover'] == "-" else r['inv_turnover'].replace(',', '')), reverse=True)
        }

        report_action = self.env.ref('om_inventory_turnovers_analysis_report.action_inventory_turnover_pdf').report_action(None, data=data)
        report_action['close_on_report_download'] = True

        return report_action
    
    def btn_inventory_turnover_export_xlsx(self):

        return