from django.contrib import admin
from django.urls import path, include
from mainapp.views import PlayerColumn, SignUp
from mainapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', PlayerColumn.as_view(), name='index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('registration/', include('social_django.urls', namespace='social')),
    path('makechoice/<int:player_id>/', views.create_choice, name='makechoice'),
    path('randomchoice/', views.random_choice, name='randomchoice'),
]
