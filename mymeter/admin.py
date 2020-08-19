from django.contrib import admin
from .models import accounts,meters, transactions

# Register your models here.

admin.site.register(accounts)
admin.site.register(meters)
admin.site.register(transactions)


