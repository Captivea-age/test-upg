# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class GamificationChallenge(models.Model):
    _inherit='gamification.challenge'

    parent_challenge_id = fields.Many2one('gamification.challenge', string='Parent challenge', ondelete='set null')
    week_number = fields.Integer(string='Week Number')
    year = fields.Integer(string='Year')
    child_challenges = fields.One2many('gamification.challenge', 'parent_challenge_id', string='Child Challenges')
