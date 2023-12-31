from django.urls import path
from .views import MenuItemListView, SingleMenuItemView
urlpatterns = [
    path('menu-items', MenuItemListView.as_view(), name='menu-item-list'),
    path('menu-items/<int:pk>', SingleMenuItemView.as_view(), name='menu-item-detail'),
]