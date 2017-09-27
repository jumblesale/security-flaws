import sqlite3
import os
import typing
import security_flaws.user as user

# the root dir is one directory above the current directory
ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
DB_NAME = 'db.sqlite'
DATABASE_PATH = os.path.join(ROOT_DIR, DB_NAME)
# sql definitions are in the 'sql' directory
SQL_PATH = os.path.join(ROOT_DIR, 'sql')

# obtain a connection to the database
db = sqlite3.connect(DATABASE_PATH)
# as in the docs, this gives us dicts back instead of tuples
db.row_factory = sqlite3.Row


def execute_sql(sql_path):
    """
    execute the contents of a script in the parent sql directory
    
    :param sql_path: the path to the sql script 
    :return: None 
    """
    with open(os.path.join(SQL_PATH, sql_path), 'r') as f:
        sql = f.read()
        db.executescript(sql)


def create_schema():
    """
    create the schema for the database by running the create table script
    :return: None
    """
    execute_sql('create_tables.sql')


def insert_fixtures():
    """
    insert example data for testing
    :return: None
    """
    execute_sql('insert_fixtures.sql')


def save_user(user_to_save: user.User):
    sql = '''
        INSERT INTO `users` (`username`, `secret`)
        VALUES ("{}", "{}");
    '''.format(user_to_save.username, user_to_save.secret)
    cursor = db.execute(sql)
    last_id = cursor.lastrowid
    saved_user = user.create_user(
        user_to_save.username,
        user_to_save.secret
    )
    saved_user.id = last_id
    return saved_user


def query_db(query, args=(), one=False):
    """
    run an sql query against the database
    
    :param query: the sql query to run 
    :param args: arguments to be used as bound parameters
    :param one: only return one result?
    :return: result[s] from the db, or None if the query did not receive any results
    """
    cursor = db.execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    if result is None:
        return None
    if one is True:
        return result[0]
    return result


def find_user_by_username(username: str) -> typing.Optional[user.User]:
    """
    given a username, see if they exist in the database. if they do,
    return a User object representing this user. otherwise return None
    :param username: the username to search for
    :return: None if the username does not exist, a User object if they do
    """
    sql = 'select * from users where username="{}"'.format(username)
    result = query_db(query=sql, one=True)
    if result is None:
        return None
    retrieved_user = user.create_user(result['username'], result['secret'])
    retrieved_user.id = result['id']
    return retrieved_user


def find_user_by_id(user_id: int) -> typing.Optional[user.User]:
    """
    given a username, see if they exist in the database. if they do,
    return a User object representing this user. otherwise return None
    :param id: the id of the user to search for
    :return: None if the username does not exist, a User object if they do
    """
    sql = 'select * from users where id=?'
    result = query_db(query=sql, one=True, args=[user_id])
    if result is None:
        return None
    retrieved_user = user.create_user(result['username'], result['secret'])
    retrieved_user.id = result['id']
    return retrieved_user


