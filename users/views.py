import stripe
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, View

from config import settings
from users.forms import UserRegisterForm, UserUpdateForm, CancelSubscriptionForm, PaymentSubscriptionForm
from users.models import User, PaymentSubscription


class RegisterView(CreateView):
    """
    View for registering a new user
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    View for editing a user's profile
    """
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, View):
    """
    View for deleting a user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        logout(request)
        return redirect('users/user_success_delete.html')


def are_you_sure(request):
    return render(request, 'users/are_you_sure.html')


def user_success_delete(request):
    return render(request, 'users/user_success_delete.html')


class CreatePaymentSubscriptionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for creating a payment subscription
    """
    permission_required = 'content.add_paymentsubscription'
    template_name = 'users/subscription.html'
    success_url = reverse_lazy('users:payment_success')

    def get(self, request, *args, **kwargs):
        form = PaymentSubscriptionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        subscription_selection = [
            {'name': 'short',
             'description': 'short period of subscription for 1 month',
             'amount': 300,
             'currency': 'rub',
             'duration': '1 month'
             },
            {'name': 'long',
             'description': 'long period of subscription for 6 month',
             'amount': 600,
             'currency': 'rub',
             'duration': '6 month'
             },
            {'name': 'ultra',
             'description': 'ultra period of subscription for 1 year',
             'amount': 1000,
             'currency': 'rub',
             'duration': '1 year'},
        ]

        try:
            subscription_name = request.POST.get('subscription_name')
            selected_subscription = next((sub for sub in subscription_selection if sub['name'] == subscription_name),
                                         None)
            if selected_subscription is None:
                return HttpResponseBadRequest('No subscription selected')
            user = request.user

            amount_in_cents = selected_subscription['amount'] * 100

            subscription = PaymentSubscription.objects.create(
                user=user,
                amount=amount_in_cents,
                payment_url='',
                is_active=False
            )

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': selected_subscription['currency'],
                            'unit_amount': amount_in_cents,
                            'product_data': {
                                'name': selected_subscription['name'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('users:payment_success')),
                cancel_url=request.build_absolute_uri(reverse('users:payment_stop')),
            )
            subscription.payment_url = session.url
            subscription.save()

            return HttpResponseRedirect(session.url)
        except stripe.error.StripeError as e:
            return JsonResponse({'Error': str(e)}, status=400)


def success_view(request):
    """
    View for displaying success message
    """
    return render(request, 'users/payment_success.html')


def error_view(request):
    """
    View for displaying error message
    """
    return render(request, 'users/payment_error.html')


class CancelSubscriptionView(LoginRequiredMixin, View):
    """
    View for cancelling a subscription
    """
    template_name = 'users/cancel_subscription.html'
    success_url = 'profile'

    def post(self, request, *args, **kwargs):
        form = CancelSubscriptionForm(request.POST)
        if form.is_valid():
            user = request.user
            subscription = PaymentSubscription.objects.filter(user=user).first()

            if subscription:
                subscription.is_active = False
                subscription.save()
                messages.success(request, 'Your subscription has been successfully cancelled.')
            else:
                messages.error(request, 'You do not have an active subscription to cancel.')

            return redirect(self.success_url)
        else:
            messages.error(request, 'Please confirm cancellation.')
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        """
        Custom GET request for cancelling a subscription
        """
        form = CancelSubscriptionForm()
        return render(request, self.template_name, {'form': form})


def stop_payment(request):
    """
    View for stopping a payment subscription
    """
    return render(request, 'users/payment_stop.html')


class StripeWebhookView(LoginRequiredMixin, View):
    """
    Check out the Stripe session.
    """

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.headers['Stripe-Signature']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return HttpResponse({'Error': str(e)}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse({'Error': str(e)}, status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            payment_intent_id = session['payment_intent']
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if payment_intent.status == 'succeeded':
                user_id = session['client_reference_id']
                user = User.objects.get(id=user_id)
                user.is_subscribed = True
                user.save()

        return HttpResponse(status=200)


