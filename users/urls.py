from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, success_view, error_view, CancelSubscriptionView, \
    CreatePaymentSubscriptionView, stop_payment

app_name = UsersConfig.name

urlpatterns = [
    # User URLs
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # PaymentSubscription URLs
    path('subscription/', CreatePaymentSubscriptionView.as_view(), name='subscription'),
    path('payment_stop/', stop_payment, name='payment_stop'),
    path('payment_success/', success_view, name='payment_success'),
    path('payment_error/', error_view, name='payment_error'),
    path('cancel_subscription/<int:pk>/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
]
