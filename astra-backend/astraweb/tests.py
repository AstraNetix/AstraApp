import os, django, subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "astraweb.settings")
django.setup()
from django.db.utils import IntegrityError
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
                        [(postchecks[i].__name__, postcheck_results[i]) for i in range(len(postchecks))]
                    ] if ((given_output != expected_output) or all(postcheck_results)) else False
        return response

    @classmethod
    def __main__(cls):
        try:
            superuser = User.objects.create_superuser('superuser@gmail.com', 'Super1@useR')
        except IntegrityError: 
            superuser = User.objects.get(email='superuser@gmail.com')
        tests = cls()
        methods = [getattr(tests, name) for name in dir(tests) 
            if getattr(getattr(tests, name),"_is_for_test", False)]
        outputs = [method() for method in methods]
        superuser.delete()
        
        logs = {methods[i].__name__ : 
            ["success"] if not outputs[i] else ["failure"] + outputs[i] 
            for i in range(len(outputs))
        }
        for method_name, log in logs.items():
            method_name = method_name.title().replace('_', ' ')
            if log[0] == "success":
                print("*** " + method_name + " succeeded")
            else:
                print("*** " + method_name + " failed\n")
                print("---------- Expected output -----------")
                print(log[1], "\n")
                print("------------ Given output ------------")
                print(log[2], "\n")
                print("--------- Postcheck failures ---------")
                (print("\t" + postcheck[0]) for postcheck in log[3] if postcheck[1])
                print("\n\n\n")

