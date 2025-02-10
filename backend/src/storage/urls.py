from django.urls import path

from src.storage import views

app_name = 'storage'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/auth/', views.auth, name='auth'),
    path('api/order/', views.order, name='order'),
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:pk>', views.order_detail, name='order_detail'),
]
