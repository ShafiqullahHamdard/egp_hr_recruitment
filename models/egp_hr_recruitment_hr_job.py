from odoo import api, fields, models


class Job(models.Model):
    _inherit = 'hr.job'
    website_published = fields.Boolean(help='Set if the application is published on the website of the company.'
                                       ,
                                       groups="hr.group_hr_user,egp_hr_recruitment.group_recruitment_amir,egp_hr_recruitment.group_recruitment_Karshanas",
                                       tracking=True)
