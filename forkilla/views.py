from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta
from rest_framework import viewsets
from .serializers import RestaurantSerializer , ReviewSerializer
from forkilla.permissions import IsOwnerOrReadOnly
from rest_framework import permissions



def index(request):
    restaurants_by_city = Restaurant.objects.filter(is_promot="True")
    promoted = True

    context = {
        'restaurants': restaurants_by_city,
        'promoted': promoted,
        'viewedrestaurants': _check_session(request),
        'logged': request.user.is_authenticated(),
        'username':request.user.username
    }
    return render(request, 'forkilla/index.html', context)

def restaurants(request, city="", category = ""):
    promoted = False
    if request.GET.get('city') is not None:
        city = request.GET['city']

    if city:
        restaurants_by_city = Restaurant.objects.filter(city__iexact=city)

        if category:
            restaurants_by_city = restaurants_by_city.filter(category__iexact=category)


    else:
        restaurants_by_city = Restaurant.objects.filter(is_promot="True")
        promoted = True

    context = {
        'city': city,
        'category': category,
        'restaurants': restaurants_by_city,
        'viewedrestaurants': _check_session(request),
        'promoted': promoted,
        'logged': request.user.is_authenticated(),
        'username':request.user.username
    }
    return render(request, 'forkilla/restaurants.html', context)

def details(request,restaurant_number):

    try:
        viewedrestaurants = _check_session(request)
        restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
        while (len(viewedrestaurants.restaurant.all()) >= 5):
            viewedrestaurants.restaurant.remove(viewedrestaurants.restaurant.first())
        viewedrestaurants.restaurant.add(restaurant)

        reviews = Review.objects.filter(restaurant=restaurant)
        puntuacio = 0
        for i in reviews:
            puntuacio += i.rate

        if puntuacio != 0:
            puntuacio = round(puntuacio/reviews.count())

        if restaurant.featured_photo != "":
            foto = restaurant.featured_photo.url[16:]
        else:
            foto = ""

        context = {
            'restaurants': restaurant,
            'viewedrestaurants': viewedrestaurants,
            'reviews' : reviews,
            'puntuacio' : puntuacio,
            'next_url': "/restaurant/"+restaurant.restaurant_number,
            'logged': request.user.is_authenticated(),
            'username':request.user.username,
            'foto' : foto,
        }

        return render(request, 'forkilla/details.html', context)

    except Restaurant.DoesNotExist:

        return render(request, 'forkilla/error.html')

@login_required
def reservation(request):
    try:
        if request.method == "POST":
            form = ReservationForm(request.POST)
            if form.is_valid():
                restaurant_number = request.session["reserved_restaurant"]
                restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
                # Agafem totes les reserves per el mateix dia a la mateixa hora
                day = form.data["day"]
                time_slot = form.data["time_slot"]
                reserves = Reservation.objects.filter(restaurant=restaurant).filter(day=day).filter(time_slot=time_slot)
                # Contem la quantitat de persones que han reservat
                persones = 0
                for i in reserves:
                    persones += i.num_people

                # Si la nova reserva hi cap, tirem endevant
                if int(form.data['num_people']) + persones <= restaurant.capacity:
                    resv = form.save(commit=False)
                    resv.restaurant = restaurant
                    resv.user = request.user
                    resv.save()
                    request.session["reservation"] = resv.id
                    request.session["result"] = "OK"
                else:
                    return render(request, 'forkilla/error.html')
            else:
                  request.session["result"] = form.errors
            return HttpResponseRedirect(reverse('checkout'))

        elif request.method == "GET":
            restaurant_number = request.GET["reservation"]
            restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
            request.session["reserved_restaurant"] = restaurant_number

            viewedrestaurants = _check_session(request)

            while(len(viewedrestaurants.restaurant.all()) >= 5):
                viewedrestaurants.restaurant.remove(viewedrestaurants.restaurant.first())

            viewedrestaurants.restaurant.add(restaurant)

            form = ReservationForm()
            context = {
                'restaurant': restaurant,
                'viewedrestaurants': viewedrestaurants,
                'form': form,
                'next_url': "/restaurant/" + restaurant_number,
                'logged': request.user.is_authenticated(),
                'username':request.user.username
            }
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant Does not exists")
    return render(request, 'forkilla/reservation.html', context)

def _check_session(request):

    if "viewedrestaurants" not in request.session:
        viewedrestaurants = ViewedRestaurants()
        viewedrestaurants.save()
        request.session["viewedrestaurants"] = viewedrestaurants.id_vr
    else:
        viewedrestaurants = ViewedRestaurants.objects.get(id_vr=request.session["viewedrestaurants"])
    return viewedrestaurants

def checkout(request):

    resv_id = request.session["reservation"]
    reservation = Reservation.objects.get(id = resv_id)

    context ={
        'restaurant': reservation.restaurant.name,
        'day': reservation.day,
        'time': Reservation._d_slots[reservation.time_slot],
        'people':reservation.num_people,
        'viewedrestaurants' : _check_session(request),
        'logged': request.user.is_authenticated()   ,
        'username':request.user.username
    }

    return render(request, 'forkilla/checkout.html', context)

