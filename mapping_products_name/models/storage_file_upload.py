from odoo import models, fields, api, _

class FilesUpload(models.Model):
    _name = 'storage.file.upload'
    _discription = 'storage.file.upload'

    name = fields.Char('File Name')
    file_data = fields.Binary(string="Upload File", required=True)
    

    