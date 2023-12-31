from django.urls import path
from .views import MenuItemListView, SingleMenuItemView, ManagerGroupUsersView, ManagerGroupUserDetailView, OrderListView, OrderDetailView
urlpatterns = [
    path('menu-items', MenuItemListView.as_view(), name='menu-item-list'),
    path('menu-items/<int:pk>', SingleMenuItemView.as_view(), name='menu-item-detail'),
    path('groups/manager/users/', ManagerGroupUsersView.as_view(), name='manager-group-users'),
    path('groups/manager/users/<int:pk>/', ManagerGroupUserDetailView.as_view(), name='manager-group-user-detail'),
    path('orders', OrderListView.as_view(), name='order-list-create'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
]