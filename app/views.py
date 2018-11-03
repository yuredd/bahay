from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView

from app.models import SystemSetting, GPIOPin, Shutter

# Create your views here.
class DashboardView(TemplateView):
    template_name = 'app/dashboard.html'

class ShuttersView(ListView):
    model = Shutter
    template_name = 'app/shutters.html'

class UserLoginView(LoginView):
    pass

class SystemSettingView(ListView):
    model = SystemSetting

class GPIOPinView(ListView):
    model = GPIOPin

