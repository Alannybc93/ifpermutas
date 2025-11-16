from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home, name='home'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]