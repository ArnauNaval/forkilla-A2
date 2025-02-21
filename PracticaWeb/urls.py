"""PracticaWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf.urls import (handler404, handler500)
from forkilla import views



from django.conf.urls import url, include
from rest_framework import routers
from forkilla import views


router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'reviews', views.ReviewViewSet)


handler404 = views.error_404
handler500 = views.error_500

listOfAddresses = ["sd2019-forkilla-a2","sd2019-f8-forkilla","sd2019-forkillaa7","sd2019-forkillaa9","sd2019-forkillab2","sd2019-forkillab8","sd2019-forkillab9","sd2019-forkillab11","sd2019-f2-forkilla","sd2019-forkillaf6","sd2019-forkillaf11","sd2019-forkilla-a6","sd2019-f4-forkilla", "sd2019-forkilla-b5", "sd2019-forkilla-b6"]

urlpatterns = [
    url(r'^forkilla/', include('forkilla.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('forkilla.urls')),
    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$',  logout,  {'next_page': '/'}, name='logout'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^comparator$', views.comparator, {'ips': listOfAddresses}),
]
print(router.urls)
