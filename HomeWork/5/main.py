import requests
import re
import json
import sqlite3


def getdata():
    response = requests.get('https://www.lejobadequat.com/emplois')

    with open('response.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)

    pattern = r'<a href="(http[^"]+)"[\W\w]*?<h3 class="jobCard_title">(.*)<\/h3>'
    jobs = re.findall(pattern, response.text)

    # export to JSON
    # =======================================================
    jobs_list = [{'title': j[1], 'url': j[0]} for j in jobs]
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(jobs_list, f, indent=4)

    # export to SQLite
    # =======================================================
    filename = 'jobs.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
        create table if not exists t_jobs (
            id integer primary key autoincrement,
            title text,
            url text
        )
    """
    cursor.execute(sql)

    for j in jobs:
        url, title = j
        cursor.execute('''insert into t_jobs (url, title)
                        values (?, ?)''', (url, title))

    conn.commit()
    conn.close()


def readSQLite():
    filename = 'jobs.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # 1. get all data
    sql = """
        select *
        from t_jobs
    """
    rows = cursor.execute(sql).fetchall()
    print(rows)

    conn.close()


if __name__ == '__main__':
    getdata()
    # readSQLite()
