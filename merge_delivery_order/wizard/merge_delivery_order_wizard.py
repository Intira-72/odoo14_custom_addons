from odoo import api, models, fields


class StockMergeDeliveryOrderWizard(models.TransientModel):
    _name = 'stock.merge.delivery.order.wizard'

    @api.model
    def default_get(self, fields):
        res = super(StockMergeDeliveryOrderWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids')

        orders = self.env['stock.picking'].browse(active_ids)

        res['order_line_ids'] = orders.move_line_ids_without_package

        return res  


    order_line_ids = fields.Many2many('stock.move.line', string='Order Line')


    def action_report_merge_order(self):
        product_requisition = []        

        for product in self.order_line_ids:
            order_id = self.env['stock.picking'].browse(product.picking_id.id).group_id.sale_id

            order_dict = {'product_id': product.product_id.id,
                            'name': product.product_id.display_name,
                            'product_qty': product.product_uom_qty,
                            'location': product.location_id.complete_name.strip("WH/Stock/"),
                            'unit': product.product_uom_id.name,
                            'order_detail': [{'order_no': order_id.name,
                                            'order_ref': order_id.client_order_ref,
                                            'order_qty': product.product_uom_qty,
                                            'unit': product.product_uom_id.name}]}

            if product_requisition:
                if order_dict['product_id'] in [o['product_id'] for o in product_requisition]:
                    for order in product_requisition:
                        if order_dict['product_id'] == order['product_id']:
                            order['product_qty'] += order_dict['product_qty']
                            order['order_detail'] += order_dict['order_detail']
                else:
                    product_requisition.append(order_dict)
            else:
                product_requisition.append(order_dict)

        data = {'product_requisition': product_requisition}
        
        report_action = self.env.ref('merge_delivery_order.delivery_order_merge_action').report_action(self, data=data)       
        report_action['close_on_report_download'] = True

        return report_action
