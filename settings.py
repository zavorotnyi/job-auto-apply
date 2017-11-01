chromedriver_path = "D:/dev/chromedriver.exe"

url_login = 'https://www.karriere.at/user/login'
url_filter = 'https://www.karriere.at/jobs/python/wien?sort=date'
url_jobs = 'https://www.karriere.at/jobs/'
db_karriereat = 'karriereat'
# Queries for database
q_select = 'SELECT id FROM JOB'
q_insert = 'INSERT INTO JOB(ID, CITY, JOB_NAME, COMPANY, JOB_DATE, INFO) VALUES(?,?,?,?,?,?)'
q_update = 'UPDATE JOB SET SENT = ? WHERE ID = ?'

user_login = 'user_login'
user_password = 'user_password'
