from odoo import models, fields, api
from odoo import http

class Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    '''
    Add tags field to settings
    '''
    tags = fields.Many2many('product.tag', string='Many2many Tags')

    '''
    Get saved tags from ir.config_parameter
    '''
    @api.model
    def get_values(self):
        tags = super(Settings, self).get_values()
        tag_ids = self.env['ir.config_parameter'].sudo().get_param('po_settings.tags')
        if tag_ids:
            tag_ids = tag_ids.replace("[", "").replace("]", "").split(",")  # Remove brackets
            tag_ids = [int(tag_id) for tag_id in tag_ids]
            tags.update(tags=[(6, 0, tag_ids)])
        return tags

    '''
    Save data to ir.config_parameter
    '''
    def set_values(self):
        super(Settings, self).set_values()
        tag_ids = self.tags.ids
        self.env['ir.config_parameter'].sudo().set_param('po_settings.tags', tag_ids)



