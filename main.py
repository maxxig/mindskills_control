import time
from db import db
from webdriver import webdriver
import config

driver = webdriver.create_web_driver()
cnfg = config.get_config()

danya, danya_previous, alina, alina_previous = dict(), dict(), dict(), dict()

from datetime import date

print(date.today())

while(1):
    danya_info = db.get_previous_total_task_count(1)
    if not danya:
        danya_previous['total_cnt'] = danya_info[1]
    danya_limit = danya_info[0]
    cnt_complited_tasks_today = db.get_count_tasks_today(1)

    # получаем количество решенных за сегодня, если danya_previous нул, если в бд за сегодня тоже нет - 0
    danya = webdriver.get_current_student_tasks(driver, cnfg['login_danya'], cnfg['password_danya'], cnfg['course_class_id_danya'])

    if danya.get('total_cnt') == 0:
        # у дани нет заданий  - сразу отправляем панику - после 8 утра
        pass
    if danya.get('total_cnt') > 0 and cnt_complited_tasks_today == 0:
        # задания есть, ничего не решал - напомнить после 20.00
        pass
    if danya.get('total_cnt') < danya_previous.get('total_cnt'):
        db.update_today_stat(1, cnt_complited_tasks_today + (danya_previous.get('total_cnt') - danya.get('total_cnt')))
        db.update_user_tasks_stock(1,danya.get('total_cnt'))

    elif danya.get('total_cnt') > danya_previous.get('total_cnt'):
        db.update_user_tasks_stock(1,danya.get('total_cnt'))


    # alina_previous = alina.copy()
    # alina = get_current_student_tasks(cnfg['login_alina'], cnfg['password_alina'], cnfg['course_class_id_alina'])
    # if alina.get('total_cnt') != alina_previous.get('total_cnt'):
    #     print(alina_previous)
    #     print(alina)
    # else:
    #     print('Алина не решала')
    time.sleep(10)