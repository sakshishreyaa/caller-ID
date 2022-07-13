from django.contrib import admin

# Register your models here.
from callerIDapp.models import CustomUser,Phonebook,SpamNumbers

admin.site.register(CustomUser)
admin.site.register(Phonebook)
admin.site.register(SpamNumbers)