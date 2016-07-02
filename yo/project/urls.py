from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^budget/', include('budget.urls')),
    url(r'^admin/', admin.site.urls)
]

admin.site.site_header = '~ django, yo ~'
admin.site.index_title = '~ django, yo ~'