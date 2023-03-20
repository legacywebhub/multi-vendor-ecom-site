from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


measures = (
        ('kilos', 'kilos'),
        ('grams', 'grams'),
        ('kilograms', 'kilograms'),
        ('pieces', 'pieces'),
        ('crates', 'crates'),
        ('rolls', 'rolls'),
        ('cups', 'cups'),
        ('paints', 'paints'),
        ('sacks', 'sacks'),
        ('bags', 'bags'),
        ('package', 'package'),
        ('baskets', 'baskets'),
        ('buckets', 'buckets'),
        ('trucks', 'trucks'),
)
# Create your models here.

# This model holds general values, ads, address, links and other info of our site or app 
class CompanyInfo(models.Model):
    logo = models.ImageField(upload_to="images/company", blank=True, null=True)
    name = models.CharField(max_length=150, blank=False, null=False)
    address = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=25, blank=False, null=False)
    website = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.URLField(max_length=2000, blank=True, null=True)
    twitter_link = models.URLField(max_length=2000, blank=True, null=True)
    instagram_link = models.URLField(max_length=2000, blank=True, null=True)
    youtube_link = models.URLField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=60, null=False, blank=False,  help_text="e.g dollar")
    currency_shortcode = models.CharField(max_length=3, null=False, blank=False, help_text="e.g usd")
    currency_symbol = models.CharField(max_length=1, null=False, blank=False,  help_text="e.g $")
    public_key = models.CharField(max_length=160, blank=True, null=True)
    secret_key = models.CharField(max_length=160, blank=True, null=True)
    google_analytics = models.TextField(max_length=3000, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id and CompanyInfo.objects.exists():
            raise ValueError("This model cannot have two or more records")
        else:
            super().save(*args, **kwargs)


# Manager class for custom user
class UserManager(BaseUserManager):
    # Determines how to create our user model and validations
    def create_user(self, first_name, last_name, email, phone, password=None):
        # Use this check for as many field you want
        if not first_name:
            raise ValueError("first name is required")
        if not last_name:
            raise ValueError("last name is required")
        if not email:
            raise ValueError("email is required")
        if not phone:
            raise ValueError("Enter a phone number")

        user = self.model(
            # normalize_email ensures our email is properly formatted
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone
        )
        # Setting password for user
        user.set_password(password)
        # Saving user to database
        user.save(using=self._db)
        # Return user after saving
        return user

    # Determines how to create superuser
    def create_superuser(self, first_name, last_name, email, phone, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            password=password
        )
        # Granting permissions to the super user
        user.is_staff = True
        user.is_superuser = True
        # Saving user to database
        user.save(using=self._db)
        # Return user after saving
        return user

    '''
    Make sure to set this manager as the manager in your custom model
    objects = UserManager()
    '''


# Custom user model class
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name="first name", max_length=60)
    last_name = models.CharField(verbose_name="last name", max_length=60)
    username = models.CharField(verbose_name="username", max_length=30, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name="email address", max_length=60, unique=True)
    phone = models.CharField(verbose_name="phone", max_length=15, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def verified(self):
        if self.kyc.status == 'approved':
            verified = True
        else:
            verified = False
        return verified

    # Setting to determing what field to use as login parameter
    USERNAME_FIELD = "email"

    # Setting to set required fields
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    # Setting a manager for this custom user model
    objects = UserManager()

    # Setting to determine what field to show on our database
    def __str__(self):
        return self.full_name

    # Determines if signup user has permissions
    def has_perm(self, perm, obj=None):
        return True

    # Determines if the signed up user will have acccess to other models
    # In our app or project
    def has_module_perms(self, app_label):
        return True

    # Function to get url per user for sitemapping
    def get_absolute_url(self):
        return f'/profile/{self.id}'

    '''
    Make sure to set this custom model as our user model in settings.py
    AUTH_USER_MODEL = "App.CustomUserModel"
    Make sure to delete previous migration files incase of errors
    Then make migrations
    '''


class KYC(models.Model):
    id_types = (
        ('bvn', 'Bank Verification Number'),
        ('nin', 'National Identification Number')
    )
    status = (
        ('null', 'Null'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    company = models.CharField(verbose_name='Company name', max_length=150, blank=False, null=True)
    passport = models.ImageField(upload_to='images/user',blank=True, null=True)
    proof_of_address = models.ImageField(upload_to='images/user',blank=True, null=True)
    id_type = models.CharField(verbose_name='ID', max_length=20, choices=id_types, blank=True, null=True)
    id_number = models.CharField(verbose_name='ID Number', max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=250, blank=True, null=True, help_text="bio is a brief introduction about you which helps your customers and prospects know more about your personality")
    account_name = models.CharField(max_length=20, blank=True, null=True, help_text='bank account name')
    account_number = models.CharField(max_length=10, blank=True, null=True, help_text='bank account number')
    bank_name = models.CharField(max_length=20, blank=True, null=True, help_text='bank name')
    status = models.CharField(max_length=20,choices=status, default='pending')

    @property
    def approved(self):
        approved = False
        if self.status == 'approved':
            approved = True
        return approved

    def __str__(self):
        return self.user.full_name

    def save(self, *args, **kwargs):
        if self.status == 'declined':
            self.passport.delete()
            self.passport = None
            self.proof_of_address.delete()
            self.proof_of_address = None
            self.id_type = None
            self.id_number = None
            self.status = 'pending'
        super().save(*args, **kwargs)


# This model holds shipping details of signed up users
class ShippingDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    apartment = models.CharField(max_length=200, null=True, blank=True, help_text='block or room number')
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    phone1 = models.CharField(verbose_name='Land phone number', max_length=25, null=True, blank=True)
    phone2 = models.CharField(verbose_name='Mobile phone number', max_length=25, null=True, blank=True)

    def __str__(self):
        return self.user.full_name


# Products main category model
class Category(models.Model):
    category = models.CharField(max_length=60, unique=True, blank=True, null=False)

    def __str__(self):
        return self.category


# Products sub-category model
class ProductCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    product_category = models.CharField(max_length=60, unique=True, blank=False, null=False)

    def __str__(self):
        return self.product_category


# Product model
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_uploaded = models.DateField(auto_now=True) # this is the uploaded date
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    image1 = models.ImageField(verbose_name="Product image 1", upload_to='images/products',blank=True, null=True)
    image2 = models.ImageField(verbose_name="Product image 2", upload_to='images/products',blank=True, null=True)
    image3 = models.ImageField(verbose_name="Product image 3", upload_to='images/products',blank=True, null=True)
    image_url1 = models.URLField(max_length=3000, blank=True, null=True)
    image_url2 = models.URLField(max_length=3000, blank=True, null=True)
    image_url3 = models.URLField(max_length=3000, blank=True, null=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    measurement = models.CharField(max_length=20, choices=measures, blank=True, null=True)
    price = models.FloatField()
    percentage_discount = models.PositiveSmallIntegerField(default=0, choices=[(i, i) for i in range(0, 100)])
    tax_in_percentage = models.PositiveSmallIntegerField(default=0, choices=[(i, i) for i in range(0, 100)])
    shipping_fee = models.FloatField(default=0, null=False, blank=False)
    approved = models.BooleanField(default=False)

    # Function to check product rating according to customers
    @property
    def rating(self):
        pass

    # Function to check if product is in demand
    @property
    def hot(self):
        hot = False
        if self.rating >= 3.5:
            hot = True
        return hot


    # Function to calculate our discount in amount based on input discount percentage
    @property
    def discount(self):
        discount = (self.percentage_discount/100) * self.price
        return discount

    # Function to calculate discount price
    @property
    def discount_price(self):
        discount_price = self.price - self.discount
        return discount_price

    # Function to calculate tax amount based on input tax percentage
    @property
    def tax(self):
        tax_amount = (self.tax_in_percentage/100) * self.price
        return tax_amount
    
    # __str__ function determines what field to represent on the admin dashboard
    def __str__(self):
        return self.name

    # Functions to fix application crash if we don't have an image
    # This can also be fixed on our frontend by using if statement to check
    # if we have an image and then render something else if we dont have
    @property
    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    
    @property
    def image3URL(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    
    # Function to get exact category of product rather than ID of product category
    @property
    def product_category(self):
        category = ProductCategory.objects.get(id=self.category.id)
        return category.product_category
    
    # Function to get product url per item for site mapping
    def get_absolute_url(self):
        return f'/product/{self.id}'


# Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)

    # Function to check if all order items in an order has been delivered
    @property
    def delivered(self):
        delivered = False
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if not orderitem.delivered:
                delivered = False
            else:
                delivered = True
        return delivered


    # Function to sum up prices for all order items in our cart 
    @property
    def price_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.item_price_total for item in orderitems])
        return  total

    # Function to sum up DISCOUNT prices for all order items in our cart
    # Note that we are using discount prices rather than actual price
    @property
    def discount_price_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.item_discount_price_total for item in orderitems])
        return  total
    
    # Function to sum up tax for all order items in our cart
    @property
    def tax_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.item_tax_total for item in orderitems])
        return total

    # Function to sum up shipping fee for all order items in our cart
    @property
    def shipping_fee_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.item_shipping_fee_total for item in orderitems])
        return total
    
    # Function to sum up total order items in our cart and reset when order is delivered
    @property
    def item_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        # Resetting order items after delivery or delivered status has been set to true
        # if self.delivered == True:
        #     for i in orderitems:
        #         i.quantity = 0
        #         total = i.quantity
        return  total
    
    # Function to calculate total bill of customer using other functions
    @property
    def total(self):
        total = self.discount_price_total + self.shipping_fee_total + self.tax_total
        return total
    
    # Function to get our customer name to use in our admin dashboard
    @property
    def customer_name(self):
        return str(self.user.full_name)
    

