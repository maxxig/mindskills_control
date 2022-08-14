from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import configparser,time, sqlite3
from datetime import date


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
def get_count_tasks_today(user_id = 1):
    conn = sqlite3.connect('mindskills_db.sqlite')
    current_date = date.today()
    data = conn.execute('select complited_tasks from users_complited_tasks where date = ? and user_id = ? LIMIT 1', (current_date, user_id))
    for d in data:
        res = d
    conn.close()
    return res[0]
def get_previous_total_task_count(user_id):
    conn = sqlite3.connect('mindskills_db.sqlite')
    data = conn.execute('select [limit], task_stock from users where id = ? LIMIT 1', [user_id])
    for d in data:
        res = d
    conn.close()
    return res
def update_today_stat(user_id, cnt):
    conn = sqlite3.connect('mindskills_db.sqlite')
    current_date = date.today()
    conn.execute('update users_complited_tasks set complited_tasks = ? where user_id = ? and date = ?', (cnt, user_id, current_date))
    conn.commit()
    conn.close()

while(1):
    danya_info = get_previous_total_task_count(1)
    if not danya:
        danya_previous['total_cnt'] = danya_info[1]
    danya_limit = danya_info[0]
    cnt_complited_tasks_today = get_count_tasks_today(1)
    # получаем количество решенных за сегодня, если danya_previous нул, если в бд за сегодня тоже нет - 0
    danya = get_current_student_tasks(cnfg['login_danya'], cnfg['password_danya'], cnfg['course_class_id_danya'])

    if danya.get('total_cnt') == 0:
        # у дани нет заданий  - сразу отправляем панику - после 8 утра
        pass
    if danya.get('total_cnt') > 0 and cnt_complited_tasks_today == 0:
        # задания есть, ничего не решал - напомнить после 20.00
        pass
    if danya.get('total_cnt') < danya_previous.get('total_cnt'):
        update_today_stat(1, cnt_complited_tasks_today + (danya_previous.get('total_cnt') - danya.get('total_cnt')))
        # даня порешал, обновим стату
        print(danya_previous)
        print(danya)
    elif danya.get('total_cnt') > danya_previous.get('total_cnt'):
        # добавили заданий, не понятно решал ли даня
        pass
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