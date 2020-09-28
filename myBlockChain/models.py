from django.db import models
from datetime import datetime

# Create your models here.
class myBlock(models.Model):
    created = models.DateTimeField(default = datetime.now)
