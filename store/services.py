from django.db import transaction
from store.models import (
    Order,
    OrderItem,
    CartItem,
    Cart,
    Product,
    Customer
)


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(validated_data, user):

        customer = Customer.objects.get(user=user)

        payment_method = validated_data.get(
            "payment_method"
        )

        order = Order.objects.create(
            customer=customer,
            payment_method=payment_method
        )

        cart_id = validated_data.get("cart_id")
        product_id = validated_data.get("product_id")
        quantity = validated_data.get("quantity", 1)

        total = 0

        # ---------------- CART CHECKOUT ----------------
        if cart_id:

            cart_items = CartItem.objects.select_related(
                "product"
            ).filter(cart_id=cart_id)

            order_items = []

            for item in cart_items:

                item_total = (
                    item.product.unit_price * item.quantity
                )

                total += item_total

                order_items.append(
                    OrderItem(
                        order=order,
                        product=item.product,
                        unit_price=item.product.unit_price,
                        quantity=item.quantity,
                    )
                )

            OrderItem.objects.bulk_create(order_items)

            # delete cart after order
            Cart.objects.filter(pk=cart_id).delete()

        # ---------------- BUY NOW ----------------
        elif product_id:

            product = Product.objects.get(pk=product_id)

            total = (
                product.unit_price * quantity
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                unit_price=product.unit_price,
                quantity=quantity
            )

        # ---------------- SAVE TOTAL ----------------
        order.cached_total_price = total

        order.save(update_fields=[
            "cached_total_price"
        ])

        return order