from odoo import models, fields

class ArrivalWindow(models.Model):
    _name="arrival.window"
    _description = 'Arrival Window'

    name = fields.Char(string="Arrival window label")
    start_time = fields.Many2one('time.selection',string="Start hour")
    end_time = fields.Many2one('time.selection',string="End hour")
    time_to_add = fields.Float(string="(Technical)Time to add")
    department = fields.Many2one('cap.department',string="Department")


class TimeSelection(models.Model):
    _name = 'time.selection'
    _description = 'Time selector for Field Service scheduling'

    name = fields.Char(string='Name')
    minutes = fields.Integer(string="Minutes since 00h")
