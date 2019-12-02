import locators
import time

import steps


class TestingClass:
    def setup(self):
        self.step = steps.Steps()

    def test(self):
        print("Example test")
        self.step.login_to_system(self.step.getProperty("main.login"), self.step.getProperty("main.password"))
        self.step.checkIsUserLoginComplete()
        self.step.checkSendMail(self.step.getProperty("main.theme_mail"))

