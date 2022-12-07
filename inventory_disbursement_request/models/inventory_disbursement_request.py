# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InventoryDisbursementRequest(models.Model):
    _name = 'inventory.disbursement.request'
    _description = 'inventory.disbursement.request'

    name = fields.Char("Requestion No.", compute='_compute_get_name')
    product_id = fields.Many2one('product.product', string="Product")
    stock_location_ids = fields.Many2many('stock.quant', string="Stock Location")
    picking_ids = fields.Many2many('stock.move.line', string="Picking")
    print_count = fields.Integer("Print Totle", default=0)


    def _compute_get_name(self):
        for rec in self:
            id_to_char = str(rec.id)
            rec.name = "RQ" + id_to_char if len(id_to_char) == 5 else "RQ" + ("0" * (5 - len(id_to_char))) + id_to_char


    def create(self):
        active_ids = self._context.get('active_ids')
        move_line_ids = self.env['stock.move.line'].search([('picking_id', 'in', active_ids)])

        is_req = 1 in [req.is_requisition for req in move_line_ids]
        
        product_ids = [move_line.product_id for move_line in move_line_ids]
        product_ids = list(dict.fromkeys(product_ids))

        try:
            if is_req == False:
                for product_id in product_ids:
                    rtn = super(InventoryDisbursementRequest, self)

                    location_ids = [loc_id.id for loc_id in self.env['stock.quant'].search([('product_id', '=', product_id.id), ('on_hand', '=', True)])]

                    move_ids = [move_line.id for move_line in move_line_ids if move_line.product_id.id == product_id.id]
                    
                    rtn.create({'product_id': product_id.id,
                                'picking_ids': [(6, 0, move_ids)],
                                'stock_location_ids': [(6, 0, location_ids)]})

                for move_id in move_line_ids:
                    move_id.is_requisition = 1
                    
            else:
                picking_list = [p.picking_id.name for p in move_line_ids if p.is_requisition == 1]
                raise ValueError('\n'.join(picking_list))

        except ValueError as err:
            raise UserError(_(f"This delivery items:\n\n{err}\n\nhas already been processed.  Please check the selected item again."))

        tree_view = {
            'name': _('Disbursement Requestions'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'inventory.disbursement.request',
            'type': 'ir.actions.act_window',
            'target': 'main',}

        return tree_view


    def req_export_pdf(self):
        total = sum([v.product_uom_qty for v in self.picking_ids])
        loc = list(dict.fromkeys([v.location_id.name for v in self.picking_ids]))
        order_lists = []

        for order in self.picking_ids:
            order_lists.append({'order_no': f"[{order.picking_id.origin}] {order.picking_id.name}",
                                'customer_ref': order.picking_id.custom_ref,
                                'order_qty': f"{order.product_uom_qty} {order.product_uom_id.name}",
                                "partner": order.picking_id.partner_id.display_name})

        data = {'name': self.name,
                'product': self.product_id.display_name,
                'total_qty': total,
                'location': ', '.join(loc),
                'order_lists': order_lists,
                'u_id': self.env.user.name}
        
        report_action = self.env.ref('inventory_disbursement_request.requisition_report_action').report_action(self, data=data)    
        self.print_count += 1   
        return report_action


    def unlink(self):
        for req in self:
            for r in req.picking_ids:
                r.is_requisition = 0

        return super(InventoryDisbursementRequest, self).unlink()


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    is_requisition = fields.Boolean(default=0)