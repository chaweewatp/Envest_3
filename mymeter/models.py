from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

customer_type = (
    ('1', 'VSPP'),
    ('2', 'CUSTOMER')
)
meter_type = (
    ('1', 'VSPP'),
    ('2', 'CUSTOMER'),
    ('3', 'GRID')
)
packages = (
    ('1', 'NONE'),
    ('2', '1200'),
    ('3', '1470'),
    ('4', '1745'),
    ('5', '2015'),
    ('6', '2290'),
    ('7', '2560'),
    ('8', '2840')

)


# Create your models here.
class accounts(models.Model):
    created = models.DateTimeField(default=datetime.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # relation
    package_type = models.CharField(max_length=8, choices=packages, blank=True, default='4')  # query
    telephone = models.CharField(max_length=30, default='[]')  # list

    def __str__(self):
        return "{}-{}".format(self.id, self.owner)

    def changePackage(self, package):
        """
        This function change package for accounts
        :arg package = 'NONE', 'SMALL', 'MEDIUM', 'LARGE'
        """
        print(package)
        self.package_type = package
        self.save()


class sub_area(models.Model):
    """
        This class provides area detail
    """
    created = models.DateTimeField(default=datetime.now)
    area_no = models.CharField(max_length=3, null=True, blank=True)
    area_text = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.id, self.area_text)


class meters(models.Model):
    """
        this class provides
    """
    created = models.DateTimeField(default=datetime.now)
    meter_type = models.CharField(max_length=8, choices=meter_type, blank=True, default='2')  # query
    owner = models.ForeignKey(accounts, on_delete=models.CASCADE)  # relation
    location = models.CharField(max_length=30, null=True, blank=True)
    area = models.ForeignKey(sub_area, on_delete=models.CASCADE, null=True, blank=True)  # relation
    meter_id = models.CharField(blank=True, max_length=20, null=True)  ## for get API value from meter network
    carbonReduce = models.FloatField(null=True, blank=True)

    def __str__(self):
        return "{}-{}-{}".format(self.id, self.meter_id, self.location)


class time_slot(models.Model):
    created = models.DateTimeField(default=datetime.now)
    text_time = models.CharField(max_length=30)  # start-hour + date + month + year example 140007092020

    def __str__(self):
        return "{}".format(self.text_time)


class measure_data(models.Model):
    created = models.DateTimeField(default=datetime.now)
    meter_id = models.ForeignKey(meters, on_delete=models.CASCADE)  # relation
    t_slot = models.ForeignKey(time_slot, on_delete=models.CASCADE)  # relation
    kWhr = models.FloatField(blank=True)

    def __str__(self):
        return "{}-{}".format(self.meter_id, self.t_slot)


class transactions(models.Model):
    """
        this class provides transaction data of customer at each hour
    """
    created = models.DateTimeField(default=datetime.now)
    meter_id = models.ForeignKey(meters, on_delete=models.CASCADE)  # relation
    t_slot = models.ForeignKey(time_slot, on_delete=models.CASCADE, blank=True)  # relation
    kWhr = models.ForeignKey(measure_data, on_delete=models.CASCADE, blank=True)  # relation
    vspp_value = models.FloatField(blank=True)
    grid_value = models.FloatField(blank=True)

    def __str__(self):
        return "{}-{}".format(self.meter_id, self.t_slot)
