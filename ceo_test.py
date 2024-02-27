from agents.CEO_persona import CEO


class TestCEO:
    def test_review_employee(self):
        ceo = CEO()
        employee_name = "John Doe"
        employee_message = "I am working on a new feature for the application."
        response = ceo.review_employee(employee_name, employee_message)
        print(response)
        assert response is not None
        assert response != ""
TestCEO().test_review_employee()