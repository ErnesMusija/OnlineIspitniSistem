from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
from django.utils.crypto import get_random_string
from datetime import timedelta

# Create your models here.


class Manager(BaseUserManager):

    def create_superuser(self, email, username, password, ime, prezime, role, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, ime, prezime, role, **other_fields)

    def create_user(self, email, username, password, ime, prezime, role, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, ime=ime, prezime=prezime, role=role, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=80, unique=True)

    ime = models.CharField(max_length=25)
    prezime = models.CharField(max_length=25)
    broj_telefona = models.CharField(max_length=15, blank=True)

    date_of_birth = models.DateField(blank=True, null=True)

    Zadavac = 'Z'
    Polagac = 'P'

    ROLE = [
        (Zadavac, 'Zadavac'),
        (Polagac, 'Polagac'),
    ]

    role = models.CharField(max_length=1, choices=ROLE, default=Polagac,)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'ime', 'prezime', 'role']

    def __str__(self):
        return self.username


class Zadavac(models.Model):
    broj_ispita = models.IntegerField(default=0)
    broj_neocjenjenih_ispita = models.IntegerField(default=0)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Polagac(models.Model):
    broj_polaganih_ispita = models.IntegerField(default=0)
    prosjecna_ocjena = models.IntegerField(default=0)
    broj_polozenih_ispita = models.IntegerField(default=0)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Ispit(models.Model):

    naziv_ispita = models.CharField(max_length=40)
    ispitni_kod = models.CharField(max_length=10)
    ukupan_broj_polagaca = models.IntegerField(default=0)
    vrijeme_trajanja = models.DurationField(default=timedelta(seconds=300))
    broj_inicijalizacija = models.IntegerField(default=0)
    oblast_ispita = models.CharField(max_length=40, blank=True)
    max_ocjena = models.IntegerField(default=5)
    min_ocjena = models.IntegerField(default=1)
    broj_zaokruzi_pitanja = models.IntegerField(default=0)
    broj_zadataka = models.IntegerField(default=0)
    zadavac = models.ForeignKey(Zadavac, on_delete=models.CASCADE)
    datum_formiranja = models.DateTimeField(auto_now_add=True)
    pokrenut = models.BooleanField(default=False)

    def __str__(self):
        return self.naziv_ispita


class Pitanja(models.Model):
    id = models.AutoField(primary_key=True)
    tekst = models.CharField(max_length=500)
    max_bodovi = models.IntegerField(default=10)
    vrijeme_trajanja = models.DurationField(default=timedelta(seconds=30))
    oblast_Pitanja = models.CharField(max_length=60, blank=True)
    ispit = models.ForeignKey(Ispit, on_delete=models.CASCADE)

    def __str__(self):
        return 'Pitanje' + str(self.id)


class Zaokruzi(models.Model):
    odgovor1 = models.CharField(max_length=250)
    odgovor2 = models.CharField(max_length=250, blank=True)
    odgovor3 = models.CharField(max_length=250, blank=True)
    tacan_odg = models.CharField(max_length=250)
    izgubljeni_bodovi = models.IntegerField(default=0)  # Izgubljeni bodovi na ne tacnom odgovoru
    pitanje = models.OneToOneField(Pitanja, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'Zaokruzi' + str(self.pitanje.id)


class Zadatak(models.Model):
    default_tacan_odg = models.CharField(max_length=500, blank=True)
    pitanje = models.OneToOneField(Pitanja, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'Zadatak' + str(self.pitanje.id)


class Polaganje(models.Model):
    polagac = models.ForeignKey(Polagac, on_delete=models.CASCADE)
    ispit = models.ForeignKey(Ispit, on_delete=models.CASCADE)
    datum_polaganja = models.DateTimeField(auto_now_add=True)
    vrijeme_pocetka = models.TimeField(auto_now_add=True)
    vrijeme_kraja = models.TimeField(blank=True, null=True)


class Ocjenjivanje(models.Model):
    class Meta:
        unique_together = (('zadavac', 'polagac', 'ispit'),)

    zadavac = models.ForeignKey(Zadavac, on_delete=models.CASCADE)
    polagac = models.ForeignKey(Polagac, on_delete=models.CASCADE)
    ispit = models.ForeignKey(Ispit, on_delete=models.CASCADE)
    ocjena = models.IntegerField(default=1)
    osvojeni_bodovi = models.IntegerField(default=0)
    napomene = models.CharField(max_length=100, blank=True)
    datum_rezultata = models.DateTimeField(auto_now_add=True)
    ocjenjen = models.BooleanField(default=False)


class OdgovorZadatka(models.Model):
    class Meta:
        unique_together = (('zadatak', 'polagac'),)

    zadatak = models.ForeignKey(Pitanja, on_delete=models.CASCADE)
    polagac = models.ForeignKey(Polagac, on_delete=models.CASCADE)
    ispit = models.ForeignKey(Ispit, on_delete=models.CASCADE)
    odgovor = models.CharField(max_length=500)






















