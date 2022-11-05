from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Balance(models.Model):
    borrower = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='owes')
    lender = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='owed_by')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    reason = models.CharField(max_length=250)
    expiration = models.BigIntegerField()

    def __str__(self):
        return f"borrower: {self.borrower}, lender: {self.lender}, Amount: {self.amount}"
