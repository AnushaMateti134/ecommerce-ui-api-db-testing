from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, OrderItem, Product, User
from app.schemas import OrderCreate, OrderResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    # Check whether user exists
    user = (
        db.query(User)
        .filter(User.id == order.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    total_amount = 0
    order_items = []

    # Validate products and calculate total
    for item in order.items:
        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found"
            )

        item_total = product.price * item.quantity
        total_amount += item_total

        order_items.append(
            {
                "product_id": product.id,
                "quantity": item.quantity,
                "price": product.price
            }
        )

    # Create order
    new_order = Order(
        user_id=order.user_id,
        total_amount=total_amount,
        status="created"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Create order items
    for item in order_items:
        new_item = OrderItem(
            order_id=new_order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"]
        )

        db.add(new_item)

    db.commit()

    return new_order


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order