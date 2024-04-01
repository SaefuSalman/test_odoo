from odoo import fields, api, models, _


class MasterTeacher(models.Model):
    _name = 'master.teacher'
    _description = 'Master Teacher'

    name = fields.Char('Name', required=True)
    alamat = fields.Char('Alamat')
    no_telepon = fields.Char('No Telepon')
    status = fields.Selection([
        ('menikah', 'Menikah'),
        ('blm_menikah', 'Belum Menikah')
    ], string='Status')
    jabatan = fields.Char('Jabatan')
    pendidikan = fields.Char('pendidikan')
    student_ids = fields.One2many('tmp.student', 'teacher_id', string='student')
    count_student = fields.Integer(compute='_compute_count_student', string='Count Student')
    master_class_id = fields.Many2one('master.class', string='Wali Kelas')

    _sql_constraints = [
        ("no_telepon_unique", "unique(no_telepon)", "Nomor Telepon kudu Uniq"),
    ]

    def _compute_count_student(self):
        for rec in self:
            student = rec.env['master.student']
            domain = [('id', 'in', rec.master_class_id.tmp_student_ids.mapped('student_id.id'))]
            student_ids = student.search_count(domain)
            rec.count_student = student_ids

    def action_view_student(self):
        self.ensure_one()
        # for tmp in self.master_class_id.tmp_student_ids:
        domain = [('id', 'in', self.master_class_id.tmp_student_ids.mapped('student_id.id'))]

        return {
            'name': _('Student'),
            'res_model': 'master.student',
            'type': 'ir.actions.act_window',
            'domain': domain,
            # 'view_id': False,
            'view_mode': 'tree,form',
            'help': _('''<p class="oe_view_nocontent_create">
                            Klik untuk Membuat untuk form student
                        </p>'''),
            'limit': 80
        }    

