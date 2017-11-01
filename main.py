from sqlite3 import connect
from selenium import webdriver
from time import sleep
from random import randint

import apply_karriereat
from settings import db_karriereat, url_filter, url_jobs, chromedriver_path, q_update
from common import output_timed_message

# main loop
while True:
    output_timed_message('Finding new jobs')

    # Getting new jobs from karriere.at
    new_jobs = apply_karriereat.get_new_jobs(url_filter)

    if len(new_jobs) > 0:
        # Starting Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--test-type')
        browser = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)

        # karriere.at applications
        logged = apply_karriereat.login(browser)
        if logged:
            conn = connect(db_karriereat)
            c = conn.cursor()
            for job in new_jobs:
                sent = apply_karriereat.apply_job(browser, url_jobs + job['id'])
                # Updating status of application
                c.execute(q_update, (sent, int(job['id'])))
                if sent:
                    output_timed_message('Sent: '+job['name'] + ' ' + job['link'])
                else:
                    output_timed_message('Could not send: ' + job['name'] + ' ' + job['link'])
            conn.commit()
            conn.close()
        browser.quit()

    else:
        output_timed_message('Nothing new')

    # half an hour sleep
    sleep(1800 + randint(-60, 60))
