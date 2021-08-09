from django.urls import path
from django.urls.conf import include
from .views_signin import signout,phone,sms
from .views_cart import verify,send_request
from .views_user import user,  save_serial, save_movie
from .views_create import (
                create_review_movie, create_review_serial, admin_create,
                create_movie, create_category, create_related_serial,
                create_serial, create_session,
            )
from .views_edit import (
                edit_review, edit_serial, edit_session, 
                edit_movie, edit_category, edit_relted_serial,

            )
from .views import (
                    serial, serial_single, review, session,
                    contact, about, search, index,
                    collection, film, singel_review,
                    change_language
                )


app_name = 'movie'

create_urlpatters = [
    path('', admin_create, name='create'),
    path('movie/', create_movie, name='create_movie'),
    path('serial/', create_serial, name='create_serial'),
    path('session/', create_session, name='create_session'),
    path('category/', create_category, name='create_category'),
    path('review/movie/', create_review_movie, name='create_review_movie'),
    path('review/serial/', create_review_serial, name='create_review_serial'),
    path('related/serial/', create_related_serial, name='create_related_serial'),
]

edit_urlpatterns = [
    path('movie/', edit_movie, name='edit_movie'),
    path('serial/', edit_serial, name='edit_serial'),
    path('review/', edit_review, name='edit_review'),
    path('session/', edit_session, name='edit_session'),
    path('category/', edit_category, name='edit_category'),
    path('related/serial/', edit_relted_serial, name='edit_related_serial'),
]

save_urlpatterns = [
    path('movie/<str:slug>/',save_movie,name='save_movie'),
    path('seria/<str:slug>/',save_serial,name='save_serial'),
]

urlpatterns = [
    path('sms/',sms , name='sms'),
    path('', index, name='index'),
    path('user/',user , name='user'),
    path('about/', about, name='about'),
    path('phone/',phone , name='phone'),
    path('review/', review, name='review'),
    path('search/',search , name='search'),
    path('logout/',signout , name='logout'),
    path('verify/', verify , name='verify'),
    path('contact/', contact, name='contact'),   
    path('film/<str:slug>/', film, name='film'),
    path('request/', send_request, name='request'),
    path('serial/<str:slug>/', serial, name='serial'),
    path('collection/', collection, name='collection'),
    path('session/<str:slug>/',session , name='session'),
    path('change_language/',change_language, name='change_language'),
    path('serial/singel/<str:slug>/', serial_single, name='serial_single'),
    path('serial_singlle/<str:slug>/', serial_single, name='serial_single'),
    path('singel/review/<str:slug>/', singel_review , name='singel_review'),

    path('save/',include(save_urlpatterns)),
    path('edit/', include(edit_urlpatterns)),
    path('create/', include(create_urlpatters)),
]