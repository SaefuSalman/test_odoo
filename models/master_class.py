from odoo import fields, api, models


class MasterClass(models.Model):
    _name = 'master.class'
    _description = 'Master Class'

    name = fields.Char('Kelas', required=True)
    tmp_student_ids = fields.One2many('tmp.student', 'class_id', string='Siswa')