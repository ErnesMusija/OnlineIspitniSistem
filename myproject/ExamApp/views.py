from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from .models import *
from datetime import timedelta
from django.utils.crypto import get_random_string
from .forms import *
import random
from django.utils import timezone


# Create your views here.

def index(request):
    return render(request, 'index.html')


def napravi_pitanje(request, pk):

    trenutni_ispit = Ispit.objects.latest('id')
    broj_zadataka = trenutni_ispit.broj_zadataka
    broj_zaokruzi = trenutni_ispit.broj_zaokruzi_pitanja
    broj_pitanja = broj_zadataka + broj_zaokruzi

    if request.method == 'POST':
        pitanje_forma = PitanjeForma(request.POST)
        if pitanje_forma.is_valid():
            nova_pitanje_forma = pitanje_forma.save(commit=False)
            nova_pitanje_forma.ispit = trenutni_ispit
            nova_pitanje_forma.save()

    pitanje_forma = PitanjeForma()

    if request.method == 'POST':
        zaokruzi_forma = ZaokruziPitanjeForma(request.POST)
        if zaokruzi_forma.is_valid():
            nova_zaokruzi_forma = zaokruzi_forma.save(commit=False)
            nova_zaokruzi_forma.pitanje = Pitanja.objects.latest('id')
            nova_zaokruzi_forma.save()

    zaokruzi_forma = ZaokruziPitanjeForma()

    if pk > broj_zaokruzi:
        if request.method == 'POST':
            zadatak_forma = ZadatakPitanjeForma(request.POST)
            if zadatak_forma.is_valid():
                nova_zadatak_forma = zadatak_forma.save(commit=False)
                nova_zadatak_forma.pitanje = Pitanja.objects.latest('id')
                nova_zadatak_forma.save()

    zadatak_forma = ZadatakPitanjeForma()

    if broj_pitanja >= pk:
        pk = pk + 1

    max_bodovi = 0
    sva_pitanja = Pitanja.objects.filter(ispit=trenutni_ispit)

    for i in sva_pitanja:
        max_bodovi += i.max_bodovi

    context = {
        'pitanje_forma': pitanje_forma,
        'zaokruzi_forma': zaokruzi_forma,
        'pk': pk,
        'broj_pitanja': broj_pitanja,
        'zadatak_forma': zadatak_forma,
        'broj_zadataka': broj_zadataka,
        'broj_zaokruzi': broj_zaokruzi,
        'podaci': trenutni_ispit,
        'max_bodovi': max_bodovi,
    }

    return render(request, 'napravi_pitanje.html', context)


def napravi_ispit(request):
    if request.method == 'POST':
        ispit_forma = IspitForma(request.POST)
        if ispit_forma.is_valid():
            nova_ispit_forma = ispit_forma.save(commit=False)

            korisnikov_id = request.user.id
            nova_ispit_forma.zadavac = Zadavac.objects.get(user_id=korisnikov_id)
            nova_ispit_forma.ispitni_kod = get_random_string(9, allowed_chars='0123456789')
            nova_ispit_forma.save()

            return redirect('napravi_pitanje/0')

    ispit_forma = IspitForma()

    context = {
        'ispit_forma': ispit_forma,
    }
    return render(request, 'napravi_ispit.html', context)


def lista_ispita(request):
    korisnikov_id = request.user.id
    ispiti = Ispit.objects.filter(zadavac=korisnikov_id).order_by('-id')

    context = {
        'ispiti': ispiti,
    }
    return render(request, 'lista_ispita.html', context)


def ispit_page(request, pk):
    ispit = Ispit.objects.get(id=pk)
    context = {
        'ispit': ispit,
    }
    return render(request, 'ispit_page.html', context)


def pokrenut_ispit(request, ispit_id):
    ispit = Ispit.objects.get(id=ispit_id)
    ispit.pokrenut = True
    ispit.save()
    polagaci = Polaganje.objects.filter(ispit=ispit)
    context = {
        'ispit': ispit,
        'polagaci': polagaci,
    }
    return render(request, 'pokrenut_ispit.html', context)


