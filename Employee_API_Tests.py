try:
    import unittest
    import json
    from Your_Own_API_Ehlert import app
except Exception as e:
    print('Some Modules are Missing{} '.format(e))


class FlaskAPITest(unittest.TestCase):

    # check for response 200
    def test_index_response_200(self):
        test_app = app.test_client(self)
        response = test_app.get('/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_index_response_404(self):
        test_app = app.test_client(self)
        response = test_app.get('/404')
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_api_all_200(self):
        test_app = app.test_client(self)
        response = test_app.get('/api/v1/resources/employees/all')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_api_all_404(self):
        test_app = app.test_client(self)
        response = test_app.get('/api/v1/resource/employees/all')
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    # def test_api_all_json_fields(self):
    #     test_app = app.test_client(self)
    #     response = test_app.get('/api/v1/resource/employees/all')
    #     json_data = json.loads(response.data)

    def test_api_param_200(self):
        test_app = app.test_client(self)
        response_one_good_param = test_app.get('/api/v1/resources/employees?age=25')
        response_two_good_param = test_app.get('/api/v1/resources/employees?aeg=25&id=E0')
        response_three_good_param = test_app.get('/api/v1/resources/employees?aeg=25&i d=E0&gender=male')
        response_four_good_param = test_app.get('/api/v1/resources/employees?aeg=25&id=E0&gender=male&full+name=Name')
        status_code_one_good_param = response_one_good_param.status_code
        status_code_two_good_param = response_two_good_param.status_code
        status_code_three_good_param = response_three_good_param.status_code
        status_code_four_good_param = response_four_good_param.status_code
        self.assertEqual(status_code_one_good_param, 200)
        self.assertEqual(status_code_two_good_param, 200)
        self.assertEqual(status_code_three_good_param, 200)
        self.assertEqual(status_code_four_good_param, 200)

    def test_api_param_404(self):
        test_app = app.test_client(self)
        response_one_bad_param = test_app.get('/api/v1/resources/employees?aeg=25')
        response_two_bad_param = test_app.get('/api/v1/resources/employees?aeg=25&i d=E0')
        response_three_bad_param = test_app.get('/api/v1/resources/employees?aeg=25&i d=E0&gedner=male')
        response_four_bad_param = test_app.get('/api/v1/resources/employees?aeg=25&i d=E0&gedner=male&fullname=Name')
        status_code_one_bad_param = response_one_bad_param.status_code
        status_code_two_bad_param = response_two_bad_param.status_code
        status_code_three_bad_param = response_three_bad_param.status_code
        status_code_four_bad_param = response_four_bad_param.status_code
        self.assertEqual(status_code_one_bad_param, 404)
        self.assertEqual(status_code_two_bad_param, 404)
        self.assertEqual(status_code_three_bad_param, 404)
        self.assertEqual(status_code_four_bad_param, 404)


if __name__ == '__main__':
    unittest.main()
