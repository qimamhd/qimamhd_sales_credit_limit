# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from odoo.exceptions import ValidationError
from datetime import datetime

class xx_account_move(models.Model):
    _inherit = 'sale.order'
 
    def actionc_confirm(self):
        for rec in self:
            
            current_balance = rec.partner_id.validation_customer_balance(rec.amount_total, rec.partner_id,rec.id,False)

            # new_balance = balance + rec.amount_total
            if current_balance > rec.partner_id.credit_limit:
                    raise ValidationError(
                                "تنبيه .. رصيد العميل [%s] تجاوز الحد الائتماني  .. الحد الائتماني [ %s ]>>> رصيد العميل [ %s ]" % (
                                    rec.partner_id.name, rec.partner_id.credit_limit, current_balance))

            invoice = super(xx_account_move, self).actionc_confirm()
        
        return invoice
     