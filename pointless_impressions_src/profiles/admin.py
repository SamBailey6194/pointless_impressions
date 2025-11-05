from django.contrib import admin
from .models import Customer, Artist


# Register your models here.
class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'Customer Profile'


class ArtistInline(admin.StackedInline):
    model = Artist
    can_delete = False
    verbose_name_plural = 'Artist Profile'
