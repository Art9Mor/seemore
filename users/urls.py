from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, success_view, error_view, CancelSubscriptionView, \
    CreatePaymentSubscriptionView, stop_payment, user_success_delete, UserDeleteView, are_you_sure, CustomLoginView, \
    AccountInactiveView, must_subscribe, must_register, user_success_update

app_name = UsersConfig.name

urlpatterns = [
    # User URLs
    path('', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('account_inactive/', AccountInactiveView.as_view(), name='account_inactive'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user_delete/', UserDeleteView.as_view(), name='user_delete'),
    path('are_you_sure/', are_you_sure, name='are_you_sure'),
    path('user_success_delete/', user_success_delete, name='user_success_delete'),
    path('user_success_update/', user_success_update, name='user_success_update'),

    # PaymentSubscription URLs
    path('subscription/', CreatePaymentSubscriptionView.as_view(), name='subscription'),
    path('payment_stop/', stop_payment, name='payment_stop'),
    path('payment_success/', success_view, name='payment_success'),
    path('payment_error/', error_view, name='payment_error'),
    path('cancel_subscription/<int:pk>/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
    path('must_subscribe/', must_subscribe, name='must_subscribe'),
    path('must_register/', must_register, name='must_register'),
]
