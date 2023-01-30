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

    short_name = fields.Char("Short Name")
    brand = fields.Char("Brand")
    series = fields.Char("Model")
    m_product_id = fields.Many2one('om_makro_order_import_xml.makro_products')
    product_id = fields.Many2one('product.product', readonly=True, required=True)


    