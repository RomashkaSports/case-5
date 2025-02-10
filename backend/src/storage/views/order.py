import json
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from src.storage.models import Inventory, Order, OrderItem


@login_required
@csrf_exempt
def order(request):
    if request.method != 'POST':
        return HttpResponse(status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    if not isinstance(data, dict):
        return HttpResponse(status=400)

    if not all(isinstance(key, str) and isinstance(value, int) for key, value in data.items()):
        return HttpResponse(status=400)

    if not all(int(value) > 0 for value in data.values()):
        return HttpResponse(status=400)

    with transaction.atomic():
        inventory = Inventory.objects.filter(id__in=data.keys())
    
        if not inventory:
            return HttpResponse(status=400)
    
        if not all(i.available >= data[str(i.pk)] for i in inventory):
            return HttpResponse(status=400)
    
        new_order = Order.objects.create(
            user=request.user,
            end_date=datetime.now() + timedelta(days=7),
        )
        order_inventory = []
        for i in inventory:
            order_inventory.append(OrderItem(
                order=new_order,
                inventory=i,
                count=data[str(i.pk)],
            ))
        OrderItem.objects.bulk_create(order_inventory)

    return HttpResponse(reverse('storage:order_detail', kwargs={'pk': new_order.pk}))


def order_detail(request, pk):
    order = None
    if request.user.is_authenticated:
        order = get_object_or_404(
            Order,
            user=request.user,
            pk=pk,
        )

    context = {
        'order': order,
    }

    return render(
        request=request,
        context=context,
        template_name='order_detail.html',
    )


def orders_list(request):
    orders = None
    new_orders = None
    active_orders = None
    other_orders = None

    if request.user.is_authenticated:
        orders = Order.objects.filter(
            user=request.user,
        )
        new_orders = orders.filter(
            status=Order.Status.CREATED,
        )
        active_orders = orders.filter(
            status=Order.Status.ACTIVE,
        )
        other_orders = orders.exclude(
            status__in=(
                Order.Status.CREATED,
                Order.Status.ACTIVE,
            )
        )

    context = {
        'orders': orders,
        'new_orders': new_orders,
        'active_orders': active_orders,
        'other_orders': other_orders,
    }

    return render(
        request=request,
        context=context,
        template_name='orders.html',
    )
