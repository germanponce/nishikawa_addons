
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
#
#
#    info skype: german_442 email: (german.ponce@hesatecnica.com)
############################################################################
#    Coded by: german_442 email: (german_442@hotmail.com)
#
##############################################################################

from osv import osv, fields
from tools.translate import _
from tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, date
import decimal_precision as dp
import time

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit ='res.partner'
    _columns = {
        'payment_csv': fields.boolean('Pago mediante CSV', help='Indica Si a estos Proveedores se les paga mediante un Archivo CSV generado por el Asistende de OpenERP.', )
        }

    _default = {
        }
res_partner()