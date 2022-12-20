from odoo import models, fields, api


class MakroBuyerData(models.Model):
    _name = 'om_makro_order_import_xml.makro_buyer'
    _description = 'om_makro_order_import_xml.makro_buyer'


    name = fields.Char("Buyer Code", required=True)
    company_id = fields.Many2one('res.company', string="Company", required=True)


    def name_get(self):
        result = []            
            
        for rec in self:
            result.append((rec.id, '[%s] %s' % (rec.name, rec.company_id.name)))           
        return result