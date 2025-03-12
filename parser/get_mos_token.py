from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchCookieException, NoSuchElementException
from selenium_stealth import stealth
from fake_useragent import UserAgent
from dotenv import load_dotenv
import os

from configs import logger_mos

load_dotenv()
MOS_LOGIN = os.getenv('MOS_LOGIN')
MOS_PASSWORD = os.getenv('MOS_PASSWORD')

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Отключаем автоматизацию
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')

driver = webdriver.Chrome(options=chrome_options)

# библиотека, которой передается драйвер и он там что-то мутит для обмана детекторов бота
stealth(driver=driver,
            user_agent=user_agent.random,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=True
            )

# Что-то редактируют в коде драйвера, на что обращают внимание детекторы ботов
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
})

driver.implicitly_wait(10) # явное ожидание ответа от сервера в 10 секунд для всех команд драйвера

#TODO переименовать в get_mos_token

def get_token():
    """
    Получаем bearer token через авторизацию на mos.ru, используя selenium из-за js кода на страницу
    :return: bearer token
    """
    try:
        driver.get(
            'https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Ddnevnik.mos.ru%26scope%3Dopenid%2Bprofile%2Bbirthday%2Bcontacts%2Bsnils%2Bblitz_user_rights%2Bblitz_change_password%26redirect_uri%3Dhttps%3A%2F%2Fschool.mos.ru%2Fv3%2Fauth%2Fsudir%2Fcallback')
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login"))
        )

        logger_mos.info('login.mos.ru открыт')

        driver.find_element(By.ID, 'login').send_keys(MOS_LOGIN)
        driver.find_element(By.ID, 'password').send_keys(MOS_PASSWORD)
        driver.find_element(By.ID, 'bind').click()

        logger_mos.info('Выполняем вход')

        token = WebDriverWait(driver, 20).until(lambda x: x.get_cookie('aupd_token'))
        logger_mos.info('Bearer token получен!')

        driver.quit()
        return token['value']
    except (TimeoutException, WebDriverException, NoSuchCookieException, NoSuchElementException) as e:
        logger_mos.error(f'Ошибка при работе Selenium: {e}')
        return False



if __name__ == "__main__":
    print(get_token())


