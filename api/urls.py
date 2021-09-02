from django.urls import path, include
from .views import admin_controller, index, category_create, contact_us, send_email, submit_email, save_serial, save_movie
from .view_movie import movie_list, movie_detail,movie_all_list,movie_create, movie_edit
from .view_user import phone, sms, signout, profile
from .view_review import create_review_movie,create_review_serial,review_list,review_movie_detail,review_serial_detail, edit_review
from .view_serial import (
                create_serial_film, edit_serial, serial_list,
                serial_detail,serial_all_list, create_serial,create_session, 
                create_serial_film, edit_serial,edit_session, edit_serial_film
            )

app_name = 'api'

review_urlpatterns = [
    path('',review_list, name='review_list'),
    path('create/movie/<int:pk>/', create_review_movie, name='create_review_movie'),
    path('create/serial/<int:pk>/', create_review_serial, name='create_review_serial'),
    path('movie/<str:slug>/', review_movie_detail, name='review_movie_detail'),
    path('serial/<str:slug>/', review_serial_detail, name='review_serial_detail'),
    path('edit/<str:slug>/',edit_review , name='edit_review'),
] 

movie_patterns = [
    path('list/<str:choice>/', movie_list , name='movie_list'),
    path('detail/<str:slug>/', movie_detail , name='movie_detail'),
    path('', movie_all_list, name="movie_all_list" ),
    path('create/',movie_create,name="movie_create"),
    path('edit/<str:slug>/',movie_edit,name="movie_edit"),
]

serial_patterns = [
    path('list/<str:choice>/', serial_list , name='serial_list'),
    path('', serial_all_list, name="serial_all_list" ),
    path('detail/<str:slug>/', serial_detail , name='serial_detail'),
    path('create/session/<str:slug>/', create_session , name='create_session'),
    path('film/create/<int:pk>/<str:slug>/', create_serial_film , name='create_serial_film'),
    path('create/', create_serial , name='serial_create'),
    path('edit/<str:slug>/', edit_serial , name='serial_edit'),
    path('edit/session/<int:pk>/', edit_session , name='session_edit'),
    path('edit/serial_film/<int:pk>/', edit_serial_film , name='serial_film_edit'),
]

save_patterns = [
    path('serial/<str:slug>/',save_serial, name="save_serial"),
    path('movie/<str:slug>/',save_movie, name="save_movie"),
]


urlpatterns = [
    path('', index , name='index'),
    path('submit/email/', submit_email , name='submit_email'),
    path('admin/controller/', admin_controller, name='admin_controller'),
    path('category/create/',  category_create, name='category_create'),
    path('contactus/',  contact_us, name='contact_us'),
    path('send_email/',send_email,name="send_email"),
    path('phone/', phone, name="phone"),
    path('sms/', sms ,name="sms"),
    path('signout/', signout ,name="signout"),
    path('profile/', profile ,name="profile"),

    path('movie/', include(movie_patterns)),
    path('serial/', include(serial_patterns)),
    path('review/', include(review_urlpatterns)),
    path('save/', include(save_patterns)),

]