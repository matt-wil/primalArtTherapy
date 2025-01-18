from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    # phone_number = Column(Integer, unique=True, nullable=False)
    # address = Column(String, unique=True, nullable=False)
    # notes = Column(String, nullable=True)


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.__initialize_database()

    def __initialize_database(self):
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            raise RuntimeError(f"Database initialization failed: {e}")

    def add_client(self, name, email):
        session = self.Session()
        try:
            client = Client(name=name, email=email)
            session.add(client)
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Failed to add client: {e}")
        finally:
            session.close()

    def delete_client(self):
        pass

    def update_client(self):
        pass

    def get_client(self):
        pass

    def get_all_clients(self):
        session = self.Session()
        try:
            return session.query(Client).all()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch clients: {e}")
        finally:
            session.close()
