"""ar_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from shop.views import home_page, about_us_page, contact_page, cart_page, register_page, product_details_page, shop_page, updateItem, processOrder, checkout_page

urlpatterns = [
    path('', home_page, name='home'),
    path('product-details/<str:pk>/', product_details_page, name='product-details'),    
    path('cart/', cart_page, name='cart'),
    path('checkout/', checkout_page, name='checkout'),
    path('update_item/', updateItem, name='update_item'),
    path('process_order/', processOrder, name='process_order'),
    path('shop/<str:pk>/', shop_page, name='shop'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('register/', register_page, name='register'),
    path('about-us/', about_us_page, name='about-us'),
    path('contact/', contact_page, name='contact'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
