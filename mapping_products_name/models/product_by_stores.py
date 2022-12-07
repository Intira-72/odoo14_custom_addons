from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Product(models.Model):
    _inherit = "product.product"

    product_by_store_ids = fields.One2many('map.product.to.other.stores', 'product_id')
    

    def action_open_store(self):
        domain = [('product_id', 'in', self.ids)]

        if len(self) == 1:
            self = self.with_context(
                default_product_id=self.id,
                single_product=True
            )
        else:
            self = self.with_context(product_tmpl_ids=self.product_tmpl_id.ids)
        action = self.env['map.product.to.other.stores']._get_product_by_store_action(domain)
        action["name"] = _('Product By Stores')
        return action


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # product_by_store_ids = fields.One2many('map.product.to.other.stores', 'product_tmpl_id')

    def action_open_store(self):
        return self.product_variant_ids.filtered(lambda p: p.active or p.qty_available != 0).action_open_store()    


class store_products(models.Model):
    _name = 'store.products'
    _description = 'mapping_product_name.store_product'

    store_id = fields.Many2one('store.list', string='Store', required=True)
    name = fields.Char('Name', required=True)    

    store_product_variant_ids = fields.One2many('store.products.variant', 'store_product_id', string='Variations')
    store_product_variant_id = fields.Many2one('store.products.variant', 'Product', compute='_compute_store_product_variant_id')

    company_id = fields.Many2one('res.company', string='company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    price_by_store = fields.Monetary(string='Unit Price', store=True)

    store_product_default_code = fields.Char('Internal Reference', required=True)

    def name_get(self):
        result = []            
            
        for rec in self:            
            result.append((rec.id, f'[{rec.store_product_default_code}] {rec.name}'))            
            
        return result
   
    @api.depends('store_product_variant_ids')
    def _compute_store_product_variant_id(self):
        for p in self:
            p.store_product_variant_id = p.store_product_variant_ids[:1].id


class store_products_variant(models.Model):
    _name = 'store.products.variant'
    _description = 'mapping_product_name.store_products_variant'
    _rec_name = 'store_product_id'

    name = fields.Char('Name')
    
    store_product_id = fields.Many2one('store.products', string='Product')
    store_product_sub_code = fields.Char('Reference', required=True)


class map_product_to_other_stores(models.Model):
    _name = 'map.product.to.other.stores'
    _description = 'map_product_to_other_stores'
    _sql_constraints = [('unique_mapping', 'unique(store_id, product_id, store_product_v_id)', 'Cannot Use one tracker twice!\nPlease, select a different product')]
    

    def _domain_store_product_id(self):
        active_ids = self.env.context.get('active_ids') 
        if active_ids:
            domain = [('product_tmpl_id', 'in', active_ids)]
        else:
            domain = None

        return domain

    def get_product_id(self):
        products = self.env['product.product'].search([('product_tmpl_id', '=', self.env.context.get('active_id'))])
        return products.id if len(products) == 1 else None

    @api.model
    def _get_product_by_store_action(self, domain=None):

        ctx = dict(self.env.context or {})
        action = {
            'name': _('Product By Store'),
            'res_model': 'map.product.to.other.stores',
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_mode': 'list,form',          
            'context': ctx,
            'domain': domain or [],
        }

        action['view_id'] = self.env.ref('mapping_products_name.product_by_store_view_tree').id
        form_view = self.env.ref('mapping_products_name.product_by_store_view_tree').id

        action.update({
            'views': [
                (action['view_id'], 'list'),
                (form_view, 'form'),
            ],
        })

        return action

    product_id = fields.Many2one('product.product', 'Product', domain=lambda self: self._domain_store_product_id(), default=get_product_id, required=True)
    store_id = fields.Many2one('store.list', string='Store', required=True)    
    store_product_v_id = fields.Many2one('store.products.variant', string='Product By Store', required=True)  

    @api.onchange("store_id")
    def _onchange_store(self):
        store = 0
        if self.store_id:
            store = self.store_id.id
            self.store_product_v_id = False
        return {'domain': {'store_product_v_id': [('store_product_id.store_id','=', store)]}}

    @api.model
    def create(self, vals):
        check_dup = self.env['map.product.to.other.stores'].search([('product_id', '=', vals['product_id']),
                                                                    ('store_id', '=', vals['store_id']),
                                                                    ('store_product_v_id', '=', vals['store_product_v_id'])])

        try:
            if check_dup.id:
                raise ValueError("The item already exists, please check.")
            else:
                return super(map_product_to_other_stores, self).create(vals)
        except ValueError as err:
            raise UserError(_(err)) 


class StoreListInherited(models.Model):
    _inherit = 'store.list'

    def name_get(self):
        result = []            
            
        for rec in self:            
            result.append((rec.id, f'[{rec.store_group_id.name}] {rec.name}')) 
            
        return result

class StoreProductListInherited(models.Model):
    _inherit = 'store.products.variant'

    def name_get(self):
        result = []            
            
        for rec in self:  
            if rec.name == "":
                result.append((rec.id,f'[{rec.store_product_id.store_product_default_code}] {rec.store_product_id.name}'))
            else:
                result.append((rec.id, f'[{rec.store_product_id.store_product_default_code}] {rec.store_product_id.name} ({rec.name})'))            
            
        return result
