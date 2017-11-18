from cart.views import get_total_price, get_total_item


def cart(request):
    return {'total_items': get_total_item(request),
            'get_total_price': get_total_price(request)}
