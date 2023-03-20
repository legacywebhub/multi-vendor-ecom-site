from django.contrib import admin
from .models import *
from django.utils.html import format_html


# Admin Classes
class CompanyInfoAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name', 'logo', 'currency')

    def logo(self, obj):
        if obj.logo:
            logo = format_html(f'<img src="/media/{obj.logo}" style="width:100px;">')
        else:
            logo = ''
        return logo



class UserAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('full_name', 'email')
    list_per_page = 30



class KYCAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('user', 'id_type', 'status')
    list_per_page = 30



class ShippingDetailAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('__str__', 'country',)
    list_per_page = 30



class ProductAdmin(admin.ModelAdmin):
    exclude = ('date_uploaded',)
    list_display = ('name', 'category', 'product_image', 'price', 'seller', 'approved')
    list_filter = ('category', 'date_uploaded', 'approved',)
    list_per_page = 20

    def product_image(self, obj):
        if obj.image1:
            image = format_html(f'<img src="/media/{obj.image1}" style="width:100px;">')
        elif obj.image_url1:
            image = format_html(f'<img src="{obj.image_url1}" style="width:100px;">')
        else:
            image = ''
        return image

    def save_model(self, request, obj, form, change):
        obj.seller = request.user
        obj.save()



class OrderAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('id', 'customer_name', 'total', 'complete',)
    list_filter = ('date_ordered', 'complete',)
    list_per_page = 20



class ShippingAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('user', 'order', 'country', 'delivered')
    list_filter = ('date_added', 'delivered')
    list_per_page = 20



class MessageAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name', 'location', 'subject', 'email')
    list_filter = ('date_received',)
    list_per_page = 20



class OrderItemAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('__str__', 'order', 'quantity', 'status')
    list_filter = ('date_added',)
    list_per_page = 30



# Register your models here.
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(User, UserAdmin)
admin.site.register(ShippingDetail, ShippingDetailAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(KYC, KYCAdmin)