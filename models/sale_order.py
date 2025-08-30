# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from odoo.exceptions import ValidationError
from datetime import datetime

class xx_account_move(models.Model):
    _inherit = 'sale.order'
 

    def validation_customer_balance(self):
        global x
        x = 0
        for partner in self:
            sql_query = """select sum(debit) - sum(credit) as balance from account_move h, account_move_line l where account_id in (select id from account_account where internal_type in ('receivable','payable')) and h.company_id=l.company_id and h.id=l.move_id and upper(state)='POSTED'"""
            sql_query += " and l.partner_id=%s " % partner.partner_id.id
            sql_query += " and l.company_id=%s " % self.env.company.id

            self.env.cr.execute(sql_query)
            seq = self.env.cr.fetchone()
            x = seq[0]
           
            return x

    def actionc_confirm(self):
        for rec in self:
            current_balance = rec.validation_customer_balance()

            # new_balance = balance + rec.amount_total
            if current_balance > rec.partner_id.credit_limit:
                    raise ValidationError(
                                "تنبيه .. رصيد العميل [%s] تجاوز الحد الائتماني  .. الحد الائتماني [ %s ]>>> رصيد العميل [ %s ]" % (
                                    rec.partner_id.name, rec.partner_id.credit_limit, current_balance))

        invoice = super(xx_account_move, self).actionc_confirm()
        
        return invoice
     