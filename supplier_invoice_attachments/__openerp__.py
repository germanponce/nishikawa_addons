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
    'name': 'Validacion de Facturas de Proveedor',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "Nishikawa",
    'description': """

            Este modulo NO permite Validar una factura si no tiene adjunto el XML y PDF del proveedor.

            Para el manejo de las Excepciones, si alguna Factura se necesita Validar sin Tener adjunto los archivos mencionados, existe un boton para llamado Autorizar Factura y pide la contraseña de Usuarios en el Grupo Gestor financiero, solo los usuarios de este grupo pueden validar las facturas con esta Excepcion.

    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","purchase"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'account_invoice_view.xml',
                    ],
    "installable" : True,
    "active" : False,
}
