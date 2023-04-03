from odoo import _, api, fields, models


class ProductReplenish(models.TransientModel):
    _inherit = 'product.replenish'
    _description = 'Product Replenish'

    @api.model
    def _prepare_run_values(self):
        result = super(ProductReplenish, self)._prepare_run_values()

        user_id = self.env.user
        
        replenishment = self.env['procurement.group'].create({
            'partner_id': user_id.partner_id.id
        })

        result['group_id'] = replenishment        
        return result
    
    @api.model
    def default_get(self, fields):
        res = super(ProductReplenish, self).default_get(fields)
        warehouse_id = self.env.user.property_warehouse_id.id
        
        if 'warehouse_id' in fields:
            if warehouse_id:
                res['warehouse_id'] = self.env.user.property_warehouse_id.id
                # res['route_ids'] = self.env.user.property_warehouse_id.name
        return res