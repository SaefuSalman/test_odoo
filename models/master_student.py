from odoo import fields, models, api
import locale


class MasterStudent(models.Model):
    _name = 'master.student'
    _description = 'Master Student'

    name = fields.Char('Nama Siswa', required=True)
    gender = fields.Selection([
        ('laki_laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Gender')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    active = fields.Boolean('Active', default=True)
    partner_id = fields.Many2one('res.partner', string="use", compute="compute_partner_id")
    move_id = fields.Many2one('account.move', string="Pembayaran")
    flag_post_move = fields.Boolean(compute="default_flag_post_move", store=True)
    sum_move = fields.Float('sum', compute='sum_total')
    
    def sum_total(self):
        for rec in self:
            if rec.move_id:
                rec.sum_move = sum(total.price_subtotal for total in rec.move_id.mapped('invoice_line_ids'))

    @api.depends('move_id')
    def default_flag_post_move(self):
        for rec in self:
            if rec.move_id.state == 'posted':
                print('Masukkkk')
                rec.flag_post_move = True
            else:
                print('TIDAKKKK Masukkkk')
                rec.flag_post_move = False

    def button_master_student_print(self):
        return self.env.ref('training_odoo.report_master_student_action_id').report_action(self)

    def compute_partner_id(self):
        for rec in self:
            same_user = rec.env['res.partner'].search([('name', '=', rec.name)], limit=1)
            rec.partner_id = same_user.id if same_user else False

    @api.model
    def create(self, vals):
        sup = super(MasterStudent, self).create(vals)
        create_res_partner = {
            'name': sup.name,
        }
        self.env['res.partner'].create(create_res_partner)
        return sup

    @api.model
    def scheduler_account_move(self):
        all_students = self.env['master.student'].search([('active', '=', True)])
        last_invoice = False
        for student in all_students:
            if student.partner_id:
                invoice = self.env['account.move'].sudo().create({
                    'partner_id': student.partner_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [(0, 0, {
                        'product_id': 17, # masih hardcode
                        'name': 'Meja', # masih hardcode
                        'quantity': 1,
                        'price_unit': 5000000,
                        'account_id': 21,
                    })]
                })
                # invoice.action_post()
                if invoice:
                    student.move_id = invoice.id
                    last_invoice = invoice
                print(invoice, 'invoice invoice invoice')
        return last_invoice  


class TmpStudent(models.Model):
    _name = 'tmp.student'
    _description = 'Tampungan Student'

    student_id = fields.Many2one('master.student', string='Nama Siswa', required=True)
    gender = fields.Selection([
        ('laki_laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Gender', related='student_id.gender')
    tanggal_lahir = fields.Date('Tanggal Lahir', related='student_id.tanggal_lahir')
    class_id = fields.Many2one('master.class', string='Kelas')
    teacher_id = fields.Many2one('master.teacher', string='teacher')
