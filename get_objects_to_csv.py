# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DOTENV_PATH = os.path.join(BASE_PATH, '.env')
load_dotenv(DOTENV_PATH)

import logging, time
import unittest, json, csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException

class TestRosAccreditationSite(unittest.TestCase):

    def setUp(self):
        # initialize logget
        self.logger = logging.getLogger(__name__)
        logger_handler = logging.FileHandler(os.path.join(BASE_PATH, '{}.log'.format(__file__)))
        logger_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logger_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_handler)
        self.logger.setLevel(logging.WARNING)
        self.logger.propagate = False

        # self.display = Display(visible=0, size=(1024,800))
        # self.display.start()

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.chromedriver_path = os.path.join(self.current_path, 'chromedriver')
        self.driver = webdriver.Chrome(self.chromedriver_path)
        self.write_filename = 'output.csv'

    def test_get_offers_list(self):
        driver = self.driver
        # driver.implicitly_wait(15)

        try:
            links = []
            with open('links.json', 'r') as read_file:
                links = json.loads(read_file.read())

            with open(self.write_filename, 'w', encoding='utf-8') as write_file:
                csv_writer = csv.writer(write_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_ALL, lineterminator='\n')
                col_names = [
                    'Реквизиты сертификата', # ПУСТОЙ СТОЛБЕЦ
                    'Регистрационный номер',
                    'Дата начала действия',
                    'Дата окончания действия',
                    'Сведения о заявителе', # ПУСТОЙ СТОЛБЕЦ
                    'Вид заявителя',
                    'Полное наименование',
                    'Адрес места нахождения',
                    'Фактический адрес',
                    'Номер телефона',
                    'Адрес электронной почты',
                    'Основной государственный регистрационный номер записи о государственной регистрации юридического лица (ОГРН)',
                    'Сведения об изготовителе иностранном юридическом лице (изготовитель)', # ПУСТОЙ СТОЛБЕЦ
                    'Полное наименование',
                    'Адрес места нахождения',
                    'Номер телефона',
                    'Адрес электронной почты',
                    'Сведения о продукции', # ПУСТОЙ СТОЛБЕЦ
                    '«Тип объекта сертификации»: серийный выпуск, партия, единичное изделие',
                    'Вид продукции',
                    'Полное наименование продукции',
                    'Сведения о продукции (тип, марка, модель, сорт, артикул и др.), обеспечивающие ее идентификацию',
                    'Код ТН ВЭД ЕАЭС',
                    'Технический регламент',
                    'Технический регламент',
                    'Технический регламент',
                    'Сведения об органе по сертификации', # ПУСТОЙ СТОЛБЕЦ
                    'Полное наименование',
                    'Номер аттестата',
                ]
                csv_writer.writerow([i.encode('utf8').decode('utf8') for i in col_names])

                for page_url in links:
                    driver.get(page_url)

                    initial_wait = WebDriverWait(driver, 60*60) # wait until capcha entered
                    try:
                        initial_wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.step-title'))
                        )

                        ### 'Реквизиты сертификата'
                        # 'Регистрационный номер',
                        try:
                            a_reg_number = driver.find_element_by_css_selector('#a_reg_number > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            a_reg_number = ' '
                        # 'Дата начала действия'
                        try:
                            a_date_begin = driver.find_element_by_css_selector('#a_date_begin > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            a_date_begin = ' '
                        # 'Дата окончания действия'
                        try:
                            a_date_finish = driver.find_element_by_css_selector('#a_date_finish > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            a_date_finish = ' '
                        ### 'Сведения о заявителе'
                        # 'Вид заявителя'
                        try:
                            applicant_type = driver.find_element_by_css_selector('#a_applicant_info-rds-app_legal_person-applicant_type > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            applicant_type = ' '
                        # 'Полное наименование'
                        try:
                            legal_person_name = driver.find_element_by_css_selector('#a_applicant_info-rds-app_legal_person-name > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            legal_person_name = ' '
                        # 'Адрес места нахождения'
                        try:
                            app_legal_person_address = driver.find_element_by_css_selector('#address_element_applicant_info-rds-app_legal_person-address_0_caption').text
                        except (NoSuchElementException, TimeoutException):
                            app_legal_person_address = ' '
                        # 'Фактический адрес'
                        try:
                            app_legal_person_address_actual = driver.find_element_by_css_selector('#address_element_applicant_info-rds-app_legal_person-address_actual_0_caption').text
                        except (NoSuchElementException, TimeoutException):
                            app_legal_person_address_actual = ' '
                        # 'Номер телефона'
                        try:
                            app_legal_person_phones = driver.find_element_by_css_selector('#a_applicant_info-rds-app_legal_person-phone > .form-right-col')
                            array_field = app_legal_person_phones.find_elements_by_class_name('array-field')
                            app_legal_person_phones = ", ".join([elem.text for elem in array_field])
                        except (NoSuchElementException, TimeoutException):
                            app_legal_person_phones = ' '
                        # 'Адрес электронной почты',
                        try:
                            app_legal_person_emails = driver.find_element_by_css_selector('#a_applicant_info-rds-app_legal_person-email > .form-right-col')
                            array_field = app_legal_person_emails.find_elements_by_class_name('array-field')
                            app_legal_person_emails = ", ".join([elem.text for elem in array_field])
                        except (NoSuchElementException, TimeoutException):
                            app_legal_person_emails = ' '
                        # 'Основной государственный регистрационный номер записи о государственной регистрации юридического лица (ОГРН)',
                        try:
                            app_legal_person_ogrn = driver.find_element_by_css_selector('#a_applicant_info-rds-app_legal_person-ogrn > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            app_legal_person_ogrn = ' '
                        ### 'Сведения об изготовителе иностранном юридическом лице (изготовитель)',
                        # 'Полное наименование'
                        try:
                            man_legal_person_name = driver.find_element_by_css_selector('#a_manufacturer_info-rds-man_legal_person-name > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            try:
                                man_legal_person_name = driver.find_element_by_css_selector('#a_manufacturer_info-rds-man_foreign_legal_person-name > .form-right-col').text
                            except (NoSuchElementException, TimeoutException):
                                man_legal_person_name = ' '
                        # 'Адрес места нахождения'
                        try:
                            man_legal_person_address_0_caption = driver.find_element_by_css_selector('#address_element_manufacturer_info-rds-man_legal_person-address_0_caption').text
                        except (NoSuchElementException, TimeoutException):
                            try:
                                man_legal_person_address_0_caption = driver.find_element_by_css_selector('#address_element_manufacturer_info-rds-man_foreign_legal_person-address_0_caption').text
                            except (NoSuchElementException, TimeoutException):
                                man_legal_person_address_0_caption = ' '
                        # 'Номер телефона'
                        try:
                            man_legal_person_phones = driver.find_element_by_css_selector('#a_manufacturer_info-rds-man_legal_person-phone > .form-right-col')
                            array_field = man_legal_person_phones.find_elements_by_class_name('array-field')
                            man_legal_person_phones = ", ".join([elem.text for elem in array_field])
                        except (NoSuchElementException, TimeoutException):
                            man_legal_person_phones = ' '
                            try:
                                man_legal_person_phones = driver.find_element_by_css_selector('#a_manufacturer_info-rds-man_foreign_legal_person-phone > .form-right-col')
                                array_field = man_legal_person_phones.find_elements_by_class_name('array-field')
                                man_legal_person_phones = ", ".join([elem.text for elem in array_field])
                            except (NoSuchElementException, TimeoutException):
                                man_legal_person_phones = ' '
                        # 'Адрес электронной почты',
                        try:
                            man_legal_person_emails = driver.find_element_by_css_selector('#a_manufacturer_info-rds-man_legal_person-email > .form-right-col')
                            array_field = man_legal_person_emails.find_elements_by_class_name('array-field')
                            man_legal_person_emails = ", ".join([elem.text for elem in array_field])
                        except (NoSuchElementException, TimeoutException):
                            try:
                                man_legal_person_emails = driver.find_element_by_css_selector('#a_manufacturer_info-rds-man_foreign_legal_person-email > .form-right-col')
                                array_field = man_legal_person_emails.find_elements_by_class_name('array-field')
                                man_legal_person_emails = ", ".join([elem.text for elem in array_field])
                            except (NoSuchElementException, TimeoutException):
                                man_legal_person_emails = ' '
                        ### 'Сведения о продукции'
                        #     '«Тип объекта сертификации»: серийный выпуск, партия, единичное изделие'
                        try:
                            product_ts_object_type_cert  = driver.find_element_by_css_selector('#a_product_info-rds-product_ts-object_type_cert  > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            product_ts_object_type_cert = ' '
                        #     'Вид продукции'
                        try:
                            product_ts_product_type  = driver.find_element_by_css_selector('#a_product_info-rds-product_ts-product_type  > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            product_ts_product_type = ' '
                        #     'Полное наименование продукции'
                        try:
                            product_ts_product_name  = driver.find_element_by_css_selector('#a_product_info-rds-product_ts-product_name  > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            product_ts_product_name = ' '
                        #     'Сведения о продукции (тип, марка, модель, сорт, артикул и др.), обеспечивающие ее идентификацию'
                        try:
                            product_ts_product_info  = driver.find_element_by_css_selector('#a_product_info-rds-product_ts-product_info  > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            product_ts_product_info = ' '
                        #     'Код ТН ВЭД ЕАЭС'
                        try:
                            product_ts_tn_veds = driver.find_element_by_css_selector('#a_product_info-rds-product_ts-tn_ved > .form-right-col')
                            array_field = product_ts_tn_veds.find_elements_by_class_name('array-field')
                            product_ts_tn_veds = ", ".join([elem.text for elem in array_field])
                        except (NoSuchElementException, TimeoutException):
                            product_ts_tn_veds = ' '
                        ### Технический регламент
                        try:
                            product_ts_prod_doc_issued = driver.find_element_by_css_selector('#a_product_info-rds-product_ts-prod_doc_issued')
                            object_value = product_ts_prod_doc_issued.find_elements_by_css_selector('.object-value .form-right-col')
                            product_ts_prod_doc_issued = [elem.text for elem in object_value]
                        except (NoSuchElementException, TimeoutException):
                            product_ts_prod_doc_issued = ' '
                        #     'Технический регламент'
                        try:
                            product_ts_prod_doc_issued_0 = product_ts_prod_doc_issued[0]
                        except IndexError:
                            product_ts_prod_doc_issued_0 = ' '
                        #     'Технический регламент'
                        try:
                            product_ts_prod_doc_issued_1 = product_ts_prod_doc_issued[1]
                        except IndexError:
                            product_ts_prod_doc_issued_1 = ' '
                        #     'Технический регламент'
                        try:
                            product_ts_prod_doc_issued_2 = product_ts_prod_doc_issued[2]
                        except IndexError:
                            product_ts_prod_doc_issued_2 = ' '
                        ###     'Сведения об органе по сертификации'
                        #     'Полное наименование'
                        try:
                            organ_to_certification_name  = driver.find_element_by_css_selector('#a_organ_to_certification-rds-organ_to_certification-name  > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            organ_to_certification_name = ' '
                        #     'Номер аттестата'
                        try:
                            organ_to_certification_reg_number  = driver.find_element_by_css_selector('#a_organ_to_certification-rds-organ_to_certification-reg_number  > .form-right-col').text
                        except (NoSuchElementException, TimeoutException):
                            organ_to_certification_reg_number = ' '

                        csv_writer.writerow([
                            ' ',
                            a_reg_number.replace('|', ''),
                            a_date_begin.replace('|', ''),
                            a_date_finish.replace('|', ''),
                            ' ',
                            applicant_type.replace('|', ''),
                            legal_person_name.replace('|', ''),
                            app_legal_person_address.replace('|', ''),
                            app_legal_person_address_actual.replace('|', ''),
                            app_legal_person_phones.replace('|', ''),
                            app_legal_person_emails.replace('|', ''),
                            app_legal_person_ogrn.replace('|', ''),
                            ' ',
                            man_legal_person_name.replace('|', ''),
                            man_legal_person_address_0_caption.replace('|', ''),
                            man_legal_person_phones.replace('|', ''),
                            man_legal_person_emails.replace('|', ''),
                            ' ',
                            product_ts_object_type_cert.replace('|', ''),
                            product_ts_product_type.replace('|', ''),
                            product_ts_product_name.replace('|', ''),
                            product_ts_product_info.replace('|', ''),
                            product_ts_tn_veds.replace('|', ''),
                            product_ts_prod_doc_issued_0.replace('|', ''),
                            product_ts_prod_doc_issued_1.replace('|', ''),
                            product_ts_prod_doc_issued_2.replace('|', ''),
                            ' ',
                            organ_to_certification_name.replace('|', ''),
                            organ_to_certification_reg_number.replace('|', ''),
                            page_url.replace('|', ''),
                        ])

                    except (NoSuchElementException, TimeoutException):
                        print('Page stalled')
                        continue
                        ### explicit wait of element
                        # a_reg_number = common_wait.until(
                        #     EC.presence_of_element_located((By.CSS_SELECTOR, '#a_reg_number > .form-right-col'))
                        # ).text

        except Exception as e:
            self.logger.exception(str(e))
        finally:
            driver.quit()


if __name__ == '__main__':
    unittest.main()
