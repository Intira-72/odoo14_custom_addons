from odoo import models, fields, api


class MakroProducts(models.Model):
    _name = 'om_makro_order_import_xml.makro_products'
    _description = 'om_makro_order_import_xml.makro_products'

    makro_code = fields.Char("Code", required=True)
    name = fields.Char("Product", required=True)
    product_ids = fields.One2many('om_makro_order_import_xml.makro_products_maching_line', 'm_product_id', string="Products")    

    def name_get(self):
        result = []            
            
        for rec in self:
            result.append((rec.id, '[%s] %s' % (rec.makro_code, rec.name)))
        return result


class MatchingProducts(models.Model):
    _name = 'om_makro_order_import_xml.makro_products_maching_line'
    _description = 'om_makro_order_import_xml.makro_products_maching_line'

    m_product_id = fields.Many2one('om_makro_order_import_xml.makro_products')
    product_id = fields.Many2one('product.product', required=True)
    categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    default_code = fields.Char('product.template', related='product_id.default_code')
    categ_name = fields.Char('Category',compute='_compute_categ_name',)


    @api.depends('product_id')
    def _compute_categ_name(self):
        for record in self:
            record.categ_name = record.categ_id.name


class ProductBrand(models.Model):
    _name = "product.template.brand"

    name = fields.Char("name")
    product_tmpl_id = fields.One2many("product.template", 'brand_id')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one("product.template.brand")


    