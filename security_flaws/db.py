from security_flaws.app import app, g
import sqlite3
import os
import typing
import security_flaws.user as user
import security_flaws.note as note
import security_flaws.log as log

# the root dir is one directory above the current directory
ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
DB_NAME = 'db.sqlite'
DATABASE_PATH = os.path.join(ROOT_DIR, DB_NAME)
# sql definitions are in the 'sql' directory
SQL_PATH = os.path.join(ROOT_DIR, 'sql')


def get_db():
    """
    get a per-request connection to the db
    :return: an sqlite3 db connection
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = _init_db()
        g._database = db
    return db


def _init_db():
    # obtain a connection to the database
    db = sqlite3.connect(DATABASE_PATH)
    # as in the docs, this gives us dicts back instead of tuples
    db.row_factory = sqlite3.Row
    return db


def close_connection():
    """
    close this request's connection
    :return: None
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def execute_sql(sql_path, db):
    """
    execute the contents of a script in the parent sql directory

    :param sql_path: the path to the sql script
    :param db: the database connection to use
    :return: None
    """
    with open(os.path.join(SQL_PATH, sql_path), 'r') as f:
        sql = f.read()
        db.executescript(sql)


def create_schema(db):
    """
    create the schema for the database by running the create table script
    :return: None
    """
    execute_sql('create_tables.sql', db)


def insert_fixtures(db):
    """
    insert example data for testing
    :return: None
    """
    execute_sql('insert_fixtures.sql', db)


def insert_into_db(query: str, args=()) -> int:
    """
    perform an INSERT query on the database

    like query_db but it commits and returns the last inserted row id
    :param query: the sql query to run
    :param args: arguments to be used as bound parameters
    :return: the last inserted row id
    """
    connection = get_db()
    log.sql(query)
    cursor = connection.execute(query, args)
    connection.commit()
    cursor.close()
    return cursor.lastrowid


def query_db(query: str, args=(), one=False):
    """
    run an sql query against the database
    
    :param query: the sql query to run 
    :param args: arguments to be used as bound parameters
    :param one: only return one result?
    :return: result[s] from the db, or None if the query did not receive any results
    """
    cursor = get_db().execute(query, args)
    log.sql(query, args)
    result = cursor.fetchall()
    cursor.close()
    if result is None:
        return None
    if one is True:
        if len(result) > 0:
            return result[0]
        return None
    return result


def get_user_count() -> int:
    """
    get a count of the users currently in the db
    :return: an integer count of the number of users
    """
    result = query_db('select count(*) as c from users;', one=True)
    return int(result['c'])


def find_user_by_username(username: str) -> typing.Optional[user.User]:
    """
    given a username, see if they exist in the database. if they do,
    return a User object representing this user. otherwise return None
    :param username: the username to search for
    :return: None if the username does not exist, a User object if they do
    """
    sql = 'select * from users where username=?'
    result = query_db(query=sql, one=True, args=[username])
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


def save_user(user_to_save: user.User) -> user.User:
    """
    save a User object to the database
    :param user_to_save: the User object to serialize and commit
    :return: a User object representing the saved user
    """
    sql = 'INSERT INTO `users` (`username`, `secret`) VALUES (?, ?);'
    last_id = insert_into_db(sql, [user_to_save.username, user_to_save.secret])
    saved_user = user.create_user(
        user_to_save.username,
        user_to_save.secret
    )
    saved_user.id = last_id
    return saved_user


def save_user_in_a_very_unsafe_way(user_to_save: user.User) -> user.User:
    """
    save a User object to the database
    :param user_to_save: the User object to serialize and commit
    :return: a User object representing the saved user
    """
    # we put the user-provided data straight into the sql statement
    sql = "INSERT INTO `users` (`username`, `secret`) VALUES ('{0}', '{1}');".format(
        user_to_save.username, user_to_save.secret
    )
    log.sql(sql)

    connection = get_db()
    # executescript allows us to run more than one command at once
    cursor = connection.executescript(sql)
    # get the last inserted id
    last_insert_row = query_db('SELECT last_insert_rowid() AS id', one=True)
    last_insert_row_id = last_insert_row['id']
    connection.commit()
    cursor.close()

    saved_user = user.create_user(
        user_to_save.username,
        user_to_save.secret
    )
    saved_user.id = last_insert_row_id
    return saved_user


def save_note(note_to_save: note.Note) -> note.Note:
    """
    save a new note
    :param note_to_save: a Note object to save
    :return: a Note object representing the saved note
    """
    sql = 'INSERT INTO `notes` (`from_user_id`, `from_username`, `to_user_id`, `note`) VALUES (?, ?, ?, ?);'
    last_id = insert_into_db(
        sql, [note_to_save.from_user.id,
              note_to_save.from_user.username,
              note_to_save.to_user.id,
              note_to_save.note]
    )

    saved_note = note_to_save
    saved_note.id = last_id
    return saved_note


def find_notes_sent_to_user_id(user_id: int) -> [str]:
    """
    find all notes where the to user has the given username
    :param user_id: the id of the user to search
    :return: a list of dicts of (note, from_username) pairs
    """
    sql = 'SELECT `note`, `from_username` FROM `notes` WHERE to_user_id=? ORDER BY `id` DESC'
    result = query_db(query=sql, args=[user_id])
    if result is None:
        return []
    notes = []
    for row in result:
        notes.append({'note': row['note'], 'from_username': row['from_username']})
    return notes


def auth(username: str, secret: str) -> bool:
    """
    check if a given username / secret matches what is in the database
    :param username:
    :param secret:
    :return: true on success false on failure
    """
    sql = 'SELECT COUNT(*) as c FROM users WHERE username=? AND secret=?'
    result = query_db(sql, one=True, args=[username, secret])
    return result['c'] == 1
