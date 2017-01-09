from django.conf.urls import url

from budget import views

urlpatterns = (
    url(r'^$', views.main),
)
