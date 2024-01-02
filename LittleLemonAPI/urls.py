from django.urls import path
from .views import MenuItemListView, SingleMenuItemView, ManagerGroupUsersView, ManagerGroupUserDetailView, OrderListView, OrderDetailView, DeliveryGroupUserDetailView, DeliveryGroupUsersView, CartListView
urlpatterns = [
    path('menu-items', MenuItemListView.as_view(), name='menu-item-list'),
    path('menu-items/<int:pk>', SingleMenuItemView.as_view(), name='menu-item-detail'),
    path('groups/manager/users', ManagerGroupUsersView.as_view(), name='manager-group-users'),
    path('groups/manager/users/<int:pk>', ManagerGroupUserDetailView.as_view(), name='manager-group-user-detail'),
    path('groups/delivery-crew/users', DeliveryGroupUsersView.as_view(), name='manager-group-users'),
    path('groups/delivery-crew/users/<int:pk>', DeliveryGroupUserDetailView.as_view(), name='manager-group-user-detail'),
    path('cart/menu-items', CartListView.as_view(), name='cart-list'),
    path('orders', OrderListView.as_view(), name='order-list-create'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
]