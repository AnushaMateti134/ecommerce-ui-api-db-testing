from sqlalchemy import text

from app.database import SessionLocal


def get_user_by_id(user_id: int):
    db = SessionLocal()

    try:
        query = text(
            """
            SELECT id, username, email
            FROM users
            WHERE id = :user_id
            """
        )

        result = db.execute(
            query,
            {"user_id": user_id}
        ).mappings().first()

        return result

    finally:
        db.close()
def get_product_by_id(product_id: int):
    db = SessionLocal()

    try:
        query = text(
            """
            SELECT id, name, description, price, category
            FROM products
            WHERE id = :product_id
            """
        )

        result = db.execute(
            query,
            {"product_id": product_id}
        ).mappings().first()

        return result

    finally:
        db.close()
def get_order_by_id(order_id: int):
    db = SessionLocal()

    try:
        query = text(
            """
            SELECT id, user_id, total_amount, status
            FROM orders
            WHERE id = :order_id
            """
        )

        result = db.execute(
            query,
            {"order_id": order_id}
        ).mappings().first()

        return result

    finally:
        db.close()


def get_order_items_by_order_id(order_id: int):
    db = SessionLocal()

    try:
        query = text(
            """
            SELECT id, order_id, product_id, quantity, price
            FROM order_items
            WHERE order_id = :order_id
            ORDER BY id
            """
        )

        result = db.execute(
            query,
            {"order_id": order_id}
        ).mappings().all()

        return result

    finally:
        db.close()