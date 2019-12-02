import os
import time

import allure
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from properties.p import Property
import locators


class Steps:
    driver = None
    main_page_url = "https://mail.google.com/mail/u/0/?ogbl#inbox"
    login_error_text = "Такая комбинация логин-пароль не найдена"

    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.path}
        chromeOptions.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def getProperty(self, name):
        prop = Property()
        dic_prop = prop.load_property_files('config.properties')
        return dic_prop.get(name)

    @allure.step("Выполнен ввод текста в поле")
    def send_text(self, locator, text):
        self.checkIsVisible(locator)
        element = self.getElement(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Выполнено нажатие на элемент")
    def clickOnElement(self, locator):
        self.checkIsVisible(locator)
        element = self.getElement(locator)
        element.click()

    def checkIsVisible(self, locator):
        if not self.isElementVisible(locator):
            raise AssertionError("Элемент не отображается на странице")

    def isElementVisible(self, locator):
        try:
            self.waitForElementBeVisible(locator)
            if self.driver.find_element(By.XPATH, locator).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def waitForElementBeVisible(self, locator):
        element = self.getElement(locator)
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of(element))
        except TimeoutException:
            raise AssertionError("Элемент не отображается на странице")

    def getElement(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        return element

    @allure.step("Выполнена проверка, что логин завершён успешно")
    def checkIsUserLoginComplete(self):
        if not self.isElementVisible(locators.Locators.INPUT_MAIL):
            raise AssertionError("Пользователь не был авторизирован")

    @allure.step("Выполнена проверка отправленного письма по имени")
    def checkSendMail(self, findText):
        self.send_text(locators.Locators.FIND_MAIL_FIELD, "in:sent " + findText)
        self.clickOnElement(locators.Locators.FIND_MAIL_BUTTON)
        time.sleep(5)
        try:
            self.driver.find_element(By.XPATH, "//*[text()='"+findText+"']")
        except AssertionError:
            raise AssertionError("Письмо не было отправлено")

    @allure.step("Выполнен логин")
    def login_to_system(self, login, password):
        self.driver.get(self.main_page_url)
        self.send_text(locators.Locators.LOGIN_FIELD, login)
        self.clickOnElement(locators.Locators.LOGIN_BUTTON_F)
        self.send_text(locators.Locators.PASSWORD_FIELD, password)
        self.clickOnElement(locators.Locators.LOGIN_BUTTON_S)
        time.sleep(5)
