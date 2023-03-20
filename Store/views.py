from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.contrib.auth.models import auth
from .forms import UserForm, ShippingForm, KYCForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django_pandas.io import read_frame
from .utils import *
from decouple import config


# Create your views here.

def index(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    new_products = Product.objects.filter(approved=True).order_by('-date_uploaded')[:4]
    p = Paginator(Product.objects.filter(approved=True), 18)
    page = request.GET.get('page')
    products = p.get_page(page)
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'company': company,
        'products': products,
        'categories' : categories,
        'random_products':random_products,
        'new_products': new_products,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
    }

    # Setting up our response object
    return render(request, 'index.html', context)



def products(request, search):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    products_list = Product.objects.filter(name__contains=search, approved=True)
    p = Paginator(products_list, 18)
    page = request.GET.get('page')
    products = p.get_page(page)
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'search':search,
        'products':products,
        'products_count':products_list.count,
        'company': company,
        'categories' : categories,
        'random_products':random_products,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
    }
    return render(request, 'products.html', context)



def specialOffer(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    # Looping through our products and add any which percentage discount
    # is more than %15 to an empty list
    all_products = Product.objects.filter(approved=True)
    products_list = []
    for product in all_products:
        if product.percentage_discount > 15 and product.shipping_fee == 0:
            products_list.append(product)

    p = Paginator(products_list, 18)
    page = request.GET.get('page')
    products = p.get_page(page)
    products_count = len(products_list)
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'products':products,
        'products_count':products_count,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'company': company,
        'categories' : categories,
        'random_products':random_products
    }
    return render(request, 'special_offers.html', context)



def category(request, category):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    products_list = Product.objects.filter(category=category, approved=True)
    category = ProductCategory.objects.get(id=category)
    p = Paginator(products_list, 18)
    page = request.GET.get('page')
    products = p.get_page(page)
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'company': company,
        'products':products,
        'products_count':products_list.count,
        'category': category,
        'item_total': order_data['item_total'],
        'total': order_data['total'],

        'categories' : categories,
        'random_products':random_products
    }
    return render(request, 'product-category.html', context)



def cart(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'company': company,
        'items': order_data['items'],
        'order': order_data['order'],
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'categories' : categories,
        'random_products':random_products
    }
    return render(request, 'cart.html', context)



def detail(request, pk):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    product = Product.objects.get(id=pk)
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    seller_products = Product.objects.filter(seller=product.seller, approved=True).order_by('?')[:10]
    other_products = []

    for seller_product in seller_products:
        if seller_product.id != product.id and len(other_products) < 7:
            other_products.append(seller_product)
        else:
            break

    if request.method == 'POST':
        if 'add-item-quantity' in request.POST:
            quantity = request.POST['quantity']
            orderItem, created = OrderItem.objects.get_or_create(order=order_data['order'], product=product)

            if quantity == 0:
                orderItem.delete()
            else:
                orderItem.quantity = quantity
                orderItem.save()
            return redirect('Store:cart')

            '''
            This is another way to write the code.. Either by checking the quantity first before doing
            any operation or setting quantity to order item before checking and doing operations

            orderItem.quantity = quantity

            if orderItem.quantity == 0:
                orderItem.delete()
            else:
                orderItem.save()
            ''' 
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)

    context = {
        'company': company,
        'product': product,
        'other_products': other_products,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'categories' : categories,
        'random_products':random_products
    }
    return render(request, 'product_details.html', context)



def login(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    if request.method == "POST":
        if 'register-submit' in request.POST:
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            email = request.POST['register-email']
            phone = request.POST['phone']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password2 == password1:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Sorry this email has already been taken!')
                else:
                    # Saving user and user instances
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone, password=password2)
                    user.save()
                    messages.success(request, 'Your account has successfully been created... you can now sign in!')
                    # shipping detail is created for every user by default on the custom user model 
            else:
                messages.error(request, 'Passwords does not match... Please try again')   
        elif 'login-submit' in request.POST:
            email = request.POST['login-email']
            password = request.POST['password']

            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid credentials..   Please try again')
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)
    context = {'company': company, 'item_total': order_data['item_total'], 'total': order_data['total'], 'categories' : categories,
    'random_products':random_products }
    return render(request, 'login.html', context)



def logout(request):
    auth.logout(request)
    return redirect('/')



def profile(request, pk):
    company = CompanyInfo.objects.last()
    user = User.objects.get(id=pk)
    user_products = Product.objects.filter(seller=request.user, approved=True)
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    context = {
        'user': user,
        'company': company,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'user_products': user_products
    }
    return render(request, 'profile.html', context)




