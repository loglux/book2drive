from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
import time
from datetime import date, timedelta
import requests


class Driving():
    def __init__(self):
        self.options = Options()
        # https://tinyurl.com/3ndv9cpc
        self.url = "https://www.dvtaonlineni.gov.uk/public/changeDrivingTest_1CollectInfo.aspx"
        # https://tinyurl.com/57asc67s
        self.first_book = "https://www.dvtaonlineni.gov.uk/public/bookDrivingTest_1CollectInfo.aspx"
        self.sms = "https://platform.clickatell.com/messages/http/send?apiKey={}" \
                   "==&to={}&content="
        self.link = ""

    def start_chrome(self, headless=False):
        if headless:
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.headless = True
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        self.options.add_argument('--user-agent={}'.format(user_agent))
        self.chromepath = "chromedriver"
        self.driver = webdriver.Chrome(executable_path=self.chromepath, options=self.options)

    def get_page(self):
        self.driver.get(self.link)
        time.sleep(1)

    # depricated:
    def post_data(self, reference, licence, birth):
        self.link = self.url
        try:
            self.driver.find_element_by_name("slotBookingRef").send_keys(reference)
            self.driver.find_element_by_name("BSP_Driver_DriverNo").send_keys(licence)
            self.driver.find_element_by_name("BSP_Driver_DateOfBirth").send_keys(birth)
            time.sleep(2)
            self.driver.find_element_by_id("nextButton").click()
        except NoSuchElementException:
            exit()

    def first_data(self, birth, licence, reference=None):
        try:
            if reference:
                self.link = self.url
                self.get_page()
                self.driver.find_element_by_name("slotBookingRef").send_keys(reference)
            else:
                self.link = self.first_book
                self.get_page()
                self.driver.find_element_by_id("BSP_DriverTestCategory_ID_option0").click()
                self.driver.find_element_by_id("drvSpecialRequirements_option0").click()
            self.driver.find_element_by_name("BSP_Driver_DriverNo").send_keys(licence)
            self.driver.find_element_by_name("BSP_Driver_DateOfBirth").send_keys(birth)
            time.sleep(3)
            self.driver.find_element_by_id("nextButton").click()
        except NoSuchElementException:
            exit()

    def get_centre(self, location = 0):
        select = Select(self.driver.find_element_by_id("slotTestCentre"))
        centre = ["DILL ROAD, BELFAST", "BALMORAL, BELFAST", "NEWTOWNARDS", "LARNE",
                  "LISBURN", "BALLYMENA", "DOWNPATRICK", "ALTNAGELVIN, LONDONDERRY",
                  "ARMAGH", "COLERAINE", "COOKSTOWN", "CRAIGAVON", "ENNISKILLEN", "NEWRY", "OMAGH"]
        print(centre[location])
        select.select_by_visible_text(centre[location])

    def get_date(self, step=0):
        today = date.today()
        tomorrow = today + timedelta(days=1) + timedelta(days=32) * step
        month_ahead = tomorrow + timedelta(days=31)
        print("From {} To {}".format(tomorrow.strftime("%d-%B-%G"), month_ahead.strftime("%d-%B-%G")))
        start_day = str(tomorrow.day)
        start_month = str(tomorrow.month).lstrip("0")
        end_day = str(month_ahead.day)
        end_month = str(month_ahead.month).lstrip("0")
        select = Select(self.driver.find_element_by_id("slotSearchStartDate_day"))
        select.select_by_value(start_day)
        select = Select(self.driver.find_element_by_id("slotSearchStartDate_month"))
        select.select_by_value(start_month)
        select = Select(self.driver.find_element_by_id("slotSearchEndDate_day"))
        select.select_by_value(end_day)
        select = Select(self.driver.find_element_by_id("slotSearchEndDate_month"))
        select.select_by_value(end_month)
        time.sleep(1)
        self.driver.find_element_by_id("nextButton").click()

    def get_back(self):
        self.driver.find_element_by_id("prevButton").click()

    def get_exit(self):
        self.driver.quit()

    def get_info(self):
        try:
            time.sleep(1)
            text = self.driver.find_element_by_class_name("slotListDiv").text
            text = text.split('\n')
            header = text[0].strip()
            del text[0]
            print(header)
            print(text)
            return text
        except UnexpectedAlertPresentException as e:
            print(e.alert_text)
            exit()

    def send_sms(self, text):
        api_key = ""
        mobile = ""
        sms = requests.get(
            self.sms.format(api_key, mobile) + "Available+in+{}+starting+from+{}+{}".format(text[0], text[2], text[3])
            + "+{}".format(self.link))
        print(sms.text)

    def get_notice(self):
        send = self.get_info()
        if len(send) > 1:
            self.send_sms(send)
            exit()

    def get_table(self):
        table = self.driver.find_element_by_tag_name("tr").text
        print(table)


if __name__ == '__main__':
    reference = 1234567890
    licence = 1234567890
    birth = "dd/mm/yyyy"
    dva = Driving()
    # True for headless mode:
    dva.start_chrome(False)
    dva.first_data(birth, licence, reference)
    num = 5
    step = 0
    for n in range(num):
        dva.get_centre(location=n)
        dva.get_date(step)
        dva.get_notice()
        time.sleep(5)
        if n < num - 1:
            dva.get_back()
    # uncomment for headless mode:
    #dva.get_exit()

