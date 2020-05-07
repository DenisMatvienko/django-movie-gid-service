from django.contrib import admin

from .models import Contact


#   Форма полученных email-ов в админке
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')
