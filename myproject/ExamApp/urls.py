from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('napravi_ispit', views.napravi_ispit, name="napravi_ispit"),
    path('napravi_pitanje/<int:pk>', views.napravi_pitanje, name="napravi_pitanje"),
    path('lista_ispita', views.lista_ispita, name="lista_ispita"),
    path('ispit_page/<int:pk>', views.ispit_page, name="ispit_page"),
    path('pokrenut_ispit/<int:ispit_id>', views.pokrenut_ispit, name="pokrenut_ispit"),
    path('pridruzivanje_ispitu', views.pridruzivanje_ispitu, name="pridruzivanje_ispitu"),
    path('izrada_ispita/<int:pk>/<int:ispit_id>', views.izrada_ispita, name="izrada_ispita"),
    path('ocjenjivanje_ispita/<int:ocjenjivanje_id>/<int:pk>', views.ocjenjivanje_ispita, name="ocjenjivanje_ispita"),
    path('neocjenjeni_ispiti', views.neocjenjeni_ispiti, name="neocjenjeni_ispiti"),
    path('pogledaj_rezultat/<int:ispit_id>', views.pogledaj_rezultat, name="pogledaj_rezultat"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # za slike