@login_required
def dashboard(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
    pending_deliveries = []

    if request.user.verified:
        orders = Order.objects.filter(complete=True)
        for order in orders:
            for orderitem in order.orderitem_set.all():
                if orderitem.product.seller == request.user:
                    pending_deliveries.append(orderitem)


    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            product = Product.objects.filter(seller=None).last()
            product.seller = request.user
            product.save()
            messages.success(request, 'Your product was successfully uploaded')
            return redirect('Store:dashboard')
    else:
        product_form = ProductForm() #initial={"seller":request.user}
        #product_form.fields['seller'] = request.user

    context = {
        'company': company,
        'categories': categories,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'pending_deliveries': pending_deliveries,
        'product_form': product_form,
        'my_products': Product.objects.filter(seller=request.user).order_by('-date_uploaded')[:10],
        'approved_products': Product.objects.filter(seller=request.user, approved=True),
        'unapproved_products': Product.objects.filter(seller=request.user, approved=False),
        'my_orders': Order.objects.filter(user=request.user).order_by('-date_ordered')[:10]
    }
    return render(request, 'dashboard.html', context)



@login_required
def userProducts(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    # Returning paginated user products
    products_list = Product.objects.filter(seller=request.user).order_by('-date_uploaded')
    p = Paginator(products_list, 15)
    page = request.GET.get('page')
    user_products = p.get_page(page)
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
    
    context = {
        'company': company,
        'categories': categories,
        'user_products': user_products,
        'products_count': products_list.count,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
    }
    return render(request, 'user_products.html', context)



@login_required
def editProduct(request, pk):
    company = CompanyInfo.objects.last()
    product = Product.objects.get(id=pk)
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Your product was successfully updated')
    else:
        product_form = ProductForm(instance=product)
    
    context = {
        'company': company,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'product': product,
        'product_form': product_form,
    }
    return render(request, 'edit_product.html', context)



@login_required
def settings(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    user_instance = User.objects.get(id=request.user.id)
    user_shipping = ShippingDetail.objects.get(user=user_instance)
    user_kyc = KYC.objects.get(user=user_instance)
    # This forms here solves our bug issue after saving either of our forms
    user_form = UserForm(instance=user_instance)
    shipping_form = ShippingForm(instance=user_shipping)
    kyc_form = KYCForm(instance=user_kyc)
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    if request.method == "POST":
        if 'save-user-detail' in request.POST:
            user_form = UserForm(request.POST or None, instance=user_instance)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile successfully updated')
        elif 'save-shipping-detail' in request.POST:
            shipping_form = ShippingForm(request.POST or None, instance=user_shipping)
            if shipping_form.is_valid():
                shipping_form.save()
                messages.success(request, 'Your shipping details successfully updated')
        elif 'save-kyc' in request.POST:
            kyc_form = KYCForm(request.POST, request.FILES, instance=user_kyc)
            if kyc_form.is_valid():
                kyc_form.save()
                messages.success(request, 'Your KYC was successfully uploaded and will be approved after proper verification')
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)
    else:
        user_form = UserForm(instance=user_instance)
        shipping_form = ShippingForm(instance=user_shipping)
        kyc_form = KYCForm(instance=user_kyc)

    context = {
        'company': company,
        'user_form': user_form, 
        'shipping_form': shipping_form,
        'kyc_form': kyc_form,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'categories': categories,
        'random_products': random_products
        }
    return render(request, 'settings.html', context)



def contact(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    if request.method == 'POST':
        if 'message' in request.POST:
            name = request.POST['name']
            location = request.POST['location']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']

            try:
                email.index('@') and email.index('.')
            except ValueError:
                messages.info(request, 'Your email is not valid')
            else:
                try:
                    # Trying to notify company or admins via mail
                    send_mail(
                    f'{subject}({location})', message, email, [company.email1, company.email2], fail_silently=False
                    )
                    print(f'Message was successfully sent to admins...')
                except:
                    pass
                message = Message.objects.create(name=name, location=location, email=email, subject=subject, message=message)
                message.save()
                messages.success(request, 'Your message was sent successfully')
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'], 
        'total': order_data['total'], 
        'company': company,
        'categories': categories,
        'random_products': random_products
    }
    return render(request, 'contact.html', context)



@login_required
def checkout(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'items': order_data['items'],
        'order': order_data['order'],
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'customer': order_data['customer'],
        'public_key': config('PAYSTACK_PUBLIC_KEY'),
        'company': company,
        'categories' : categories,
        'random_products':random_products
    }
    return render(request, 'checkout.html', context)



def success(request, pk):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    order = Order.objects.get(id=pk)

    if not order.complete:
        messages.error(request, 'This order has not been paid for or completed')
        return redirect('/checkout/')

    item_total = order.item_total
    total = order.total

    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'order': order,
        'item_total': item_total,
        'total': total, 
        'company': company,
        'categories' : categories,
        'random_products':random_products,
    }

    return render(request, 'success.html', context)

    

def faq(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'random_products':random_products
    }
    return render(request, 'faq.html', context)



def legal(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'random_products':random_products
    }
    return render(request, 'legal_notice.html', context)



def tac(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'random_products':random_products
    }
    return render(request, 'tac.html', context)



def error404(request, exception):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'random_products':random_products
    }
    return render(request, '404.html', context)



