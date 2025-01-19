from sqlalchemy import create_engine, BLOB, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Articles(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    body = Column(String)
    author = Column(String)
    published = Column(Date)
    link = Column(String)


class FAQ(Base):
    __tablename__ = 'faq'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    question = Column(String)
    answers = Column(String)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    address = Column(String, unique=True, nullable=False)
    notes = Column(String)
    receipts = relationship("SalesReceipt", backref="client")


class Protocols(Base):
    __tablename__ = 'protocols'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    protcol = Column(String)
    date = Column(Date)


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String)
    details = Column(String)
    price = Column(Float)


class ProductSales(Base):
    __tablename__ = 'product_sales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey('sales_receipts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer)
    price = Column(Float)


class SalesReceipt(Base):
    __tablename__ = 'sales_receipts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    date = Column(Date, nullable=False)
    total_amount = Column(Float)
    tax_amount = Column(Float)
    payment_method = Column(String)
    description = Column(String)
    receipt_image = Column(BLOB)
    category = Column(String)
    notes = Column(String)
    products = relationship("ProductSales", backref="receipt")


class Vendors(Base):
    __tablename__ = 'vendors'

    id = Column(Integer, unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)
    contact_person = Column(String)
    contact_number = Column(String)
    email = Column(String)
    notes = Column(String)


class PurchaseReceipts(Base):
    __tablename__ = 'purchase_receipts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    date = Column(Date, nullable=False)
    total_amount = Column(Float)
    tax_amount = Column(Float)
    payment_method = Column(String)
    description = Column(String)
    receipt_image = Column(BLOB)
    category = Column(String)
    notes = Column(String)


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
