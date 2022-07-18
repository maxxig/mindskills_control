from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('config.ini', encoding="utf-8")
cnfg = config['parameters']


driver = webdriver.Chrome('D:/_sources/python/mindskills_control/chromedriver_win32/chromedriver.exe')
driver.get('https://mindskills.online/profile/login/')


element_login  = driver.find_element(By.XPATH,"//input[contains(@name,'username')]")

element_login.send_keys(cnfg['login'])
element_pass  = driver.find_element(By.XPATH,"//input[contains(@name,'password')]")
element_pass.send_keys(cnfg['password'])
element_accept = driver.find_element(By.XPATH,'//button[@type="submit"]')
element_accept.click()

time.sleep(2)
driver.get('https://mindskills.online/students/task_list/')
# course_task_9676 - alina
tasks = driver.find_element(By.XPATH,"//div[contains(@class,'course_task_8016')]/ul")
Danya = dict()
total_cnt = 0

for i,s in enumerate(tasks.text.split('\n')):
    if i == 0:
        continue
    date = s[0:s.find(',')]
    cnt = int(s[s.find('(')+1:s.find(')')])
    Danya[date] = cnt
    total_cnt += cnt
Danya['total_cnt'] = total_cnt


print(Danya)