class ViewSetTests(Tests):
    def make_test_user(self):
        user = User.objects.get_or_create(first_name='Test', last_name='User', email='test@test.com', password='password')[0]
        user.save()
        return user

    @Tests.test
    def test_user_creation(self):
        def check_creation():
            try:
                user = User.objects.get(email='test@test.com')
                return (str(user) == 'Test User' and 
                    user.name.password == 'password' and 
                    user.telegram_addr == 'telegram_addr' and
                    user.ether_addr == '0000000000000000000000000000000000000000')
            except User.DoesNotExist:
                return False

        return self.cmnd_line_test(
            given_input = "http -a superuser@gmail.com:Super1@useR " +
                    "POST http://127.0.0.1:8000/api/users/basic/create_user/ " + 
                    "name=\"{0}\" ".format('Test User') +
                    "confirm_password=\"{0}\" ".format('password') +
                    "email=\"{0}\" ".format('test@test.com') +
                    "password=\"{0}\" ".format('password') +
                    "telegram_addr=\"{0}\" ".format('telegram_addr') +
                    "ether_addr=\"{0}\"".format('0000000000000000000000000000000000000000'),
            expected_output = """{"success", "User successfully created"}""",
            preconditions = [lambda: User.objects.get_or_create(email='test@test.com')[0].delete()],
            postchecks = [check_creation]
        ) 

    @Tests.test
    def test_set_user_verified(self):
        user = self.make_test_user()
        def check_verification():
            nonlocal user 
            return user.email_verified
        print("http -a superuser@gmail.com:Super1@useR " +
                    "PATCH http://127.0.0.1:8000/api/users/id/set_user_verified/ " + 
                    "email=\"{0}\"".format(user.email))
        response = self.cmnd_line_test(
            given_input = "http -a superuser@gmail.com:Super1@useR " +
                    "PATCH http://127.0.0.1:8000/api/users/id/set_user_verified/ " + 
                    "email=\"{0}\"".format(user.email),
            expected_output = "{\"success\": \"User successfully email verified\"}",
            preconditions = [lambda: user.set_email_invalid()],
            postchecks = [check_verification], 
        )
        return response
    
    # @Tests.test
    # def test_user_login(self):
    #     user = self.make_test_user()
    #     def check_logged_in():
    #         nonlocal user 
    #         return user.logged_in

    #     response = self.cmnd_line_test(
    #         given_input = "http -a superuser@gmail.com:Super1@useR " +
    #                 "PATCH http://127.0.0.1:8000/api/users/login/login_user/ " + 
    #                 "email=\"{0}\" ".format(user.email) +
    #                 "password=\"{0}\" ".format(user.password),
    #         expected_output = """{"success", "Successfully logged in"}""",
    #         preconditions = [lambda: user.logout()],
    #         postchecks = [check_logged_in], 
    #     ) 
    #     user.delete()
    #     return response

    # @Tests.test
    # def test_user_update(self):
    #     user = self.make_test_user()
    #     def check_updated():
    #         nonlocal user 
    #         return all([
    #             str(user) == 'New Name', 
    #             user.email == 'new@new.com', 
    #             user.password == 'newpassword'
    #         ])

    #     response = self.cmnd_line_test(
    #         given_input = "http -a superuser@gmail.com:Super1@useR " +
    #                 "PATCH http://127.0.0.1:8000/api/users/update/update_user/ " + 
    #                 "email=\"{0}\" ".format(user.email) +
    #                 "name=\"{0}\" ".format("New Name") +
    #                 "new_email=\"{0}\" ".format("new@new.com") +
    #                 "old_password=\"{0}\" ".format(user.password) + 
    #                 "new_password=\"{0}\" ".format("newpassword") +
    #                 "confirm_password=\"{0}\" ".format("newpassword"),
    #         expected_output = """{"success", "User successfully updated"}""",
    #         preconditions = [lambda: user.logout()],
    #         postchecks = [check_updated], 
    #     ) 
    #     user.delete()
    #     return response
    
    # @Tests.test
    # def test_user_add_tokens(self):
    #     user = self.make_test_user()
    #     def check_tokens_added():
    #         nonlocal user 
    #         return user.ether_balance == 10

    #     response = self.cmnd_line_test(
    #         given_input = "http -a superuser@gmail.com:Super1@useR " +
    #                 "PATCH http://127.0.0.1:8000/api/users/balance/add_ether/ " + 
    #                 "email=\"{0}\" ".format(user.email) +
    #                 "ether_balance=\"10\" ",
    #         expected_output = """{"success", "Ether added"}""",
    #         preconditions = [],
    #         postchecks = [check_tokens_added], 
    #     ) 
    #     user.delete()
    #     return response

    # @Tests.test
    # def test_user_add_icokyc(self):
    #     user = self.make_test_user()
    #     def check_icokyc_added():
    #         nonlocal user 
    #         return all([
    #             user.first_name == 'First', 
    #             user.middle_name == 'Middle', 
    #             user.last_name == 'Last',
    #             user.street_addr1 == '1234 Fake St',
    #             user.street_addr2 == 'Apt. 0',
    #             user.city == 'Cityville',
    #             user.state == 'Florida',
    #             user.country == 'US',
    #             user.zip_code == '123456',
    #             user.phone_number == '1234567890',
    #             user.ether_addr == '0000000000000000000000000000000000000000',
    #             user.ether_part_amount == '1',
    #             user.referral == 'another@email.com',
    #         ])

    #     response = self.cmnd_line_test(
    #         given_input = "http -a superuser@gmail.com:Super1@useR " +
    #                 "PATCH http://127.0.0.1:8000/api/users/icokyc/add_ICOKYC_data/ " + 
    #                 "email=\"{0}\" ".format(user.email) +
    #                 "first_name=\"{0}\" ".format("First") + 
    #                 "middle_name=\"{0}\" ".format("Middle") + 
    #                 "last_name=\"{0}\" ".format("Last") + 
    #                 "street_addr1=\"{0}\" ".format("1234 Fake St.") + 
    #                 "street_addr2=\"{0}\" ".format("Apt. 0") + 
    #                 "city=\"{0}\" ".format("Cityville") + 
    #                 "state=\"{0}\" ".format("Florida") + 
    #                 "country=\"{0}\" ".format("US") + 
    #                 "zip_code=\"{0}\" ".format("123456") + 
    #                 "phone_number=\"{0}\" ".format("1234567890") + 
    #                 "ether_addr=\"{0}\" ".format("0000000000000000000000000000000000000000") + 
    #                 "ether_part_amount=\"{0}\" ".format("1") + 
    #                 "referral=\"{0}\" ".format("another@email.com"),
    #         expected_output = """{"success", "ICOKYC data successfully set"}""",
    #         preconditions = [],
    #         postchecks = [check_icokyc_added], 
    #     ) 
    #     user.delete()
    #     return response

if __name__ == "__main__":
    ViewSetTests.__main__()






