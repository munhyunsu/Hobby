from django.db import models

import time

class Login(models.Model):
    user = models.CharField('User name', max_length=50)
    date = models.DateTimeField('date published')

    def __str__(self):
        return self.user + ' : ' + self.date.strftime('%Y-%m-%dT%H:%M:%S')

