from odoo import api, fields, models, _
from odoo.exceptions import UserError

class MultipleInvoiceCreate(models.TransientModel):
    _name = "multiple.invoice.create"
    _description = "Create Invoice By SO"

    def create_invoice_by_order(self):
        for record in self._context.get('active_ids'):            
            sale_order = self.env[self._context.get('active_model')].browse(record)
            order_line = self.env['sale.order.line'].search([('order_id', '=', record)])
            if sale_order.invoice_status == 'to invoice':
                context = {
                    'partner_id': sale_order.partner_invoice_id,
                    'partner_shipping_id': sale_order.partner_shipping_id,
                    'invoice_payment_term_id': sale_order.payment_term_id,
                    'move_type': 'out_invoice',
                    'invoice_origin': sale_order.name,
                    'ref': sale_order.client_order_ref,
                    'invoice_line_ids': [(0, 0,
                        {'product_id': i.product_id,
                         'quantity': i.qty_to_invoice,
                         'product_uom_id': i.product_uom,
                         'price_unit': i.price_unit,
                         'tax_ids': i.tax_id,
                         }) for i in order_line
                    ]
                }

                self.env['account.move'].create(context)
            sale_order.write({'invoice_status': 'invoiced'})
            
        return True
            