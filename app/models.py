import datetime
import string
import random

from django.db import models


class Machine(models.Model):
    name = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250, blank=True, default='')
    token = models.CharField(max_length=250, blank=True, default='')
    token_updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.pk, self.name)

    # Get new token
    def create_new_token(self):
        time = datetime.datetime.now()
        self.token_updated_at = time
        self.token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(64))
        self.save()
        return self.token


class Wallet(models.Model):

    # UNITS 
    
    PENCE_1 = 1
    PENCE_2 = 2
    PENCE_5 = 5
    PENCE_10 = 10
    PENCE_20 = 20
    PENCE_50 = 50
    POUND_1 = 100
    POUND_2 = 200
    POUND_5 = 500
    POUND_10 = 1000
    POUND_20 = 2000
    POUND_50 = 5000

    CURRENCY_UNITS_CHOICE = (
        (PENCE_1, '1 pence'),
        (PENCE_2, '2 pence'),
        (PENCE_5, '5 pence'),
        (PENCE_10, '10 pence'),
        (PENCE_20, '20 pence'),
        (PENCE_50, '50 pence'),
        (POUND_1, '1 pound'),
        (POUND_2, '2 pound'),
        (POUND_5, '5 pound'),
        (POUND_10, '10 pound'),
        (POUND_20, '20 pound'),
        (POUND_50, '50 pound'),
    )

    machine = models.ForeignKey(Machine, related_name="Machine", on_delete=models.CASCADE)
    units = models.PositiveIntegerField(verbose_name="Currency unit", default=PENCE_1, choices=CURRENCY_UNITS_CHOICE)
    amount = models.PositiveIntegerField(verbose_name="Amount pcs", default=0)

    def __str__(self):
        return "{}:{}".format(self.get_units_display(), self.amount)
