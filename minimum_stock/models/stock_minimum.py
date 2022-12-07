from email.policy import default
from odoo import api, fields, models, _


class BelowStock(models.Model):
    _name = "below.stock"

    name = fields.Char("Name", default="MS")
    product_id = fields.Many2one('product.product', 'Product')
    qty_availabel = fields.Float('Quantity On Hand', compute='_compute_quantities_inherit')
    virtual_available = fields.Float('Forecast Quantity', compute='_compute_quantities_inherit')
    required_amount = fields.Float("Required Amount")
    product_min_qty = fields.Float("Minimum", compute='_compute_quantities_inherit')
    order_ids = fields.One2many('purchase.order.line', 'be_stock')

    @api.depends('product_id', 'product_min_qty')
    def _compute_quantities_inherit(self):   
        for line in self:     
            product = self.env['product.product'].browse(line.product_id.id)
            minimum = self.env['stock.warehouse.orderpoint'].search([('product_id', '=', product.id)])
            orders = self.env['purchase.order.line'].search([('product_id', '=', product.id), ('order_id.state', 'in', ['draft', 'purchase'])])

            line.qty_availabel = product.qty_available
            line.virtual_available = product.virtual_available
            line.product_min_qty = minimum.product_min_qty
            line.order_ids = orders  

            sum_order = self._calculate_stock(orders)   
            line.required_amount = 0 if minimum.product_min_qty - (sum_order + product.qty_available) < 0 else minimum.product_min_qty - (sum_order + product.qty_available)


    def _calculate_stock(self, orders):
        sum_order = 0
        for order in orders:
            sum_order += order.product_qty

        return sum_order


    def minimum_check_list(self):
        var_min = self.env['stock.warehouse.orderpoint'].search([('product_min_qty', '!=', 0)])
        
        for min_rule in var_min:
            product = self.env['product.product'].browse(min_rule.product_id).id
            orders = self.env['purchase.order.line'].search([('product_id', '=', product.id), ('order_id.state', 'in', ['draft', 'purchase'])])

            sum_order = self._calculate_stock(orders)
            stock_min_ls = self.env['below.stock'].search([('product_id', '=', product.id)])

            if stock_min_ls:
                if stock_min_ls.required_amount == 0:
                    stock_min_ls.unlink()
            else:
                if min_rule.product_min_qty > (sum_order + product.qty_available):
                    super(models.Model, self).create({'product_id': product.id})


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    be_stock = fields.Many2one('below.stock', 'Below Stock')