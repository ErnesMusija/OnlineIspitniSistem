from django import forms
from .models import *


class PitanjeForma(forms.ModelForm):

    class Meta:
        model = Pitanja
        exclude = ['ispit']
        # ekskludaj rb u ispitu i automatski ga povecavaj
        # promjeni imena ona za unos ofo ono
        # unos pitanja u formi treba automatski podrazumjevat
        # prvo pitaj jel zadatak ili je zaokruzi
        # ako zaokruzi onda ponudi za njega forme, ako zadatak za njega
        # spremi u bazu i nudi sljedece pitanje opciju

        # ILI ponudi odma broj pitanja i broj zaokruzi, broj zadataka
        # mozda moram krispi forms odma


class ZaokruziPitanjeForma(forms.ModelForm):

    class Meta:
        model = Zaokruzi
        exclude = ['pitanje']


class ZadatakPitanjeForma(forms.ModelForm):

    class Meta:
        model = Zadatak
        exclude = ['pitanje']


class IspitForma(forms.ModelForm):

    class Meta:
        model = Ispit
        fields = ['naziv_ispita', 'oblast_ispita', 'max_ocjena', 'min_ocjena', 'broj_zaokruzi_pitanja', 'broj_zadataka']




        
