from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Customer
import stripe

stripe.api_key = 'sk_test_51HUzEAAj0A8AR6EvtWJDi2lxKl5TZFqT9QR88Bw2yflGU9eUMHig5uRzKyzF71pgO4uRUSjIu2lGgTo6DOToVJdQ00xr8Jydzy'


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return redirect('signup')
    else:
        form = UserRegistrationForm()
        return render(request, 'customers/signup.html', {'form': form})

@login_required
def checkout(request):
    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email='fullstack@yandex.com', source=request.POST['stripeToken'])
        plan = 'price_1HWoeLAj0A8AR6EvINfFvpmN'
        if request.POST['plan'] == 'regular':
            plan = 'price_1HWoeMAj0A8AR6EvMCX38Ekw'
        if request.POST['plan'] == 'premium':
            plan = 'price_1HWoeMAj0A8AR6EvWrwZ1tv7'
        if request.POST['plan'] == 'king':
            plan = 'price_1HWoeMAj0A8AR6EvwaCW8nO9'
        subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{'plan': plan}])

        customer = Customer()
        customer.user = request.user
        customer.stripe_id = stripe_customer.id
        customer.cancel_at_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()

        return redirect('home')
    else:
        plan = 'basic'
        description = 'TV (30 channels)'
        price = 495
        og_euro = 4.95
        final_euro = 4.95
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'regular':
                plan = 'regular'
                description = 'TV + Broadband'
                price = 995
                og_euro = 9.95
                final_euro = 9.95
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'premium':
                plan = 'premium'
                description = 'TV + Broadband + Movies'
                price = 1995
                og_euro = 19.95
                final_euro = 19.95
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'king':
                plan = 'king'
                description = 'TV + Broadband + Movies + Sports + Netflix'
                price = 2995
                og_euro = 29.95
                final_euro = 29.95

        return render(request, 'customers/checkout.html',
        {'plan':plan,'description':description,'price':price,'og_euro':og_euro,'final_euro':final_euro})
