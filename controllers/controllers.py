# -*- coding: utf-8 -*-
from odoo import http, _, exceptions
from odoo.http import request
import json 
import requests
from odoo.tests import Form
import werkzeug.wrappers


class GetRestApiMasterTeacher(http.Controller):
    @http.route('/api/master_teacher_get', type='http', auth='public', methods=['GET'], csrf=False)
    def master_teacher_rest_api(self, **params):
        # get_id = params.get('id')
        teacher_request = request.env['master.teacher'].sudo().search([])
        print(teacher_request, 'MASUKKKK TEaCHERRR')
        data_teacher = []
        for teach in teacher_request:
            data_teacher.append({
                'name': teach.name,
                'alamat': teach.alamat,
                'no_telepon': teach.no_telepon,
                'status': teach.status,
                'jabatan': teach.jabatan,
                'pendidikan': teach.pendidikan,
                'kelas': teach.master_class_id.name
            })
        print(data_teacher, 'DATA TEACHERRRR')
        data = {
            'status': 200,
            'message': 'success',
            'response': data_teacher
        }
        try: 
            return werkzeug.wrappers.Response(
                status= 200,
                content_type= 'application/json; charset=utf-8',
                response =json.dumps(data)
            )
        except Exception as e:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json; charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_descrip': str(e),
                })
            )

    @http.route('/api/master_student_post', type='json', auth='public', methods=['POST'], csrf=False)
    def master_student_rest_api_post(self, **params):
        try:
            student = request.env['master.student'].sudo().create({
                'name': params['name'],
                'gender': params['gender'],
                'tanggal_lahir': params['tanggal_lahir']
            })
            return {'success': True, 'student_id': student.id}
        except Exception as e:
            return {'error': str(e)}

    