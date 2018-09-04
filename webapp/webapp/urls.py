"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from rest_framework import routers
from tasks import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'markets/treasury-bond-future-market-by-ten-years',
                views.TreasuryBondFutureMarketByTenYearsViewSet,
                base_name='treasury-bond-future-market-by-ten-years')
router.register(r'trade/bond/buy-transaction-by-holding',
                views.BondBuyTransactionByHoldingViewSet,
                base_name='buy-transaction-by-holding')
router.register(r'trade/bond/buy-transaction-by-type',
                views.BondBuyTransactionByTypeViewSet,
                base_name='buy-transaction-by-type')
router.register(r'trade/bond/sale-transaction-by-holding',
                views.BondSaleTransactionByHoldingViewSet,
                base_name='sale-transaction-by-holding')
router.register(r'trade/bond/sale-transaction-by-type',
                views.BondSaleTransactionByTypeViewSet,
                base_name='sale-transaction-by-type')
router.register(r'trade/bond/net-transaction-by-holding',
                views.BondNetTransactionByHoldingViewSet,
                base_name='net-transaction-by-holding')
router.register(r'trade/bond/net-transaction-by-type',
                views.BondNetTransactionByTypeViewSet,
                base_name='net-transaction-by-type')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api/v1/', include('tasks.urls')),
]
