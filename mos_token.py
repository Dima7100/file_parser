from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logging_config import logger_mos

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Отключаем автоматизацию
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Устанавливаем User-Agent
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)



def get_token():
    driver.get(
        'https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Ddnevnik.mos.ru%26scope%3Dopenid%2Bprofile%2Bbirthday%2Bcontacts%2Bsnils%2Bblitz_user_rights%2Bblitz_change_password%26redirect_uri%3Dhttps%3A%2F%2Fschool.mos.ru%2Fv3%2Fauth%2Fsudir%2Fcallback')
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login"))
    )

    logger_mos.info('login.mos.ru открыт')

    driver.find_element(By.ID, 'login').send_keys('pronindv')
    driver.find_element(By.ID, 'password').send_keys('Cuibai1!')
    driver.find_element(By.ID, 'bind').click()

    logger_mos.info('Выполняем вход')
    title = False
    #TODO изменить на ожидание получения куки.
    while not title:
        if driver.title == 'Московская электронная школа':
            title = True

    token = driver.get_cookie('aupd_token').get('value')
    logger_mos.info('Bearer token получен!')

    driver.quit()
    return token