from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_page'),
    path('about/', views.about, name='about_page'),
    path('registration/', views.registration, name='registration_page'),
    path('authorization/', views.authorization, name='login_page'),
    path('cart/', views.cart, name='cart_page'),
    path('profile/', views.profile, name='profile_page'),
    path('tours/', views.tours, name='tours_page'),
    # path('logout/', views.user_logout, name='logout1'),
    # path('clear-basket/', views.clear_basket, name='clear_basket'),
    # path('cart/remove/', views.remove_item, name='remove_item'),
    # path('create_transaction/', views.create_transaction, name='create_transaction'),
    # path('payment_result/<int:transaction_id>/', views.payment_result, name='payment_result'),
]