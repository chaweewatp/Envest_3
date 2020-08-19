from django.db import models
from django.contrib.auth.models import User

customer_type = (
    ('VSPP', 'VSPP'),
    ('CUSTOMER', 'CUSTOMER')
)
meter_type = (
    ('VSPP', 'VSPP'),
    ('CUSTOMER', 'CUSTOMER'),
    ('GRID', 'GRID')
)
packages = (
    ('SMALL', 'SMALL'),
    ('MEDIUM', 'MEDIUM'),
    ('LARGE', 'LARGE'),
    ('NONE', 'NONE')
)
# Create your models here.

class accounts(models.Model):
    _id=models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # relation
    package_type = models.CharField(max_length = 8, choices = packages, blank = True, default='NONE')  # query
    telephone = models.CharField(max_length=30, default='[]')  # list

class meters(models.Model):
    """
        this class provides

    """
    _id=models.CharField(max_length = 30)
    meter_type = models.CharField(max_length = 8, choices = meter_type, blank = True, default='CUSTOMER')  # query
    owner=models.ForeignKey(accounts, on_delete=models.CASCADE)  # relation
    location=models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "{}".format(self._id)


class transactions(models.Model):
    """
        this class provides transaction data of customer at each hour
    """
    _id=models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    meter_id=models.ForeignKey(meters, on_delete=models.CASCADE)  # relation
    vspp_value=models.FloatField(blank=True)
    grid_value=models.FloatField(blank=True)

    def __str__(self):
        return "{}".format(self._id)
