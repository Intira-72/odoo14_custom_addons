from odoo import api, models, fields, _

import base64
from io import BytesIO
import pandas as pd


class OpenImportUpdateProductListWiz(models.TransientModel):
    _name = 'open.import.update.product.list.wiz'

    store_id = fields.Many2one('store.list', string='Store', required=True)
    file_data = fields.Binary(string="Upload File")
    file_name = fields.Char('File Name')


    def _create_file_binary(self):
        id_created = self.env['storage.file.upload'].create({'file_data': self.file_data,
                                                            'name': self.file_name})
        self.env.cr.commit()    

        self.env['ir.attachment'].create({
                    'name': self.file_name,
                    'type': 'binary',
                    'datas': self.file_data,
                    'res_model': id_created._name,
                    'res_id': id_created.id
                })    

        return id_created.id


    def _read_file_with_pd(self):
        file_id = self._create_file_binary()
        attachment = self.env['ir.attachment'].sudo().search([('res_model', '=', 'storage.file.upload'), ('res_id', '=', file_id)], limit=1)

        master_data = pd.read_excel(BytesIO(base64.b64decode(attachment.datas)),
                                    skiprows=[1, 2],
                                    usecols=['et_title_product_id',
                                            'et_title_product_name',
                                            'et_title_variation_id',
                                            'et_title_variation_name',
                                            'et_title_variation_price'])

        return master_data.to_dict(orient='records')


    def _check_existing_items_and_update_lists(self):
        data_read = self._read_file_with_pd()
        
        for data_item in data_read:
            data = self.env['store.products.variant'].search([('store_product_id.store_product_default_code', '=', data_item['et_title_product_id']),
                                                                ('store_product_sub_code', '=', data_item['et_title_variation_id']),
                                                                ('store_product_id.store_id', '=', self.store_id.id)])

            if data.id:
                self._update_item_name_or_variation(data_item, data.id)                
            else:
                self._add_new_item(data_item)

        return True


    def _add_new_item(self, data_item):
        product_id = self.env['store.products'].search([('store_id', '=', self.store_id.id),
                                                        ('store_product_default_code', '=', data_item['et_title_product_id'])])

        if product_id.id:
            self._add_new_item_variation(data_item, product_id.id)
        else:
            self.env['store.products'].create({'name': data_item['et_title_product_name'],
                                                'store_id': self.store_id.id,
                                                'store_product_default_code': data_item['et_title_product_id'],
                                                'price_by_store': data_item['et_title_variation_price']})
            self.env.cr.commit()

            self._add_new_item_variation(data_item, self.env['store.products'].search([('store_product_default_code', '=', data_item['et_title_product_id'])]).id)

        return True


    def _add_new_item_variation(self, data_var_item, item_id):
        self.env['store.products.variant'].create({'name': '' if pd.isna(data_var_item['et_title_variation_name']) else data_var_item['et_title_variation_name'],
                                                'store_product_id': item_id,
                                                'store_product_sub_code': data_var_item['et_title_variation_id']})
        self.env.cr.commit()

        return True


    def _update_item_name_or_variation(self, data_item, product_id):
        product_var_id = self.env['store.products.variant'].browse(product_id)

        if product_var_id.store_product_id.name != data_item['et_title_product_name']:
            product_name = self.env['store.products'].browse(product_var_id.store_product_id.id)
            product_name.write({'name': data_item['et_title_product_name'],
                                'price_by_store': float(data_item['et_title_variation_price'])})
            self.env.cr.commit()

        product_var_name = data_item['et_title_variation_name']
        
        if product_var_id.name != product_var_name:
            product_var_id.write({'name': product_var_name})
            self.env.cr.commit()

        return True


    def update_data_click(self):
        self._check_existing_items_and_update_lists()
        return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }
    

