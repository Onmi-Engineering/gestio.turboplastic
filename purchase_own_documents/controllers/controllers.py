# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseOwnDocuments(http.Controller):
#     @http.route('/purchase_own_documents/purchase_own_documents/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_own_documents/purchase_own_documents/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_own_documents.listing', {
#             'root': '/purchase_own_documents/purchase_own_documents',
#             'objects': http.request.env['purchase_own_documents.purchase_own_documents'].search([]),
#         })

#     @http.route('/purchase_own_documents/purchase_own_documents/objects/<model("purchase_own_documents.purchase_own_documents"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_own_documents.object', {
#             'object': obj
#         })
