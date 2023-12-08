class ErrorRequestBodyScheduleSave():

    def test_save_incorrect_schedule_with_empty_request_body(self):
        """
        Testa o salvamento de uma grade horária com um corpo de requisição vazio.

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        response = self.make_post_request()

        error_msg = 'the request body must not be empty'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_non_list_request_body(self):
        """
        Testa o salvamento de uma grade horária com um corpo de requisição que não é uma lista.

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        response = self.make_post_request(schedule="""{
            "hey": "there"
        }""")

        error_msg = 'the request body must be a list of classes'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_non_dict_class(self):
        """
        Testa o salvamento de uma grade horária com uma turma que não é um dicionário.

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        response = self.make_post_request(schedule=[1, 2, 3])

        error_msg = 'each class must be a object structure'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_no_discipline_key(self):
        """
        Testa o salvamento de uma grade horária com uma turma que não tem a chave "discipline".

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        response = self.make_post_request(schedule="""[{
            "schedule": "35T23",
            "class": "1",
            "teachers": ["EDSON ALVES DA COSTA JUNIOR"],
            "classroom": "FGA - I8",
            "days": ["Terça-feira 14:00 às 15:50", "Quinta-feira 14:00 às 15:50"],
            "special_dates": []

        }]""")

        error_msg = 'the class must have the discipline key'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_non_dict_discipline(self):
        """
        Testa o salvamento de uma grade horária com uma disciplina que não é um dicionário.

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        response = self.make_post_request(schedule="""[{
            "discipline": 1,
            "schedule": "35T23",
            "class": "1",
            "teachers": ["EDSON ALVES DA COSTA JUNIOR"],
            "classroom": "FGA - I8",
            "days": ["Terça-feira 14:00 às 15:50", "Quinta-feira 14:00 às 15:50"],
            "special_dates": []

        }]""")

        error_msg = 'the discipline must be a object structure'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_no_discipline_name_key(self):
        """
        Testa o salvamento de uma grade horária com uma disciplina que não tem a chave "name".

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        response = self.make_post_request(schedule="""[{
            "discipline": {},
            "schedule": "35T23",
            "class": "1",
            "teachers": ["EDSON ALVES DA COSTA JUNIOR"],
            "classroom": "FGA - I8",
            "days": ["Terça-feira 14:00 às 15:50", "Quinta-feira 14:00 às 15:50"],
            "special_dates": []

        }]""")

        error_msg = 'the discipline must have the name key'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_no_dict_discipline_department(self):
        """
        Testa o salvamento de uma grade horária com uma disciplina que não tem a chave "department".

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        response = self.make_post_request(schedule="""[{
            "discipline": {
                "name": "CÁLCULO 1",
                "code": "MAT0025",
                "department": []                    
            },
            "schedule": "35T23",
            "class": "1",
            "teachers": ["EDSON ALVES DA COSTA JUNIOR"],
            "classroom": "FGA - I8",
            "days": ["Terça-feira 14:00 às 15:50", "Quinta-feira 14:00 às 15:50"],
            "special_dates": []

        }]""")

        error_msg = 'the department must be a object structure'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_no_dict_discipline_department_year(self):
        """
        Testa o salvamento de uma grade horária com uma disciplina que não tem a chave "year".

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        response = self.make_post_request(schedule="""[{
            "discipline": {
                "name": "CÁLCULO 1",
                "code": "MAT0025",
                "department": {
                    "period": "2"
                }                    
            },
            "schedule": "35T23",
            "class": "1",
            "teachers": ["EDSON ALVES DA COSTA JUNIOR"],
            "classroom": "FGA - I8",
            "days": ["Terça-feira 14:00 às 15:50", "Quinta-feira 14:00 às 15:50"],
            "special_dates": []

        }]""")

        error_msg = 'the department must have the year key'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)
