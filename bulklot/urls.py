from django.urls import path

from . import views

app_name = 'bulklot'
urlpatterns = [
    path('', views.LotReqList.as_view()),
    path('lotreq/', views.LotReqList.as_view(), name='lot_req_list'),
    path('lotreq/form', views.LotReqCreate.as_view(), name='lot_req_create'),
    path('lotreq/<int:pk>', views.LotReqDetail.as_view(), name='lot_req_detail'),
]

