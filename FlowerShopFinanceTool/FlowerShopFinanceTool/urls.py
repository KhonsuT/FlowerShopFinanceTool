"""
URL configuration for FlowerShopFinanceTool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from . import settings
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.homePage, name="homepage"),
    path("generate_invoice/", views.invoiceQuery, name="generate_invoice"),
    path("search/", views.search, name="search"),
    path("addFlower/" , views.addFlower, name="addFlower"),
    path("addPrice/", views.updatePrice,name="addPrice"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
