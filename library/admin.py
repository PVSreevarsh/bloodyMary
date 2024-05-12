from django.contrib import admin
from .models import Investment,Bank,Sector,SME

# Register your models here.
admin.site.register(Investment)
admin.site.register(Bank)
admin.site.register(Sector)
admin.site.register(SME)
