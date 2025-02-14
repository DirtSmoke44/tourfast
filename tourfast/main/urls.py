from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.start, name='start_page'),
    path('hottours/', views.hottours, name='hottours_page'),
    path('registration/', views.RegisterView.as_view(), name='registration_page'),
    path('authorization/', views.LoginUserView.as_view(), name='login_page'),
    path('cart/', views.cart, name='cart_page'),
    path('profile/', views.profile, name='profile_page'),
    path('tours/', views.tours, name='tours_page'),
    path('accounts/', include("django.contrib.auth.urls")),
    path("logout/", views.logout_view, name="logout"),
    # path('clear-basket/', views.clear_basket, name='clear_basket'),
    # path('cart/remove/', views.remove_item, name='remove_item'),
    # path('create_transaction/', views.create_transaction, name='create_transaction'),
    # path('payment_result/<int:transaction_id>/', views.payment_result, name='payment_result'),
]