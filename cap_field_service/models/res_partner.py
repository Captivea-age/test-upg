# -- coding: utf-8 --
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    zone = fields.Many2one('team.color', string="Zone", compute='_compute_zone',store=True)
    job_task_history_ids = fields.Boolean(string='z - do not use', stored=False)

    @api.depends('zip')
    def _compute_zone(self):
        for record in self:
            zone = False
            out_of_sa = self.env['team.color'].search([('name','=','Out of SA')], limit = 1)

            if out_of_sa:
                if record.zip and record.partner_type == "location":
                    zip_search = self.env['zip.list'].search([('zip','=',str(record.zip))], limit=1)
                    if not zip_search:
                        zone = out_of_sa
                    else:
                        zone = self.env['team.color'].search([('name','=',zip_search.team.name)], limit=1)

                    if zone == out_of_sa and not record.out_of_sa:
                        #Create Out of SA Alert
                        self.env['internal.alert'].create({
                            'partner_id': record.id,
                            'alert_level': 'error',
                            'alert_text': 'Out of SA',
                        })
                        record['out_of_sa'] = True
#                         env.cr.commit()

            record['zone'] = zone