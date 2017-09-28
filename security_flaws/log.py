import os

ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'log.log')


def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(msg + '\n')


def sql(*args):
    query = args[0]
    msg = '[SQL] ' + query
    if len(args) > 1:
        args_list = ','.join(args[1])
        msg += ' (' + args_list + ')'
    log(msg)
