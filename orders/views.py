from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.models import Cart, get_total_price
from django.views.generic import ListView
from django.views.generic.edit import FormMixin


class OrderCreate(FormMixin, ListView):
    model = Cart
    template_name = 'create.html'
    context_object_name = 'cart'
    form_class = OrderCreateForm

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['get_total_price'] = get_total_price
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
