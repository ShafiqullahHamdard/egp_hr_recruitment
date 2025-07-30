from importlib.resources import _

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class egp_hr_recruitmentApplicant(models.Model):
    _inherit = "hr.applicant"

    Father_name = fields.Char(string='Father Name')
    partner_name = fields.Char(string="Applicant's Name",required=True)
    province = fields.Many2one('res.country.state', string="Province", tracking=True, ondelete='cascade')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], tracking=True, default="male")
    LANGUAGES = [
        ('en_US', 'English'),
        ('ps', 'Pashto'),
        ('prs', 'Dari'),
        ('arabic', 'Arabic'),
        ('other', 'Other'),
    ]
    native_language = fields.Selection(LANGUAGES, string='Native Language', default='ps')
    type_of_application = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline')
    ], string='Type of application', required=True, default='online')

    website_published = fields.Boolean(help='Set if the application is published on the website of the company.',
                                       tracking=True, default=0)
    salary_proposed_extra = fields.Char("Proposed Salary Extra",
                                        help="Salary Proposed by the Organisation, extra advantages", tracking=True,
                                        groups="hr_recruitment.group_hr_recruitment_user,egp_hr_recruitment.group_recruitment_amir,egp_hr_recruitment.group_recruitment_Karshanas")

    salary_expected_extra = fields.Char("Expected Salary Extra", help="Salary Expected by Applicant, extra advantages",
                                        tracking=True,

                                        groups="hr_recruitment.group_hr_recruitment_user,egp_hr_recruitment.group_recruitment_amir,egp_hr_recruitment.group_recruitment_Karshanas")
    salary_proposed = fields.Float("Proposed Salary", group_operator="avg", help="Salary Proposed by the Organisation",
                                   tracking=True,
                                   groups="hr_recruitment.group_hr_recruitment_user,egp_hr_recruitment.group_recruitment_amir,egp_hr_recruitment.group_recruitment_Karshanas")
    salary_expected = fields.Float("Expected Salary", group_operator="avg", help="Salary Expected by Applicant",
                                   tracking=True,
                                   groups="hr_recruitment.group_hr_recruitment_user,egp_hr_recruitment.group_recruitment_amir,egp_hr_recruitment.group_recruitment_Karshanas")
    job_id = fields.Many2one('hr.job', "Applied Job")
    position_rank_id = fields.Selection(related='job_id.position_rank', string='Position Rank', store=True)
    position_code = fields.Char(related='job_id.code', string='Job Code', store=True)
    work_location_id = fields.Many2one(related='job_id.work_location_id', string='Work Location')
    total_years_experience = fields.Selection([
        ('1', '1 year'),
        ('2', '2 years'),
        ('3', '3 years'),
        ('4', '4 years'),
        ('5', '5 years'),
        ('6', '6 years'),
        ('7', '7 years'),
        ('8', '8 years'),
        ('9', '9 years'),
        ('10', '10 years'),
        ('11', 'Above than 10')
    ], string='Total Years of Experience')

    committee_members = fields.Many2many('hr.employee', string='Committee Members', tracking=True)
    committee_chief = fields.Many2one('hr.employee', string='Committee Chief', tracking=True)
    @api.depends('committee_members')
    def _compute_committee_member_positions(self):
        for record in self:
            record.committee_member_positions = ', '.join(record.committee_members.mapped('job_id.name'))

    committee_member_positions = fields.Char(compute="_compute_committee_member_positions", string="Positions")
