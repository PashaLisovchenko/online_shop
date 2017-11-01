from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, View, CreateView
from .forms import Register
from .models import User


class LoginView(FormView):
    template_name = 'sing_in.html'
    form_class = AuthenticationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)


class CreateUser(CreateView):
    model = User
    template_name = 'sign_up.html'
    form_class = Register
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = self.form_valid(form)
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        return user


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)
