import os

ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'log.log')


def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(msg)


def sql(*args):
    query = args[0]
    log(query)
    # log(args[0] + '(' + ','.join(args[1:]) + ')')
