from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:id>/', views.get_checkout_session, name='get_checkout_session'),
    path('item/<int:id>/', views.get_item_page, name='get_item_page'),
    path('create_order/', views.create_order, name='create_order'),
]
