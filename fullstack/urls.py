
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from plans import views as plan_views
from customers import views as customers_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', plan_views.home, name='home'),
    path('signup/', customers_views.register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='customers/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
]
