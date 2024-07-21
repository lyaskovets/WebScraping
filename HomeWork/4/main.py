import requests
import re


def getdata():
    response = requests.get('https://www.lejobadequat.com/emplois')

    print(response.status_code)
    with open('response.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)

    pattern = r'<h3 class="jobCard_title">(.+)<\/h3>'
    job = re.findall(pattern, response.text)

    with open('joblist.txt', 'w', encoding='utf-8') as file:
        for j in job:
            file.write(j + '\n')
    print(job)


if __name__ == '__main__':
    getdata()
