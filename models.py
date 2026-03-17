from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from main import DATABASE_URL

# 1. Create connection to the database
db = create_engine(DATABASE_URL) 

# 2. Create a base class for our models
Base = declarative_base() 

# 3. Define our models/tables
class User(Base): 
    __tablename__ = "users" 
    id= Column("id", Integer, primary_key=True, autoincrement=True)
    name= Column("nome", String)
    email= Column("email", String, nullable=False)
    password= Column("password", String)
    active= Column("active", Boolean)
    admin= Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class Order(Base):
    __tablename__ = "orders"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) 
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False) 
    total_price = Column("total_price", Float)
    itens = relationship("Item", cascade="all, delete") 
    

    def __init__(self, user_id, status="PENDING", total_price=0,): 
        self.user_id = user_id
        self.status = status
        self.total_price = total_price

    def calculate_total_price(self): 
        self.total_price = sum(item.unit_price * item.quantity for item in self.itens) 

class Item(Base):
    __tablename__ = "order_items"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer, default=1)
    size = Column("size", String)
    flavor = Column("flavor", String)
    unit_price = Column("unit_price", Float)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"), nullable=False)

    def __init__(self, size, flavor, unit_price, order_id, quantity=1):
        self.size = size
        self.flavor = flavor
        self.unit_price = unit_price
        self.order_id = order_id
        self.quantity = quantity
