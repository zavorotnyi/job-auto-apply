from bs4 import BeautifulSoup
from urllib.request import urlopen
from sqlite3 import connect

from settings import url_login, user_login, user_password, db_karriereat, q_select, q_insert
from common import output_timed_message, wait


def get_new_jobs(url):
    # Connection to database and extraction of processed jobs
    conn = connect(db_karriereat)
    conn.row_factory = lambda cursor, row: str(row[0])
    c = conn.cursor()
    ids = c.execute(q_select).fetchall()

    # Parsing of new jobs from url
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    jobs = soup.findAll('div', {"class": "m-jobItem "})
    new_jobs = []
    for job in jobs:
        # Check if already processed
        if job.attrs['data-id'] not in ids:
            city = job.findAll('a', {'class': "m-jobItem__locationLink"})[0].contents[0]
            company = job.findAll('a', {'class': "m-jobItem__company"})[0].contents[0]
            date = job.findAll('span', {'class': "m-jobItem__date"})[0].contents[0].split()[1]
            info = job.findAll('p', {'class': "m-jobItem__snippet"})[0].contents[0]
            name = job.findAll('a', {'class': "m-jobItem__titleLink"})[0].contents[0]
            link = job.findAll('a', {'class': "m-jobItem__titleLink"})[0].attrs['href']
            c.execute(q_insert, (job.attrs['data-id'], city, name, company, date, info))
            new_jobs.append({'id': job.attrs['data-id'], 'link': link, 'name': name})
    # Commit changes if there are any
    if len(new_jobs) > 0:
        conn.commit()
    conn.close()
    return new_jobs


def login(browser):
    # Login to karriere.at
    try:
        browser.get(url_login)
        wait()
        browser.find_element_by_id('email').send_keys(user_login)
        wait()
        browser.find_element_by_id('password').send_keys(user_password)
        browser.find_elements_by_class_name("m-userLogin__submitButton")[0].click()
        wait()
        if len(browser.find_elements_by_id('email')) > 0:
            output_timed_message('ERROR: Wrong login/password')
            return 0
        return 1
    except:
        output_timed_message('ERROR: Login error')
        return 0


def apply_job(browser, job_page):
    # Open job page and send application
    try:
        wait()
        browser.get(job_page)
        wait()
        browser.find_elements_by_class_name("m-applyButton__button")[0].click()
        wait()
        browser.find_elements_by_class_name("c-applyForm__action")[0].click()
        return 1
    except:
        output_timed_message('ERROR: Applying error')
        return 0
