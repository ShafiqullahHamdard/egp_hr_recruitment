from odoo import http
from odoo.http import request

class HelloWorldController(http.Controller):

    @http.route('/my/education-attachments', type='http', auth='user', website=True)
    def education_attachments(self, **kw):
        return http.request.render('egp_hr_recruitment.education_attachments', {})
