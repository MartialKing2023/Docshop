"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from store.views import index, product_detail, add_to_cart, cart, cart_quantity_update, delete_cart
from accounts.views import login_user, signup, logout_user

from shop import settings

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('cart/', cart, name="cart"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart', add_to_cart, name="add-to-cart"),
    path('product/<str:slug>/cart-quantity-update', cart_quantity_update, name="cart-quantity-update"),
    path('comment/', include('comments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
