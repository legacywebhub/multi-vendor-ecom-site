# About
This is an agro based multi-vendor ecommerce web app made with javascript, python/django for backend.
It has total of 20+ pages which includes index, register/login, profile, cart,
special offer, checkout, contact, faq, legal notice, tac(terms & condition),
product detail, product category, error pages(404 and 500) and password reset pages.

Users register as buyers and have option to upgrade to a vendor or seller by completing their KYC
and getting approved. Vendors can see their details, kyc status, orders, pending delivery (per order item)
and manage products on their dashboard. The ecom site act as an escrow so vendors can only be paid after
customers confirm they have received good by clicking a confirmation button on the order via the dashboard.
Customers can also access vendors profile information via product detail page and also other vendor products
 
# Features
* Cart functionality with javascript.
* Product images have url slot to fetch images from external sources to save server
  bandwidth.
* Special offers page which includes products with discount of 15% and above and free
  shipping.
* Visitors can make purchases without signing up but can't have access to special offers.
* Payment integration with paystack and paypal.
* Error 404 and 500 pages implemented to handle error pages.
* Password reset functionality.
* Sitemap to boost SEO.
* Newsletter functionality
* Configured to use cloudinary cloud storage to serve media files.
* Secured.

# Libraries/Packages
python-3.7
dj-database-url==0.5.0
Django==3.2.2
gunicorn==20.1.0
Pillow==9.2.0
django-cloudinary-storage==0.3.0
django-heroku==0.3.1
psycopg2==2.9.3
python-magic==0.4.25(online/live/hosted) / python-magic-bin==0.4.14(offline for windows os)
python-decouple==3.6
whitenoise==5.3.0
django-pandas==0.6.6
django-crispy-forms==1.8

# Images
images for products should be of consistent size(width x height)
to avoid layout distort. default image dimension for products is 160x160(WxL).
Navbar Logo should be white if needed.