# -*- coding: utf-8 -*-
##############################################################################
#
#    Author Vincent Renaville.
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

# from openerp import models, fields, exceptions
from openerp.osv import fields, orm
from openerp import exceptions


class AccountMove(orm.Model):
    _inherit = 'account.move'
    
    _columns = {
        'locked':fields.boolean('Locked', readonly=False)
    }

    # locked = fields.boolean('Locked', readonly=True)

#    @api.multi
    def write(self, vals):
        for move in self:
            if move.locked:
                raise exceptions.Warning(_('Move Locked!'),
                                         move.name)
        return super(AccountMove, self).write(vals)

#    @api.multi
    def unlink(self):
        for move in self:
            if move.locked:
                raise exceptions.Warning(_('Move Locked!'),
                                         move.name)
        return super(AccountMove, self).unlink()

#    @api.multi
    #def button_cancel(self):
    def button_cancel(self, cr, uid, ids, context=None):
        # Cancel a move was done directly in SQL
        # so we need to test manualy if the move is locked
        #for move in self:
        #   if move.locked:
        #      raise exceptions.Warning(_('Move Locked!'),
        #                              move.name)                
        for line in self.browse(cr, uid, ids, context=context):
            if line.locked:
                raise exceptions.Warning(_('Move Locked!'), line.name)
            
            #if not line.journal_id.update_posted:
                #raise osv.except_osv(_('Error!'), _('You cannot modify a posted entry of this journal.\nFirst you should set the journal to allow cancelling entries.'))
        return super(AccountMove, self).button_cancel(cr, uid, ids, context)
