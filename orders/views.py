from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.models import Cart
from cart.views import get_total_price
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormMixin, ListView):
    model = Cart
    template_name = 'create.html'
    context_object_name = 'cart'
    form_class = OrderCreateForm

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['get_total_price'] = get_total_price(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        order = form.save()
        cart = self.model.objects.all()
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item.products,
                                     price=item.product_price,
                                     quantity=item.quantity)
        cart.delete()
        return render(None, 'created.html', {'order': order})
