from odoo import models, fields, api


class MakroStoreLocation(models.Model):
    _name = 'om_makro_order_import_xml.makro_store_loc'
    _description = 'om_makro_order_import_xml.makro_store_loc'

    _sql_constraints = [
        ('name', 'unique (name)', 'The location number already Exists!'),
    ]

    name = fields.Char("Location Code", required=True)
    contact_id = fields.Many2one('res.partner', string="Contact", required=True)
    zone_id = fields.Many2one('makro.location_zone', string="Zone", required=True)


    def name_get(self):
        result = []            
            
        for rec in self:
            result.append((rec.id, '%s' % (rec.contact_id.display_name)))           
        return result


class MakroStoreLocatoinZone(models.Model):
    _name = 'makro.location_zone'
    _description = 'makro.location_zone'

    name = fields.Char("Zone", required=True)