def pridruzivanje_ispitu(request):
    if request.method == "POST":
        kod = request.POST['ispitni_kod']
        ispiti = Ispit.objects.all()

        # petlja krece od zadnjeg elementa jer su vece sanse da se nedavno dodani ispit zadaje

        pronadjen = False
        for ispit in reversed(ispiti):
            if ispit.ispitni_kod == kod:
                pronadjen = True
                ispit_id = ispit.id
                zadavac = ispit.zadavac
                korisnik = request.user
                ocjenjivanje, created = Ocjenjivanje.objects.get_or_create(ispit=ispit, polagac=korisnik.polagac, zadavac=zadavac)

                if ispit.pokrenut and created:
                    polaganje = Polaganje.objects.create(polagac=korisnik.polagac, ispit=ispit)
                    polaganje.save()
                    return redirect('izrada_ispita/0/{}'.format(ispit_id))
                elif ocjenjivanje.ocjenjen:
                    return redirect('pogledaj_rezultat/{}'.format(ispit_id))
                else:
                    return redirect('izrada_ispita/11/{}'.format(ispit_id))

        if not pronadjen:
            messages.info(request, "Pogresan kod")
            return redirect('pridruzivanje_ispitu')

    return render(request, 'pridruzivanje_ispitu.html')


def izrada_ispita(request, pk, ispit_id):

    korisnik = request.user
    ispit = Ispit.objects.get(id=ispit_id)
    polagac = korisnik.polagac
    zadavac = ispit.zadavac
    ocjenjivanje, created = Ocjenjivanje.objects.get_or_create(ispit=ispit, polagac=polagac, zadavac=zadavac)
    if created:
        ocjenjivanje.save()

    if request.method == "POST":
        pitanja = Pitanja.objects.filter(ispit=ispit)
        pitanje = pitanja[pk]

        if hasattr(pitanje, 'zaokruzi'):
            odgovor = request.POST['0']
            print(odgovor)
            if odgovor == pitanje.zaokruzi.tacan_odg:
                ocjenjivanje.osvojeni_bodovi = ocjenjivanje.osvojeni_bodovi + pitanje.max_bodovi
                print(odgovor)
                print(ocjenjivanje.osvojeni_bodovi)
                ocjenjivanje.save()

            else:
                ocjenjivanje.osvojeni_bodovi = ocjenjivanje.osvojeni_bodovi - pitanje.zaokruzi.izgubljeni_bodovi
                ocjenjivanje.save()

        else:
            odg = request.POST['odg']
            odgovor_zadatka = OdgovorZadatka.objects.create(zadatak=pitanje, polagac=polagac, ispit=ispit)
            odgovor_zadatka.odgovor = odg
            odgovor_zadatka.save()

        pk = pk + 1

        return redirect('/izrada_ispita/{}/{}'.format(pk, ispit_id))

    pitanja = Pitanja.objects.filter(ispit=ispit)
    ukupno_pitanja = ispit.broj_zadataka + ispit.broj_zaokruzi_pitanja
    zaokruzivanje = False

    if ispit.pokrenut:
        pitanje = pitanja[0]

        if pk < ukupno_pitanja:
            pitanje = pitanja[pk]

        ponudjeni_odgovori = []
        broj_ponudjenih_odgovora = 1
        rb_tacnog_odg = 0

        if hasattr(pitanje, 'zaokruzi'):
            zaokruzivanje = True
            if not pitanje.zaokruzi.odgovor1.strip() == '':
                broj_ponudjenih_odgovora += 1
                ponudjeni_odgovori.append(pitanje.zaokruzi.odgovor1)
            if not pitanje.zaokruzi.odgovor2.strip() == '':
                broj_ponudjenih_odgovora += 1
                ponudjeni_odgovori.append(pitanje.zaokruzi.odgovor2)
            if not pitanje.zaokruzi.odgovor3.strip() == '':
                broj_ponudjenih_odgovora += 1
                ponudjeni_odgovori.append(pitanje.zaokruzi.odgovor3)

            rb_tacnog_odg = random.randint(1, broj_ponudjenih_odgovora)
            ponudjeni_odgovori.insert(rb_tacnog_odg-1, pitanje.zaokruzi.tacan_odg)

        trajanje = pitanje.vrijeme_trajanja
        sekunde = trajanje.total_seconds()

        context = {
            'ispit': ispit,
            'pitanje': pitanje,
            'pk': pk,
            'rb_tacnog_odg': rb_tacnog_odg,
            'ponudjeni_odgovori': ponudjeni_odgovori,
            'ukupno_pitanja': ukupno_pitanja,
            'zaokruzi': zaokruzivanje,
            'sekunde': sekunde,
        }
    return render(request, 'izrada_ispita.html', context)


