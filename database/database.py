"""
This python script holds the database instance and the models used in the
database for data persistence
"""
import os.path
from datetime import date

from sqlalchemy import Float, Integer, Date, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DBConnection(object):
    """
    This class just holds the DBConnection. For now, it is a disk based database interacted with SQLAlchemy ORM.
    This class will allow for the developer to easily add another database connection type in the future.
    SQLAlchemy supports other databases sucha as SQLite, Postgresql, MySQL, MariaDB, Oracle, and MS-SQL
    """
    DB_FILENAME = 'personalWellness.db'

    def get_sqlalchemy_sqlite_connection(self):
        return "sqlite:///database/" + self.DB_FILENAME

    def get_sqlalchemy_engine(self):
        return create_engine(self.get_sqlalchemy_sqlite_connection(), echo=True)


class Base(DeclarativeBase):
    """
        The Base class inherits the DeclarativeBase class from the SQLAlchemy library to be used for ORM
    """
    pass


class Finance(Base):
    """
        The Finance class is a descriptor for the Finance object that the application will be using
        The Finance class defines the python and SQL data types to be mapped.
    """
    __tablename__ = "finance"

    income: Mapped[float] = mapped_column(Float)
    grocery_expense: Mapped[float] = mapped_column(Float)
    utility_expense: Mapped[float] = mapped_column(Float)
    rent: Mapped[float] = mapped_column(Float)
    food_expense: Mapped[float] = mapped_column(Float)
    misc_expense: Mapped[float] = mapped_column(Float)
    log_date: Mapped[date] = mapped_column(Date, primary_key=True)

    def __repr__(self) -> str:
        return (f"Finance(income={self.income}, grocery={self.grocery_expense} "
                f"utility={self.utility_expense}, rent={self.rent}, food={self.food_expense}"
                f" misc={self.misc_expense} log_date={self.log_date})")


class Mindfulness(Base):
    """
    The Mindfulness class is a descriptor for the Mindfulness object that the application will be using
    The Mindfulness class defines the python and SQL data types to be mapped
    """
    __tablename__ = "mindfulness"

    user_mood: Mapped[str] = mapped_column(String)
    log_date: Mapped[date] = mapped_column(Date, primary_key=True)

    def __repr__(self):
        return f"Mindfulness(user_mood={self.user_mood}, log_date={self.log_date})"


class Journal(Base):
    """
        The Journal class is a descriptor for the Mindfulness object that the application will be using
        The Journal class defines the python and SQL data types to be mapped
        """
    __tablename__ = "journal"

    journal_entry: Mapped[str] = mapped_column(String)
    journal_title: Mapped[str] = mapped_column(String)
    journal_date: Mapped[date] = mapped_column(Date, primary_key=True)

    def __repr__(self):
        return f"Journal(entry={self.journal_entry}, title={self.journal_title}, date={self.journal_date})"


def create_all_tables():
    """
    This function creates all tables
    :return:
    """
    conn = DBConnection()
    if os.path.exists(conn.DB_FILENAME):
        os.remove(conn.DB_FILENAME)
    engine = conn.get_sqlalchemy_engine()
    Base.metadata.create_all(engine)
