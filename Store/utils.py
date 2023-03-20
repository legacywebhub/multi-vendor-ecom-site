from datetime import datetime
from django.shortcuts import render, redirect
from .models import *


# Functions

# Generating a unique code used as order or transaction id
# Or cookie to identify unique customers
def generateUniqueId():
    return str(datetime.now().timestamp()).replace('.', '-')

# View functions for D.R.Y principle
def getCustomerAndOrder(request):
    try:
        customer = request.user
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items =  order.orderitem_set.all()
        item_total = order.item_total
        total = order.total
        object = {'items':items, 'order':order, 'item_total': item_total, 'total': total, 'customer': customer,}
    except:
        object = {'order':'null', 'items':[], 'item_total': 0, 'total': 0, 'customer': customer,}
    return object


