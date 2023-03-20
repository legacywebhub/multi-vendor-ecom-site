from django import forms
from .models import User, ShippingDetail, KYC, Product



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'image1', 'image2', 'image3', 'category', 'name', 'description', 'measurement', 'price']



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



class KYCForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = ['company', 'passport', 'proof_of_address', 'id_type', 'id_number', 'bio', 'account_number', 'account_name', 'bank_name']



class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingDetail
        fields = ['address', 'apartment', 'city', 'state', 'country', 'zipcode', 'phone1', 'phone2']