import sqlite3
import datetime as DT
dbname = 'mindskills_db.sqlite'

def get_count_tasks_today(user_id = 1):
    conn = sqlite3.connect(dbname)
    data = conn.execute('select complited_tasks from users_complited_tasks where dt = ? and user_id = ? LIMIT 1', (DT.date.today(), user_id))
    res = ()
    for d in data:
        res = d
    conn.close()
    return res[0] if len(res)>0 else 0

def get_previous_total_task_count(user_id):
    conn = sqlite3.connect(dbname)
    data = conn.execute('select [limit], task_stock from users where id = ? LIMIT 1', [user_id])
    for d in data:
        res = d
    conn.close()
    return res
def update_today_stat(user_id, cnt):
    conn = sqlite3.connect(dbname)
    conn.execute('replace into users_complited_tasks (complited_tasks, user_id, dt) values (?,?,?)', (cnt, user_id, DT.date.today()))
    conn.commit()
    conn.close()
def update_user_tasks_stock(user_id, stock):
    conn = sqlite3.connect(dbname)
    conn.execute('update users set task_stock = ? where id = ?', (stock, user_id))
    conn.commit()
    conn.close()

def update_log(user_id, doc):
    conn = sqlite3.connect(dbname)
    conn.execute('replace into users_complited_tasks (complited_tasks, user_id, dt) values (?,?,?)', (cnt, user_id, DT.date.today()))
    conn.commit()
    conn.close()