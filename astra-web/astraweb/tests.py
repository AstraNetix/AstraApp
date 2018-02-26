import os, django, subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "astraweb.settings")
django.setup()

from api.models.user import User

class Tests():
    @staticmethod
    def test(func):
        func._is_for_test = True
        return func

    def cmnd_line_test(self, given_input, expected_output, preconditions, postchecks):
        given_input = given_input.split(" ")

        (precondition() for precondition in preconditions)

        test = subprocess.run(given_input, stdout=subprocess.PIPE)
        given_output = test.stdout.decode('utf-8')

        postcheck_results = [postcheck() for postcheck in postchecks]

        response = [expected_output, given_output, 
                        [(postchecks[i].__name__, postcheck_results[i]) 
                            for i in range(len(postchecks))
                        ]
                    ] if ((given_output != expected_output) or all(postcheck_results)) else False
        return response

    @classmethod
    def __main__(cls):
        tests = cls()
        methods = [getattr(tests, name) for name in dir(tests) 
            if getattr(getattr(tests, name),"_is_for_test",False)]
        outputs = [method() for method in methods]

        logs = {methods[i].__name__ : 
            ["success", None] if not outputs[i] else ["failure"] + outputs[i] 
            for i in range(len(outputs))
        }

        print(logs)
        for method_name, log in logs.items():
            if log[0] == "success":
                print("***" + method_name + " succeeded.")
            else:
                print("***" + method_name + " failed.\n")
                print("--------- Expected output ---------")
                print(log[1], "\n")
                print("--------- Given output ---------")
                print(log[2], "\n")
                print("--------- Postcheck failures ---------")
                (print("\t" + postcheck[0]) for postcheck in log[3] if postcheck[1])

class ViewSetTests(Tests):
    @Tests.test
    def test_set_user_verified_view(self):
        def email_is_verified(): 
            return User.objects.get(email='john@email.org').email_verified

        return self.cmnd_line_test(
            given_input = "http -a skale1@berkeley.edu:Starry1@nighT " +
                    "PATCH http://127.0.0.1:8000/api/users/id/set_user_verified/ " + 
                    "email=\"john@email.org\"",
            expected_output = """{"success": "User successfully email verified"}""",
            preconditions = [lambda: User.objects.get(email='john@email.org').set_email_invalid()],
            postchecks = [email_is_verified], 
        )

class UserTests(Tests):
    @Tests.test
    def send_mail(self):
        user = User.objects.get(email="skale1@berkeley.edu")
        user.send_email(subject="test", message="poop")

    @classmethod
    def __main__(cls):
        tests = UserTests()
        methods = [getattr(tests, name) for name in dir(tests) 
            if getattr(getattr(tests, name),"_is_for_test",False)]
        return [method() for method in methods]


if __name__ == "__main__":
    print(UserTests.__main__()[0])






