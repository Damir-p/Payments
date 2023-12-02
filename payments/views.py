# views.py
from django.shortcuts import render
from django.http import JsonResponse
import stripe
from dotenv import load_dotenv
import os

from payments.models import Item, Order

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def get_checkout_session(request, id):
    item = Item.objects.get(pk=id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/item/{id}'),
        cancel_url=request.build_absolute_uri(f'/item/{id}'),
    )

    return JsonResponse({'session_id': session.id})

def get_item_page(request, id):
    item = Item.objects.get(pk=id)
    stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    return render(request, 'item_page.html', {'item': item, 'stripe_publishable_key': stripe_publishable_key})

def create_order(request):
    items_ids = request.POST.getlist('item_ids[]')
    items = Item.objects.filter(pk__in=items_ids)
    total_price = sum(item.price for item in items)

    order = Order.objects.create(total_amount=total_price)  # Используйте total_amount вместо total_price
    order.items.set(items)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',  # Укажите валюту, в которой вы хотите произвести оплату
                'product_data': {
                    'name': f'Order #{order.id}',
                },
                'unit_amount': int(total_price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/order/{order.id}'),
        cancel_url=request.build_absolute_uri(f'/order/{order.id}'),
    )

    return JsonResponse({'session_id': session.id})
