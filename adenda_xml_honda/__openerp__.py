# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2010 moylop260 - http://www.hesatecnica.com.com/
#    All Rights Reserved.
#    info skype: german_442 email: (german.ponce@hesatecnica.com)
############################################################################
#    Coded by: german_442 email: (german.ponce@hesatecnica.com)
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
#
##############################################################################
{
    'name': 'Adenda Honda',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "Nishikawa",
    'description': """

            Este modulo permite que al generar la Validacion de Una Factura, en el proceso de la Generacion del Archivo XML, se agrega una Adenda Nueva (Honda) .
    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","l10n_mx_facturae","l10n_mx_ir_attachment_facturae"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [

                    ],
    "installable" : True,
    "active" : False,
}