# This model saves order products or items
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product.name

    # Function to check delivery status since order-items in an order may have different vendors/sellers
    @property
    def status(self):
        status = ''
        if self.order.complete and not self.delivered:
            status = 'pending'
        elif self.order.complete and self.delivered:
            status = 'delivered'
        return status

    # Function to calculate price of item by it's quantity
    @property
    def item_price_total(self):
        total = self.product.price * self.quantity
        return total

    # Function to calculate DISCOUNT price of item by it's quantity
    @property
    def item_discount_price_total(self):
        total = self.product.discount_price * self.quantity
        return total

    # Function to calculate shipping fee of item by it's quantity
    @property
    def item_shipping_fee_total(self):
        total = self.product.shipping_fee * self.quantity
        return total
    
    # Function to calculate tax of item by it's quantity
    @property
    def item_tax_total(self):
        total = self.product.tax * self.quantity
        return total

    # Function to calculate total bill or expenditure of item by it's quantity
    @property
    def item_total_bill(self):
        total = self.item_discount_price_total + self.item_shipping_fee_total + self.item_tax_total
        return total


# This model holds shipping address details for our customers that checked out
class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=200, null=False, blank=False)
    apartment = models.CharField(max_length=200, null=False, blank=False, help_text='block or room number')
    city = models.CharField(max_length=200, null=False, blank=False)
    state = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)
    zipcode = models.CharField(max_length=200, null=False, blank=False)
    phone1 = models.CharField(max_length=25, null=False, blank=False)
    phone2 = models.CharField(max_length=25, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    # shipping is not checked if payment was paid or completed because an instance
    # of shipping can only be created after successful payment

    def __str__(self):
        return f'{self.customer_name} {self.address}'


# This model saves messages from users on our contact page
class Message(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=3000, null=False, blank=False)
    date_received = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.date_received}'
