from sqlalchemy import create_engine, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from settings import DATABASE_URL

# 1. Create connection to the database
db = create_engine(DATABASE_URL) 

# 2. Create a base class for our models
Base = declarative_base() 

# 3. Define our models/tables
class User(Base): 
    __tablename__ = "users" 
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("nome", String)
    email: Mapped[str] = mapped_column("email", String, nullable=False)
    password: Mapped[str] = mapped_column("password", String)
    active: Mapped[bool] = mapped_column("active", Boolean)
    admin: Mapped[bool] = mapped_column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column("status", String) 
    user_id: Mapped[int] = mapped_column("user_id", Integer, ForeignKey("users.id"), nullable=False) 
    total_price: Mapped[float] = mapped_column("total_price", Float)
    itens: Mapped[list["Item"]] = relationship("Item", cascade="all, delete") 
    

    def __init__(self, user_id, status="PENDING", total_price=0,): 
        self.user_id = user_id
        self.status = status
        self.total_price = total_price

    def calculate_total_price(self): 
        self.total_price = sum(item.unit_price * item.quantity for item in self.itens) 

class Item(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column("quantity", Integer, default=1)
    size: Mapped[str] = mapped_column("size", String)
    flavor: Mapped[str] = mapped_column("flavor", String)
    unit_price: Mapped[float] = mapped_column("unit_price", Float)
    order_id: Mapped[int] = mapped_column("order_id", Integer, ForeignKey("orders.id"), nullable=False)

    def __init__(self, size, flavor, unit_price, order_id, quantity=1):
        self.size = size
        self.flavor = flavor
        self.unit_price = unit_price
        self.order_id = order_id
        self.quantity = quantity
        self.quantity = quantity
