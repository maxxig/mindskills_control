from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import configparser
import time

#create webdriver
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#get config
config = configparser.ConfigParser()
config.sections()
config.read('config.ini', encoding="utf-8")
cnfg = config['parameters']
danya, danya_previous, alina, alina_previous = dict(), dict(), dict(), dict()


def get_current_student_tasks(login, password, course_id):
    res_dict = dict()
    driver.get('https://mindskills.online/profile/login/')
    element_login = driver.find_element(By.XPATH, "//input[contains(@name,'username')]")
    element_login.send_keys(login)

    element_pass = driver.find_element(By.XPATH, "//input[contains(@name,'password')]")
    element_pass.send_keys(password)

    element_accept = driver.find_element(By.XPATH, '//button[@type="submit"]')
    element_accept.click()

    time.sleep(2)
    driver.get('https://mindskills.online/students/task_list/')

    tasks = driver.find_element(By.XPATH, f"//div[contains(@class,'{course_id}')]/ul")
    total_cnt = 0

    for i, s in enumerate(tasks.text.split('\n')):
        if i == 0:
            continue
        date = s[0:s.find(',')]
        cnt = int(s[s.find('(') + 1:s.find(')')])
        res_dict[date] = cnt
        total_cnt += cnt
    res_dict['total_cnt'] = total_cnt
    return res_dict

while(1):
    danya_previous = danya.copy()
    danya = get_current_student_tasks(cnfg['login_danya'], cnfg['password_danya'], cnfg['course_class_id_danya'])
    if danya.get('total_cnt') != danya_previous.get('total_cnt'):
        print(danya_previous)
        print(danya)
    else:
        print('Даня не решал')
    alina_previous = alina.copy()
    alina = get_current_student_tasks(cnfg['login_alina'], cnfg['password_alina'], cnfg['course_class_id_alina'])
    if alina.get('total_cnt') != alina_previous.get('total_cnt'):
        print(alina_previous)
        print(alina)
    else:
        print('Алина не решала')
    time.sleep(10)