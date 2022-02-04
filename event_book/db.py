import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date, Text, Float, UniqueConstraint
)
import os

__all__ = ['person', 'event', 'coupon']

meta = MetaData()

person = Table(
    'person', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
    Column('surname', String(200), nullable=False),
    Column('token', Text(), nullable=False)
)

event = Table(
    'event', meta,

    Column('id', Integer, primary_key=True),
    Column('remain', String(200), nullable=False),
    Column('title', String(200), nullable=False),
    Column('description', Text(), nullable=False),
    Column('price', Float(), nullable=False),
    Column('date', Date, nullable=False),
)

coupon = Table(
    'coupon', meta,

    Column('id', Integer, primary_key=True),
    Column('event_id',
           Integer,
           ForeignKey('event.id', ondelete='CASCADE')),
    Column('person_id',
           Integer,
           ForeignKey('person.id', ondelete='CASCADE')),
    Column('hash', Text(), nullable=False),
    UniqueConstraint('event_id', 'person_id', name='uix_1')

)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def pg_context(app):
    engine = await aiopg.sa.create_engine(
        database=os.environ['DATABASE_DB'],
        user=os.environ['DATABASE_USER'],
        password=os.environ['DATABASE_PASS'],
        host=os.environ['DATABASE_HOST'],
        port=os.environ['DATABASE_PORT'],
        minsize=1,
        maxsize=5,
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


async def get_person_list(conn):
    stmt = 'SELECT person.* , COUNT(coupon.id) as events_count from person , coupon where person.id=coupon.person_id group by person.id HAVING COUNT(coupon.id) > 3 ORDER BY events_count DESC '
    result = await conn.execute(stmt)
    question_record = await result.fetchall()
    return question_record


#
async def get_event_list(conn):
    result = await conn.execute(
        event.select())
    event_record = await result.fetchall()
    return event_record


async def get_coupon_list(conn):
    result = await conn.execute(
        coupon.select())
    event_record = await result.fetchall()
    return event_record