def neocjenjeni_ispiti(request):
    korisnik = request.user
    zadavac = korisnik.zadavac
    ispiti = Ocjenjivanje.objects.filter(zadavac=zadavac)
    neocjenjeni = []
    for i in ispiti:
        if not i.ocjenjen:
            neocjenjeni.append(i)

    context = {
        'ispiti': neocjenjeni,
    }
    return render(request, 'neocjenjeni_ispiti.html', context)


def ocjenjivanje_ispita(request, ocjenjivanje_id, pk):

    ocjenjivanje = Ocjenjivanje.objects.get(id=ocjenjivanje_id)
    polagac = ocjenjivanje.polagac
    ispit = ocjenjivanje.ispit
    odgovor_zadatka = OdgovorZadatka.objects.filter(polagac=polagac, ispit=ispit)
    duzina = len(odgovor_zadatka)
    trenutni_odgovor = odgovor_zadatka[0]

    if pk < duzina:
        trenutni_odgovor = odgovor_zadatka[pk]

    if request.method == "POST" and pk < duzina:
        bodovi = request.POST['bodovi']
        ocjenjivanje.osvojeni_bodovi += int(bodovi)
        ocjenjivanje.save()
        pk += 1
        return redirect('/ocjenjivanje_ispita/{}/{}'.format(ocjenjivanje_id, pk))

    if request.method == "POST" and pk == duzina:
        ocjena = request.POST['ocjena']
        napomena = request.POST['napomena']
        ocjenjivanje.ocjena = int(ocjena)
        ocjenjivanje.napomene = napomena
        ocjenjivanje.ocjenjen = True
        ocjenjivanje.save()
        pk += 1
        return redirect('/ocjenjivanje_ispita/{}/{}'.format(ocjenjivanje_id, pk))

    max_bodovi = 0
    sva_pitanja = Pitanja.objects.filter(ispit=ispit)

    for i in sva_pitanja:
        max_bodovi += i.max_bodovi

    context = {
        'odgovori': odgovor_zadatka,
        'duzina': duzina,
        'pk': pk,
        'trenutni_odgovor': trenutni_odgovor,
        'ocjenjivanje': ocjenjivanje,
        'ispit': ispit,
        'max_bodovi': max_bodovi,
    }
    return render(request, 'ocjenjivanje_ispita.html', context)


def pogledaj_rezultat(request, ispit_id):
    ispit = Ispit.objects.get(id=ispit_id)
    korisnik = request.user
    ocjenjivanje = Ocjenjivanje.objects.get(ispit=ispit, polagac=korisnik.polagac)
    sva_pitanja = Pitanja.objects.filter(ispit=ispit)
    max_bodovi = 0

    for i in sva_pitanja:
        max_bodovi += i.max_bodovi

    max_ocjena = ispit.max_ocjena

    context = {
        'ocjenjivanje': ocjenjivanje,
        'sva_pitanja': sva_pitanja,
        'max_bodovi': max_bodovi,
        'max_ocjena': max_ocjena,
    }
    return render(request, 'pogledaj_rezultat.html', context)


def registration(request):
    User = get_user_model()
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        ime = request.POST['name']
        prezime = request.POST['lastname']
        rola = request.POST['acc_type']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect('registration')

            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already in use")
                return redirect('registration')

            else:
                korisnik = User.objects.create_user(username=username, email=email, password=password, ime=ime,
                                                    prezime=prezime, role=rola)

                if korisnik.role == 'P':
                    korisnik.is_active = True
                    korisnik.save()
                    p1 = Polagac(user=korisnik)
                    p1.save()

                elif korisnik.role == 'Z':
                    korisnik.is_active = True
                    korisnik.save()
                    z1 = Zadavac(user=korisnik)
                    z1.save()

                return redirect('login')

        else:
            messages.info(request, "Password not the same")
            return redirect('registration')
    else:
        return render(request, 'registration.html')


def login(request):
    if request.method == "POST":

        password = request.POST['password']
        email = request.POST['email']

        korisnik = auth.authenticate(email=email, password=password)

        if korisnik is not None:
            auth.login(request, korisnik)
            return redirect('index')

        else:
            messages.info(request, "Pogresni kredencijali")
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')

