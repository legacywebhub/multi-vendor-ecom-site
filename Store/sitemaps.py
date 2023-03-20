from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Product, User

# site maps of static pages
class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'Store:index', 
            'Store:cart', 
            'Store:special', 
            'Store:contact', 
            'Store:faq',  
            'Store:legal', 
            'Store:tac',
            'Store:checkout',
            'Store:login', 
            'Store:reset_password',
            ]

    def location(self, item):
        return reverse(item)

# site map of every user in database
class UserSitemap(Sitemap):
    def items(self):
        return User.objects.all()

# site map of every product in database
class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()


'''
make sure to add 'django.contrib.sitemaps' to installed apps
'''