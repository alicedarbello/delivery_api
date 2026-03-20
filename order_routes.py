from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import create_session, verify_token
from schemas import OrderSchema, ItemSchema, StatusSchema, ResponseOrderSchema
from models import Order, User, Item
from typing import List

order_router = APIRouter(
    prefix="/orders", tags=["Orders"], dependencies=[Depends(verify_token)]
)

@order_router.get("/", response_model=List[ResponseOrderSchema])
async def get_orders(
    user_id: int | None = None,
    status: str | None = None,
    session: Session = Depends(create_session), user: User = Depends(verify_token)
):
    """
        This route is only for administrators. 
        You can get all orders, filter by user_id or by order status (PENDING, CANCELED, COMPLETED).
    """
    if not user.admin:
        raise HTTPException(
            status_code=401, detail="Only administrador can access this route."
        )
    else:
        orders = session.query(Order).all()
        
        if user_id:
            orders = [order for order in orders if order.user_id == user_id]

        if status:
            orders = [order for order in orders if order.status == status.upper()]

        if not orders:
            raise HTTPException(status_code=404, detail="No orders found with these filters.")

        return orders

@order_router.get("/{id_order}")
async def get_order_by_id(
    id_order: int,
    session: Session = Depends(create_session), user: User = Depends(verify_token)
):
    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    elif not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="You're not authorized.")
    return {
        "items_quantity": len(order.itens),
        "order": order
    }

@order_router.post("/", status_code=201)
async def create_order(
    order_schema: OrderSchema, session: Session = Depends(create_session)
):
    new_order = Order(
        user_id=order_schema.user_id
    )  
    session.add(new_order)
    session.commit()
    return {"message": f"Order created successfully. Order ID: {new_order.id}"}

@order_router.post("/{order_id}/items", status_code=201)
async def add_order_item(
    order_id: int,
    item_schema: ItemSchema,
    session: Session = Depends(create_session),
    user: User = Depends(verify_token),
):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found.")
    elif not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="You're not authorized.")
    order_item = Item(
        quantity=item_schema.quantity,
        size=item_schema.size,
        flavor=item_schema.flavor,
        unit_price=item_schema.unit_price,
        order_id=order_id,
    )
    session.add(order_item)
    order.calculate_total_price()  # type: ignore
    session.commit()
    return {
        "message": f"Item added successfully to order number {order.id}",
        "order_price": order.total_price
    }
    
@order_router.patch("/{order_id}")
async def modify_order(
    order_id: int,
    status: StatusSchema,
    session: Session = Depends(create_session),
    user: User = Depends(verify_token),
):
    """
        Only administrators can change the order status back to PENDING.
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found.")
    elif (
        not user.admin and user.id != order.user_id
    ):  
        raise HTTPException(
            status_code=401, detail="You're not authorized to do this."
        )
    
    if status is StatusSchema.CANCELED:
        order.status = "CANCELED"
        session.commit()
        return {
            "message": f"Your order number {order.id} was canceled successfully",
            "order": order,
        }
    if status is StatusSchema.COMPLETED:
        order.status = "COMPLETED"
        session.commit()
        return {
            "message": f"Your order number {order.id} was completed  successfully",
            "quantity_items": len(order.itens),
            "order": order
        }
    if status is StatusSchema.PENDING:
        if not user.admin:
            raise HTTPException(status_code=401, detail="You're not authorized to do this.")
        order.status = "PENDING"
        session.commit()
        return {
            "message": f"Order number {order.id} is pending again."
        }

@order_router.delete("/{order_id}/items/{id_item}")
async def remove_item(
    id_item: int,
    order_id: int,
    session: Session = Depends(create_session),
    user: User = Depends(verify_token),
):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found.")
    item = session.query(Item).filter(Item.id == id_item).first()
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    elif item:
        order = session.query(Order).filter(Order.id == item.order_id).first()
        if not user.admin and user.id != order.user_id:  # type: ignore
            raise HTTPException(status_code=401, detail="You're not authorized.")
        session.delete(item)
        order.calculate_total_price()  # type: ignore
        session.commit() 
        return {
            "message": f"Item removed successfully from order number {item.order_id}",
            "itens": order.itens,  # type: ignore
            "order": order
        }