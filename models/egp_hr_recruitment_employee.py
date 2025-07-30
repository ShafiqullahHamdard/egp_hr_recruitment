from odoo import fields, models, api


class egp_hr_recruitmentEmployee(models.Model):
    _inherit = "hr.employee"

    issue_date = fields.Char(string='Issue Date')
    expire_date = fields.Char(string='Expire Date')
    # pashto_position_title = fields.Char(string='Pashto/Farsi Position Title', required=True)
    # employee_pashto_name = fields.Char(string='Pashto/Farsi Employee Name', required=True)
    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.",
                          groups="hr.group_hr_user,egp_hr_recruitment.group_recruitment_amir,egp_hr_recruitment.group_recruitment_Karshanas,egp_hr_recruitment.group_recruitment_id_card_manager",
                          copy=False)

    message_main_attachment_id = fields.Many2one(
        'ir.attachment',
        string="Main Attachment",
        groups="egp_hr_recruitment.group_recruitment_id_card_manager,hr.group_hr_user,egp_hr_recruitment.group_recruitment_Karshanas,egp_hr_recruitment.group_recruitment_amir,base.group_erp_manager,egp_hr.group_employee_officers")
