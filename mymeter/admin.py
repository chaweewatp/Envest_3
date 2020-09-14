from django.contrib import admin
from .models import accounts, meters, time_slot, measure_data, sub_area, transactions

# Register your models here.

admin.site.register(accounts)
admin.site.register(meters)
admin.site.register(transactions)
admin.site.register(time_slot)
admin.site.register(measure_data)
admin.site.register(sub_area)


