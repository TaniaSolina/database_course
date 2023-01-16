from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from view import View


user = 'postgres'
password = 'S0l1na'
host = 'localhost'
port = 5432
database = 'cinema'


Base = declarative_base()


def get_engine():
    return create_engine(url=f"postgresql://{user}:{password}@{host}:{port}/{database}")


def connect():
    try:
        _engine = get_engine()
        Base.metadata.create_all(_engine)
        print(f"Connection to the {host} for user {user} created successfully.")
        return sessionmaker(bind=_engine)()
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)


session = connect()


class FilmGenres(Base):
    __tablename__ = 'film_genres'
    film_id = Column(Integer, ForeignKey('films.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)

    def __init__(self, film_id, genre_id):
        self.film_id = film_id
        self.genre_id = genre_id
        super(FilmGenres, self).__init__()


class Films(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    producer = Column(String)
    release_year = Column(Integer)
    duration = Column(Integer)

    def __init__(self, id, title, producer, release_year, duration):
        self.id = id
        self.title = title
        self.producer = producer
        self.release_year = release_year
        self.duration = duration
        super(Films, self).__init__()


class Genres(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name
        super(Genres, self).__init__()


class Halls(Base):
    __tablename__ = 'halls'
    id = Column(Integer, primary_key=True)
    technology_id = Column(Integer, ForeignKey('technologies.id'))

    def __init__(self, id, technology_id):
        self.id = id
        self.technology_id = technology_id
        super(Halls, self).__init__()


class Prices(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    technology_id = Column(Integer, ForeignKey('technologies.id'))
    price = Column(Integer)

    def __init__(self, id, technology_id, price):
        self.id = id
        self.technology_id = technology_id
        self.price = price
        super(Prices, self).__init__()


class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    hall_id = Column(Integer, ForeignKey('halls.id'))
    film_id = Column(Integer, ForeignKey('films.id'))
    date_time = Column(String)

    def __init__(self, id, hall_id, film_id, date_time):
        self.id = id
        self.hall_id = hall_id
        self.film_id = film_id
        self.date_time = date_time
        super(Session, self).__init__()


class SoldTickets(Base):
    __tablename__ = 'sold_tickets'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'))
    place = Column(Integer)
    row = Column(Integer)

    def __init__(self, id, session_id, place, row):
        self.id = id
        self.session_id = session_id
        self.place = place
        self.row = row
        super(SoldTickets, self).__init__()


class Technologies(Base):
    __tablename__ = 'technologies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        super(Technologies, self).__init__()


tables = {
    1: FilmGenres,
    2: Films,
    3: Genres,
    4: Halls,
    5: Prices,
    6: Session,
    7: SoldTickets,
    8: Technologies,
}


def get_table_data(table):
    return [tuple(getattr(item, col.name) for col in item.__table__.columns)
            for item in session.query(table).all()]


def get_column_names(table):
    row = session.query(table).first()
    return [col for col in row.__table__.columns.keys()]


def get_row_id(table):
    if table is FilmGenres:
        return table.film_id
    return table.id


def get_range(id_range_to_delete):
    # begin == first value, end == second value (if it exists)
    # if there is no second value end == begin
    begin, end = id_range_to_delete[0], id_range_to_delete[-(len(id_range_to_delete) - 1)] + 1
    return range(begin, end)


def select_table(table_num):
    table = tables[table_num]
    column_names = get_column_names(table)
    data = get_table_data(table)
    View.table_parser(tables[table_num].__tablename__, column_names, data)


def select_all_tables():
    for table_num in range(1, 9):
        select_table(table_num)


def insert_into_table(table_num, data=()):
    column_names = get_column_names(tables[table_num])
    if not data:
        data = View.input_data(column_names)
    session.add(tables[table_num](*data))


def update_table(data, table_num):
    id_ = data[0]
    table = tables[table_num]
    row = session.query(table).filter(get_row_id(table) == int(id_)).first()

    for column, value in zip(get_column_names(table), data):
        row.__setattr__(column, value)
    session.commit()


def delete_data(table_num, id_range):
    table = tables[table_num]
    for _id in get_range(id_range):
        row = session.query(table).filter(get_row_id(table) == int(_id)).first()
        if row:
            session.delete(row)
            session.commit()
