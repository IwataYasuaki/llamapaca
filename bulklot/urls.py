from django.urls import path

from . import views

app_name = 'bulklot'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('lotreq/', views.LotReqList.as_view(), name='lot_req_list'),
    path('lotreq/form', views.LotReqCreate.as_view(), name='lot_req_create'),
    path('lotreq/<int:pk>', views.LotReqDetail.as_view(), name='lot_req_detail'),
    path('member/', views.MemberList.as_view(), name='member_list'),
    path('member/form', views.MemberCreate.as_view(), name='member_create'),
    path('member/<int:pk>', views.MemberUpdate.as_view(), name='member_update'),
    path('member/<int:pk>/delete', views.MemberDelete.as_view(), name='member_delete'),
    path('lotresult/', views.LotResultList.as_view(), name='lot_result_list'),
]

