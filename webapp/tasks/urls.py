from django.conf.urls import url
from tasks import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # vurl(r'^treasury-bond-future-market-by-ten-years/$',
    #     views.treasury_bond_future_market_by_ten_years_list),
    url(r'^/market/treasury-bond-future-market-by-ten-years/$',
        views.TreasuryBondFutureMarketByTenYearsList.as_view()),
    # url(r'^treasury-bond-future-market-by-ten-years/(?P<pk>[0-9]+)/$',
    #     views.treasury_bond_future_market_by_ten_years_detail),
    #url(r'^treasury-bond-future-market-by-ten-years/(?P<pk>[0-9]+)/$',
    #    views.TreasuryBondFutureMarketByTenYearsDetail.as_view()),
    # url(r'^treasury-bond-future-market-by-ten-years/(?P<pk>[0-9]+)/$',
    #    views.TreasuryBondFutureMarketByTenYearsDetailMixins.as_view()),
    url(r'^/market/treasury-bond-future-market-by-ten-years/(?P<pk>[0-9]+)/$',
        views.TreasuryBondFutureMarketByTenYearsDetailGeneric.as_view(),
        name='treasury-bond-future-market-by-ten-years-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)