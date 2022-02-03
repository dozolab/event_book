from sqlalchemy import create_engine, MetaData

from event_book.db import person, event, coupon
# from aiohttpdemo_polls.settings import BASE_DIR, get_config
import os


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
database_db = os.environ['DATABASE_DB']
database_user = os.environ['DATABASE_USER']
database_password = os.environ['DATABASE_PASS']
database_host = os.environ['DATABASE_HOST']
database_port = os.environ['DATABASE_PORT']

ADMIN_DB_URL = DSN.format(
    user=os.environ['DATABASE_USER'],
    password=os.environ['DATABASE_PASS'],
    database=os.environ['DATABASE_DB'],
    host=os.environ['DATABASE_HOST'],
    port=os.environ['DATABASE_PORT']
)
admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')


# USER_CONFIG_PATH = BASE_DIR / 'config' / 'polls.yaml'
# USER_CONFIG = get_config(['-c', USER_CONFIG_PATH.as_posix()])
# USER_DB_URL = DSN.format(**os.environ['DATABASE_DB'])
# user_engine = create_engine(USER_DB_URL)
#
# TEST_CONFIG_PATH = BASE_DIR / 'config' / 'polls_test.yaml'
# TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
# TEST_DB_URL = DSN.format()
# test_engine = create_engine(TEST_DB_URL)


def setup_db():
    db_name = database_db
    db_user = database_user
    db_pass = database_password

    conn = admin_engine.connect()
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
    conn.execute("CREATE DATABASE %s ENCODING 'UTF8'" % db_name)
    conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                 (db_name, db_user))
    conn.close()


# def teardown_db(config):
#
#     db_name = database_db
#     db_user = database_user
#
#     conn = admin_engine.connect()
#     conn.execute("""
#       SELECT pg_terminate_backend(pg_stat_activity.pid)
#       FROM pg_stat_activity
#       WHERE pg_stat_activity.datname = '%s'
#         AND pid <> pg_backend_pid();""" % db_name)
#     conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
#     conn.execute("DROP ROLE IF EXISTS %s" % db_user)
#     conn.close()


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[person, event, coupon])


def drop_tables(engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[person, event, coupon])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(person.insert(), [
        {'name': 'Ozodbek',
         'surname': 'Ulashov',
         'token': 'asdfasdfasdf',
         },
        {'name': 'Bekzod',
         'surname': 'Aliev',
         'token': 'asdfasdfasdf',
         },
        {'name': 'Person 3',
         'surname': 'Person3 Sourname',
         'token': 'asdfasdfasdf',
         },
        {'name': 'Person 4',
         'surname': 'Person 4 Sourname',
         'token': 'asdfasdfasdf',
         },
    ])
    conn.execute(event.insert(), [
        {'remain': 'Not much', 'title': "Event 1", 'description': "asdfsdffasdf", 'price': 200,
         'date': '2015-12-15 17:17:49.629+02'},
        {'remain': 'Not much', 'title': "Event 2", 'description': "asdfsdffasdf", 'price': 200,
         'date': '2015-12-15 17:17:49.629+02'},
        {'remain': 'Not much', 'title': "Event 3", 'description': "asdfsdffasdf", 'price': 200,
         'date': '2015-12-15 17:17:49.629+02'},
        {'remain': 'Not much', 'title': "Event 4", 'description': "asdfsdffasdf", 'price': 200,
         'date': '2015-12-15 17:17:49.629+02'},
        {'remain': 'Not much', 'title': "Event 5", 'description': "asdfsdffasdf", 'price': 200,
         'date': '2015-12-15 17:17:49.629+02'}


    ])
    try:
        conn.execute(coupon.insert(), [
            {'person_id': 1, 'event_id': 2, 'hash': "asdfasf"},
            {'person_id': 1, 'event_id': 1, 'hash': "asdfasf"},
            {'person_id': 1, 'event_id': 3, 'hash': "asdfasf"},
            {'person_id': 1, 'event_id': 4, 'hash': "asdfasf"},
            {'person_id': 1, 'event_id': 5, 'hash': "asdfasf"},
            {'person_id': 2, 'event_id': 2, 'hash': "asdfasf"},
            {'person_id': 3, 'event_id': 2, 'hash': "asdfasf"},
            {'person_id': 3, 'event_id': 3, 'hash': "asdfasf"},
            {'person_id': 3, 'event_id': 4, 'hash': "asdfasf"},
            {'person_id': 3, 'event_id': 5, 'hash': "asdfasf"},
            {'person_id': 4, 'event_id': 2, 'hash': "asdfasf"},
            {'person_id': 4, 'event_id': 3, 'hash': "asdfasf"},
            {'person_id': 4, 'event_id': 4, 'hash': "asdfasf"}
        ])
    except Exception as e:
        print()
    conn.close()


if __name__ == '__main__':
    # setup_db()
    create_tables(engine=admin_engine)
    sample_data(engine=admin_engine)
