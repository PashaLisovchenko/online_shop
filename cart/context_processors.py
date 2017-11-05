from .models import get_total_price, Cart
from django.db.models import Sum


def cart(request):
    total_quantity = Cart.objects.aggregate(total_sum=Sum('quantity'))
    if total_quantity['total_sum']:
        return {'total_items': total_quantity['total_sum'],
                'get_total_price': get_total_price}
    return {'total_items': 0,
            'get_total_price': get_total_price}