from django.urls import path, reverse_lazy
from . import views
# For password reset
from django.contrib.auth import views as auth_views
# Site map
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, UserSitemap, ProductSitemap


sitemaps = {
    'static': StaticViewSitemap,
    'User': UserSitemap,
    'product': ProductSitemap,
}

app_name='Store'
urlpatterns = [
    # Page urls and paths
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('category/<str:category>', views.category, name='category'),
    path('special-offer/', views.specialOffer, name='special'),
    path('products/<str:search>/', views.products, name='products'),
    path('product/<str:pk>/', views.detail, name='detail'),
    path('my-products/', views.userProducts, name='user_products'),
    path('product/edit/<str:pk>/', views.editProduct, name='edit_product'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('legal-notice/', views.legal, name='legal'),
    path('tac/', views.tac, name='tac'),
    path('checkout/', views.checkout, name='checkout'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('success/<str:pk>/', views.success, name='success'),

    # Pseudo urls and paths
    path('update_item/', views.updateItem, name='update_item'),
    path('delete_product/', views.deleteProduct, name='delete_product'),
    path('process_shipping_order/', views.processShippingOrder, name='process_shipping_order'),
    path('set_delivered_order/', views.setDeliveredOrder, name='set_delivered_order'),

    # Authentication url and paths
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),

    # Password reset paths
    path('reset-password/', 
    auth_views.PasswordResetView.as_view(
    template_name="password_reset.html",
    success_url=reverse_lazy('password_reset_done')
    ), 
    name="reset_password"),

    path('reset-password-sent/', 
    auth_views.PasswordResetDoneView.as_view(
    template_name="password_reset_sent.html"
    ), 
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(
    template_name="password_reset_form.html",
    success_url=reverse_lazy('password_reset_complete')
    ), 
    name="password_reset_confirm"),

    path('password-reset-complete', 
    auth_views.PasswordResetCompleteView.as_view(
    template_name="password_reset_complete.html"
    ), 
    name="password_reset_complete"),

    # Sitemap
    path('sitemap.xml/', sitemap, {'sitemaps':sitemaps}),
]