@login_required()
def reviews(request):
    try:
        if request.method == "POST":
            form = ReviewForm(request.POST)

            if form.is_valid():

                restaurant_number = request.session["reviewed_restaurant"]
                restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)

                rev = form.save(commit=False)
                rev.restaurant = restaurant
                rev.user = request.user
                rev.save()
                request.session["review"] = rev.id
                request.session["result"] = "OK"

            else:
                request.session["result"] = form.errors
            return HttpResponseRedirect(reverse('checkreview'))

        elif request.method == "GET":

            restaurant_number = request.GET["review"]
            restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
            request.session["reviewed_restaurant"] = restaurant_number

            form = ReviewForm()
            context = {
                'restaurant': restaurant,
                'viewedrestaurants': _check_session(request),
                'form': form,
                'next_url': "/restaurant/" + restaurant_number,
                'logged': request.user.is_authenticated(),
                'username':request.user.username
            }
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant Does not exists")
    return render(request, 'forkilla/reservation.html', context)

def checkreview(request):

    rev_id = request.session["review"]
    review = Review.objects.get(id=rev_id)

    context = {
        'restaurant': review.restaurant.name,
        'username': review.user.username,
        'message': review.message,
        'rate': review.rate,
        'viewedrestaurants': _check_session(request),
        'logged': request.user.is_authenticated()
    }

    return render(request, 'forkilla/checkreview.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, 'forkilla/register.html', {
        'form': form,
    })

def error_404(request):
    context = {
        'username': request.user.username,
        'viewedrestaurants': _check_session(request),
        'logged': request.user.is_authenticated()
    }
    return render(request, 'forkilla/error_404.html', context)


def error_500(request):
    context = {
        'username': request.user.username,
        'viewedrestaurants': _check_session(request),
        'logged': request.user.is_authenticated()
    }
    return render(request, 'forkilla/error_500.html', context)

@login_required()
def reservationlist(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user, day__gte=datetime.now().date()).order_by('day')
    reservations_old = Reservation.objects.filter(user=user, day__lte=(datetime.now().date() - timedelta(1))).order_by('day')
    context = {
        'username' : request.user.username,
        'reservations' : reservations,
        'old_reservations': reservations_old,
        'viewedrestaurants': _check_session(request),
        'logged': request.user.is_authenticated(),
    }
    return render(request, 'forkilla/reservationlist.html', context)

@login_required()
def cancellation(request):
    context = { }
    if request.method == "GET":
        id = request.GET["cancellation"]
        reserva = Reservation.objects.get(id=id)

        Reservation.objects.filter(id=id).delete()

        context={
            'username': request.user.username,
            'logged': request.user.is_authenticated(),
            'reserva' : reserva,
        }
    return render(request,'forkilla/cancellation.html', context)


@login_required()
def reviewBefore(request):
    try:
        if request.method == "POST":
            form = ReviewForm(request.POST)

            if form.is_valid():

                restaurant_number = request.session["reviewed_restaurant"]
                restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)

                rev = form.save(commit=False)
                rev.restaurant = restaurant
                rev.user = request.user
                rev.save()
                request.session["review"] = rev.id
                request.session["result"] = "OK"

            else:
                request.session["result"] = form.errors
            return HttpResponseRedirect(reverse('checkreview'))

        elif request.method == "GET":

            id = request.GET["review"]
            reserva = Reservation.objects.get(id=id)

            Reservation.objects.filter(id=id).delete()

            restaurant_number = reserva.restaurant.restaurant_number
            restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
            request.session["reviewed_restaurant"] = restaurant_number


            form = ReviewForm()
            context = {
                'restaurant': restaurant,
                'viewedrestaurants': _check_session(request),
                'form': form,
                'next_url': "/restaurant/" + restaurant_number,
                'logged': request.user.is_authenticated(),
                'username': request.user.username
            }
    except Reservation.DoesNotExist:
        return HttpResponse("Reservation Does not exists")
    return render(request, 'forkilla/reservation.html', context)

def comparator(request,ips):
    context = {
        'ips':ips
    }
    return render(request, 'forkilla/ConsultaWeb.html',context)


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Restaurants to be viewed or edited.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    serializer_class = RestaurantSerializer
    #queryset = Restaurant.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Restaurant.objects.all()
        city = self.request.query_params.get('city', None)
        category = self.request.query_params.get('category', None)
        price = self.request.query_params.get('price_average', None)

        if city is not None:
            queryset = queryset.filter(city=city)

        if category is not None:
            queryset = queryset.filter(category=category)

        if price is not None:
            queryset = queryset.filter(price_average__gte = 0,price_average__lte=price)

        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Restaurants to be viewed or edited.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
