from django.conf.urls import url

from . import views

listOfAddresses = ["161.116.56.65","161.116.56.165","127.0.0.1"]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^restaurants/$', views.restaurants, name='restaurants'),
    url(r'^restaurants/(?P<city>.*)/$', views.restaurants, name='restaurants'),
    url(r'^restaurant/(?P<restaurant_number>.*)/$', views.details, name='restaurant'),
    url(r'^restaurants/(?P<city>.*)/(?P<category>.*)$',views.restaurants ,name = 'restaurants'),
    url(r'^reservation/$', views.reservation, name='reservation'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^reviews/$', views.reviews, name='reviews'),
    url(r'^checkreview/$', views.checkreview, name='checkreview'),
    url(r'^register/$', views.register, name='register'),
    url(r'^reservationlist/$', views.reservationlist, name='reservationlist'),
    url(r'^cancellation/$', views.cancellation, name='cancellation'),
    url(r'^reviewBefore/$', views.reviewBefore, name='reviewBefore'),
    url(r'^comparator$', views.comparator, {'ips': listOfAddresses}),
]