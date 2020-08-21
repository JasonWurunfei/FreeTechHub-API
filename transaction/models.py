from django.db import models
from django.conf import settings

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('B','bounty'),
        ('PBQ','post bounty question'),
        ('DL', 'daily login'),
        ('LT', 'light tree'),
        ('L10%', 'like over 10%'),
        ('L25%', 'like over 25%'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE)
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField()

    class Meta:
        ordering = ['-time']

    def make_transaction(self):
        self.user.balance += self.amount
        if self.user.balance < 0:
            raise Exception('not enough balance!')
        else:
            self.user.save()

    @property
    def user_instance(self):
        return self.user
        