def serverError(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {        
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'random_products':random_products}
    return render(request, '500.html', context)



def newsletter(request):
    company = CompanyInfo.objects.last()
    categories = Category.objects.all()
    random_products = Product.objects.filter(approved=True).order_by('?')[:3]
    # Getting request user order
    order_data = getCustomerAndOrder(request)
    # getting all users email
    emails = User.objects.all()
    # the following line of codes converts the query to a list object
    # using the read_mail function from django-pandas external module
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()

    if request.method=="POST":
        if 'newsletter-submit' in request.POST:
            subject = request.POST['subject']
            message = request.POST['message']
            file = request.POST['file']

            if request.user.is_superuser:
                if 'file' in request.POST:
                    
                    try:
                        email = EmailMessage(subject, message, company.email1, mail_list)
                        email.content_subtype = 'html'
                        email.attach(file.name, file.read(), file.content_type)
                        email.send()
                        messages.success(request, 'Message and file succesfully sent to mail list')
                    except:
                        messages.error(request, 'Sorry... There was an error while forwarding newsletter')
                        
                else:
                    try:
                        send_mail(subject, message, company.email1, mail_list, fail_silently=False)
                        messages.success(request, 'Message succesfully sent to mail list')
                    except:
                        messages.error(request, 'Sorry... There was an error while forwarding newsletter')
            else:
                messages.error(request, 'Sorry... Only admins can forward newsletters')
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)
    
    context = {        
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'random_products':random_products,
        }
    return render(request, 'newsletter.html', context)





# Pseudo Views

def deleteProduct(request):
    data = json.loads(request.body)
    productId = data['productId']
    print(productId)
    product = Product.objects.get(id=productId)
    if product:
        product.delete()
        return JsonResponse('success', safe=False)
    else:
        return JsonResponse('failed', safe=False)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('product',productId)
    print('action',action)
    
    # Getting product
    product = Product.objects.get(id=productId)
    # Fetching order of customer
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    # Determines what action to take
    if action == 'subtract':
        orderItem.quantity -= 1
    elif action == 'add':
        orderItem.quantity += 1
    elif action == 'delete':
        orderItem.delete()
        
    orderItem.save()
    
    # Deleting item if quantity is less than 1
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was manipulated', safe=False)



def processShippingOrder(request):
    data = json.loads(request.body)
    print('data:', data)
    phone2 = data['orderFormData']['phone2']

    # Checking to see if phone2 is empty since it isn't mandactory
    # Set as None if an empty string
    if phone2 == '' or phone2 == "None":
        phone2 = None

    # Trying to get customer from authenticated user
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order.transaction_id = data['orderFormData']['transaction-id']
    total = data['orderFormData']['total']

    # Making sure total on the frontend equals total on the backend
    # Frontend may be manipulated using browser inspection tool
    if total == order.total:
        order.complete = True
    order.save()

    print('order saved')

    # Saving shipping detail for current order
    shipping = Shipping.objects.create(
        user=request.user,
        order=order,
        address=data['orderFormData']['address'],
        apartment=data['orderFormData']['apartment'],
        city=data['orderFormData']['city'],
        state=data['orderFormData']['state'],
        country=data['orderFormData']['country'],
        zipcode=data['orderFormData']['zipcode'],
        phone1=data['orderFormData']['phone1'],
        phone2=phone2,
    )
    shipping.save()

    print('shipping saved')
    
    return JsonResponse('Payment and checkout was successful', safe=False)



def setDeliveredOrder(request):
    data = json.loads(request.body)
    print('data:', data)
    order = Order.objects.get(id=data['orderId'])
    status = 'failed'

    if order.complete:
        try:
            orderitems =  order.orderitem_set.all()
            for orderitem in orderitems:
                orderitem.delivered = True
                orderitem.save()
            shipping = Shipping.objects.get(order=order)
            shipping.delivered = True
            shipping.save()
            status = 'success'
        except:
            status = 'failed'
    print(status)
    # Note that Order.delivered is automatically set when all order item has been delivered
    return JsonResponse(status, safe=False)