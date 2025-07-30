from odoo import api, fields, models, _, tools
from datetime import datetime, date


class egpـhr_recruitment_hr_applicant_report(models.TransientModel):
    _name = "hr.applicant.report"
    _description = "HR Applicant Report"

    position_ids = fields.Many2many('hr.job', string='Position Name')

    def action_print_xlsx_report(self):
        data = {
            'position_ids': self.position_ids.ids,  # Extract IDs here
            'create_date': self.create_date,

        }
        return self.env.ref('egp_hr_recruitment.action_hr_applicant_xlsx_report').report_action(self, data=data)


class egpـhr_recruitment_hr_applicant_reporttWizardAbstract(models.AbstractModel):
    _name = "report.egp_hr_recruitment.hr_applicant_xlsx_report_template"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, plans):
        job_ids = self.env['hr.job'].search([('id', 'in', data['position_ids'])])

        bold_format = workbook.add_format(
            {'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'size': 14})

        regular_format = workbook.add_format({'text_wrap': True, 'align': 'right', 'valign': 'vcenter', 'border': 1})

        date_format = workbook.add_format(
            {'num_format': 'yyyy-mm-dd', 'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'rotation': 90, })

        vertical_text_format = workbook.add_format(
            {'rotation': 90, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'size': 12})

        vertical_text_header_format = workbook.add_format(
            {'rotation': 90, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'size': 12})

        header_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'size': 12})

        for job in job_ids:
            long_listed_applicants = self.env['hr.applicant'].search([('job_id', '=', job.id)])

            sheet = workbook.add_worksheet(f' Long List for {job.name} position')
            row = 2
            sheet.merge_range(row, 3, row, 7, 'امارت اسلامی افغانستان', bold_format)
            sheet.merge_range(row + 1, 3, row + 1, 7, 'وزارت مخابرات وتکنالوجی معلوماتی', bold_format)
            sheet.merge_range(row + 2, 3, row + 2, 7, 'ریاست منابع بشری', bold_format)
            sheet.merge_range(row + 3, 3, row + 3, 7, 'امریت استخدام', bold_format)
            sheet.merge_range(row + 4, 3, row + 4, 7, ' لیست عمومی کاندیدان (لانګ لیست)', bold_format)

            sheet.merge_range(row + 6, 8, row + 6, 10, ' وزارت : مخابرات وتکنالوجی معلوماتی', header_format)
            sheet.merge_range(row + 7, 10, row + 8, 10, 'شماره', vertical_text_header_format)
            sheet.merge_range(row + 7, 8, row + 7, 9, 'شهرت کاندید', header_format)
            sheet.write(row + 8, 9, 'اسم وتخلص', header_format)
            sheet.write(row + 8, 8, 'ولد', header_format)
            sheet.merge_range(row + 6, 1, row + 6, 7, job.name, header_format)
            sheet.merge_range(row + 7, 3, row + 7, 4, 'جنسیت', header_format)
            sheet.write(row + 8, 3, 'زن', header_format)
            sheet.write(row + 8, 4, 'مرد', header_format)
            sheet.merge_range(row + 7, 7, row + 8, 7, 'ایمیل ادرس', header_format)
            sheet.merge_range(row + 7, 6, row + 8, 6, 'شماره تماس ', header_format)
            sheet.merge_range(row + 7, 5, row + 8, 5, 'تحصیلات ', header_format)
            sheet.merge_range(row + 7, 2, row + 8, 2, 'حضوری ', header_format)
            sheet.merge_range(row + 7, 1, row + 8, 1, 'انلاین ', header_format)
            sheet.write(row + 6, 0, 'تاریخ     /    ', header_format)
            sheet.merge_range(row + 7, 0, row + 8, 0, 'ملاحظات ', header_format)

            row = row + 9
            index = 1
            for applicant in long_listed_applicants:

                sheet.write(row, 10, index, regular_format)
                if applicant.partner_name:
                    sheet.write(row, 9, applicant.partner_name, regular_format)
                if applicant.Father_name:
                    sheet.write(row, 8, applicant.Father_name, regular_format)
                if applicant.email_from:
                    sheet.write(row, 7, applicant.email_from, regular_format)
                if applicant.partner_phone:
                    sheet.write(row, 6, applicant.partner_phone, regular_format)
                if applicant.type_id:
                    sheet.write(row, 5, applicant.type_id.name, regular_format)
                else:
                    sheet.write(row, 5, '', regular_format)

                if applicant.gender == 'male':
                    if applicant.gender == 'male':
                        sheet.write(row, 4, '✔', regular_format)
                    else:
                        sheet.write(row, 4, '', regular_format)
                else:
                    if applicant.gender == 'female':
                        if applicant.gender == "female":
                            sheet.write(row, 3, '✔', regular_format)
                    else:
                        sheet.write(row, 3, '', regular_format)
                        if applicant.type_of_application == 'online':
                            sheet.write(row, 6, '✔', regular_format)
                            sheet.write(row, 6, '', regular_format)
                        elif applicant.type_of_application == 'offline':
                            sheet.write(row, 6, '', regular_format)
                            sheet.write(row, 6, '✔', regular_format)

                sheet.write(row, 2, '', regular_format)
                sheet.write(row, 1, '', regular_format)
                sheet.write(row, 0, '', regular_format)
                row = row + 1
                index = index + 1

            # Longs list Committee Information

            sheet.merge_range(row + 3, 3, row + 3, 7, 'شهرت اعضای کمیټه', bold_format)
            sheet.write(row + 4, 10, 'شماره', header_format)
            sheet.merge_range(row + 4, 8, row + 4, 9, 'اسم وتخلص', header_format)
            sheet.merge_range(row + 4, 6, row + 4, 7, 'موقف در کمیته', header_format)
            sheet.merge_range(row + 4, 4, row + 4, 5, 'وظیفه', header_format)
            sheet.merge_range(row + 4, 0, row + 4, 3, 'امضاء', header_format)
            # Committee Cheif
            if applicant.committee_chief:
                sheet.write(row + 5, 10, 1, regular_format)
            if applicant.committee_chief:
                sheet.merge_range(row + 5, 8, row + 5, 9, applicant.committee_chief.name, regular_format)
            if applicant.committee_chief:
                sheet.merge_range(row + 5, 6, row + 5, 7, 'ریس کمیته', regular_format)
            if applicant.committee_chief.job_id:
                sheet.merge_range(row + 5, 4, row + 5, 5, applicant.committee_chief.job_id.name, regular_format)
            if applicant.committee_chief:
                sheet.merge_range(row + 5, 0, row + 5, 3, '', regular_format)

            # committee Members
            if applicant.committee_chief:
                comittee_index = 2
                committee_row = row + 6
            else:
                comittee_index = 1
                committee_row = row + 5

            for member in applicant.committee_members:
                sheet.write(committee_row, 10, comittee_index, regular_format)
                if member:
                    sheet.merge_range(committee_row, 8, committee_row, 9, member.name, regular_format)
                if member:
                    sheet.merge_range(committee_row, 6, committee_row, 7, 'عضو کمیته', regular_format)
                if member.job_id:
                    sheet.merge_range(committee_row, 4, committee_row, 5, member.job_id.name, regular_format)
                if member:
                    sheet.merge_range(committee_row, 0, committee_row, 3, '', regular_format)

                comittee_index = comittee_index + 1
                committee_row = committee_row + 1
