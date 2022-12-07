# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WrongUploadSaleOrderList(models.Model):
    _name = 'wrong.upload.so.list'
    _description = 'mapping_product_name.wrong_upload_so_list'

    name = fields.Char("Reference")
    order_id = fields.Integer("Order ID")
    store_id = fields.Many2one("store.list", string="Store")
    product_name = fields.Char("Product")
    product_variant = fields.Char("Variantion")    
    order_qty = fields.Integer("Qty")

    company_id = fields.Many2one('res.company', string='company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    unit_price = fields.Monetary(string='Unit Price', store=True)

    state = fields.Selection(string='Status', copy=False, selection=[('product_error', 'Product Not Found'),
                                                                    ('product_v_error', 'Variantion Not Found'),
                                                                    ('mapping_error', 'Not Matched')])

    def reimport_sale_order(self):
        active_ids = self.env.context.get('active_ids')        
        order_ids = self.env['wrong.upload.so.list'].browse(active_ids)

        for ids in order_ids:
            product_check = self._product_check(ids.store_id.id, ids.product_name, ids.product_variant)

            if product_check:
                self.env['sale.order.line'].create({'order_id': ids.order_id,                                                
                                                'product_id': product_check.id,
                                                'product_uom_qty': ids.order_qty,
                                                'price_unit': ids.unit_price})
                self.env.cr.commit()

                ids.unlink()
            else:
                pass
        

    def _product_check(self, store_id, product_name, variantion):
        product = self.env['store.products'].search([('name', '=', product_name), ('store_id', '=', store_id)])

        if product:
            product_var = self.env['store.products.variant'].search([('name', '=', variantion), ('store_product_id', '=', product[-1].id)])
            if product_var:
                product_by_store = self.env['map.product.to.other.stores'].search([('store_product_v_id', '=', product_var.id), ('store_id', '=', store_id)]).product_id
                if product_by_store:
                    return product_by_store
                else:
                    return False
            else:
                return False
        else:
            return False

