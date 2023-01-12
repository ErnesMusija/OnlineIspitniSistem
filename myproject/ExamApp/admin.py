from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(MyUser)
admin.site.register(Polagac)
admin.site.register(Zadavac)
admin.site.register(Pitanja)
admin.site.register(Zadatak)
admin.site.register(Zaokruzi)
admin.site.register(Ocjenjivanje)
admin.site.register(Polaganje)
admin.site.register(Ispit)
admin.site.register(OdgovorZadatka)

