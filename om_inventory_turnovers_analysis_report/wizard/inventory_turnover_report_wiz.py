from odoo import api, fields, models, _
import datetime
import calendar


class InventoryTurnoverReportWizard(models.TransientModel):
    _name = 'inventory.turnover.report'
    _description = "Inventory Turnover Report Wizard"

    start_date = fields.Datetime(string="Opening Date", default=lambda self: datetime.datetime.combine(datetime.date.today().replace(day=1), datetime.time.min) - datetime.timedelta(hours=7))
    end_date = fields.Datetime(string="Closing Date", default=lambda self: datetime.datetime.combine(datetime.date.today().replace(day=calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1]), datetime.time.max) - datetime.timedelta(hours=7))
    product_ids = fields.Many2many('product.product', string="Products")
    category_ids = fields.Many2many('product.category', string="Categories", default=lambda self: self.env['product.category'].search([], limit=1))
    warehouse_ids = fields.Many2one('stock.warehouse', string="Warehouse")
    location_ids = fields.One2many('stock.location')
    company_ids = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)


    def _at_open_date(self, product_id):
        product_in = 0
        product_out = 0

        opening_stock = self.env['stock.move'].search([('product_id', '=', product_id), '|',
                                                        ('location_id', 'child_of', self.warehouse_ids.view_location_id.id),
                                                        ('location_dest_id', 'child_of', self.warehouse_ids.view_location_id.id),
                                                        ('date', '<=', self.start_date),
                                                        ('state', '=', 'done')])
        
        

        return product_in - product_out
        

    def btn_inventory_turnover_export_pdf(self):
        context = []
        for i in self.product_ids:
            context.append({
                'product_name': i.name,
                'opening_stock': self._at_open_date(i.id)
            })
            
        print(context)
        return
    
    def btn_inventory_turnover_export_xlsx(self):
        return