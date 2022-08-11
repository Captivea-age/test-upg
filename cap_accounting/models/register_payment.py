from odoo import models, fields, api, _
import logging
logger = logging.getLogger(__name__)


class AccountMove(models.Model):
	_inherit = "account.move"

	# def action_register_payment(self):
	#	 ''' Open the account.payment.register wizard to pay the selected journal entries.
	#	 :return: An action opening the account.payment.register wizard.
	#	 '''
	#	 cash_journal_id = self.env['account.journal'].search([('name','=','First Horizon - Cash/Check')],limit=1)
	#	 return {
	#		 'name': _('Register Payment'),
	#		 'res_model': 'account.payment.register',
	#		 'view_mode': 'form',
	#		 'context': {
	#			 'active_model': 'account.move',
	#			 'active_ids': self.ids,
	#			 'default_journal_id':cash_journal_id[0].id,
	#		 },
	#		 'target': 'new',
	#		 'type': 'ir.actions.act_window',
	#	 }

	def action_invoice_print(self):
		""" Print the invoice and mark it as sent, so that we can see more
			easily the next step of the workflow
		"""

		if any(not move.is_invoice(include_receipts=True) for move in self):
			#raise UserError(_("Only invoices could be printed."))
			logger.error('Only invoices could be printed.')
		self.filtered(lambda inv: not inv.is_move_sent).write({'is_move_sent': True})
		if self.user_has_groups('account.group_account_invoice'):
			return self.env.ref('account.account_invoices').report_action(self)
		else:
			return self.env.ref('account.account_invoices_without_payment').report_action(self)


	def _get_report_base_filename(self):
		if any(not move.is_invoice() for move in self):
			#raise UserError(_("Only invoices could be printed."))
			logger.error('Only invoices could be printed.')
		return self._get_move_display_name()



class AccountPaymentRegister(models.TransientModel):
	_inherit = 'account.payment.register'

	@api.depends('company_id', 'source_currency_id')
	def _compute_journal_id(self):
		for wizard in self:
			domain = [
				('type', 'in', ('bank', 'cash')),
				('company_id', '=', wizard.company_id.id),
			]
			journal = None
			cash_journal_id = self.env['account.journal'].search([('name','=','First Horizon - Cash/Check')],limit=1)
			if not cash_journal_id:
				if wizard.source_currency_id:
					journal = self.env['account.journal'].search(domain + [('currency_id', '=', wizard.source_currency_id.id)], limit=1)
				if not journal:
					journal = self.env['account.journal'].search(domain, limit=1)
				wizard.journal_id = journal
			else:
				wizard.journal_id = cash_journal_id.id