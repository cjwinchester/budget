from django.conf.urls import url

from budget import views

urlpatterns = (
    url(r'^recipients/(?P<pk>[\d]+)/$', views.recipient, name="recipient-view"),
    url(r'^spending/(?P<exp_id>[\d]+)/$', views.expense, name="expense-view"),
    url(r'^categories/$', views.category_index, name="category-index-view"),
    url(r'^categories/(?P<pk>[\d]+)/$', views.category, name="category-view"),
    url(r'^(?P<year>[\d]{4})/(?P<month>[0-1]?[0-9])/(?P<day>[0-3]?[0-9])/$', views.day, name="day-view"),
    url(r'^(?P<year>[\d]{4})/(?P<month>[0-1]?[0-9])/$', views.month, name="month-view"),
    url(r'^(?P<year>[\d]{4})/$', views.year, name="year-view"),
    url(r'^search/$', views.search, name="search-view"),
    url(r'^$', views.main),
)