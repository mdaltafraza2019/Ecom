"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from shop.views import*
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('login/',loginfun,name='login'),
    path('logout/',logoutfun,name='logout'),
    path('register/',register,name='register'),
    path('single/<int:id>/',single,name='single'),
    path('category/<slug>/',category,name='category'),
    path('addtocart/<slug>/',addtocart,name='addtocart'),
    path('removefromcart/<slug>/',removeFromcart,name='removefromcart'),
    path('delte_from_cart/<int:id>/',deletefromcart,name='deltefromcart'),
    path('delte_from_order/<int:id>/',deletefromOrder,name='deltefromorder'),
    path('cart/',cart,name='cart'),
    path('addcoupon/',addCoupon,name='addcoupon'),
    path('removecoupon/',remove_coupon,name='removecoupon'),
    path('chekout/',chekout,name='chekout'),
    path('search/',search,name='search'),
    path('chekoutwithaddress/',chekout_with_save_address,name='chekoutwith'),
    path('pay/',pay_now,name='paynow'),
    path('myorder/',my_order,name='myorder')
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

