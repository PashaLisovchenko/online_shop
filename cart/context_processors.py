from .models import get_total_price, Cart


def cart(request):
    carts = Cart.objects.all()
    q = []
    for c in carts:
        q.append(c.quantity)
    total_items = sum(total for total in q)
    return {'total_items': total_items,
            'get_total_price': get_total_price,}