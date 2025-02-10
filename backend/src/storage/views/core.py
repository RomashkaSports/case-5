from django.shortcuts import render

from src.storage.models import (
    Inventory,
)


def index(request):
    inventories = Inventory.objects.all().order_by('category_id')

    context = {
        'inventories': inventories
    }

    return render(
        request=request,
        context=context,
        template_name='index.html',
    )
