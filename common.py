from time import gmtime, strftime, sleep
from random import randint


def output_timed_message(message=''):
    print(strftime("%Y-%m-%d %H:%M:%S " + message, gmtime()))
    return


def wait():
    secs = 1 + randint(0, 4)
    sleep(secs)
    return
