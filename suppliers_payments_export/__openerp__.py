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
    'name': 'Generacion de Archivos de Banca Electronica a Proveedores',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "Nishikawa",
    'description': """

            Este modulo permite Generar un Archivo Electronico para el registro de Pagos para los Bancos:
                - Banamex
                - Agrega un Check en los Proveedores para indicar a cuales se les genera Pago.
                    --> En la ficha de Proveedores activar el check, pago mediante CSV.
                - El Asistente para Generar el Layout se encuenta en: Compras --> Pago Proveedores --> Exportar Pago Proveedores

    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","purchase"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'partner_view.xml',
                    'supplier_view.xml',
                    'security/ir.model.access.csv',
                    ],
    "installable" : True,
    "active" : False,
}
