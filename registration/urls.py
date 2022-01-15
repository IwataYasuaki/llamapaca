from django.urls import path, include

from . import views

app_name = 'registration'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
]


