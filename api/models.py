from django.db import models
from django.db.models import Sum


class Users(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)

    def owes_and_owed_by_cal(self, action):
        owes = {}
        owed_by = {}
        lenders = (
            self.borrowers.values_list("lender__name")
            .order_by("lender__name")
            .annotate(amount=Sum("amount"))
        )
        lenders = dict((x, y) for x, y in lenders)
        borrowers = (
            self.lenders.values_list("borrower__name")
            .order_by("borrower__name")
            .annotate(amount=Sum("amount"))
        )
        borrowers = dict((x, y) for x, y in borrowers)
        for lender, amount in lenders.items():
            if borrowers.get(lender):
                if amount > borrowers.get(lender):
                    owes[lender] = amount - borrowers.get(lender)
                else:
                    owed_by[lender] = borrowers.get(lender) - amount
                del borrowers[lender]
            else:
                owes[lender] = amount

        owed_by.update(borrowers)
        if action == "owes":
            return owes
        else:
            return owed_by

    @property
    def owes(self):
        return self.owes_and_owed_by_cal("owes")

    @property
    def owed_by(self):
        return self.owes_and_owed_by_cal("owed_by")

    @property
    def balance(self):
        total_owes = 0
        total_owed_by = 0
        if self.borrowers.exists():
            total_owes = self.borrowers.aggregate(Sum("amount"))["amount__sum"]
        if self.lenders.exists():
            total_owed_by = self.lenders.aggregate(Sum("amount"))["amount__sum"]

        return total_owed_by - total_owes


class Balance(models.Model):
    borrower = models.ForeignKey(
        "Users", on_delete=models.CASCADE, related_name="borrowers"
    )
    lender = models.ForeignKey(
        "Users", on_delete=models.CASCADE, related_name="lenders"
    )
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    reason = models.CharField(max_length=250)
    expiration = models.BigIntegerField()

    def __str__(self):
        return (
            f"borrower: {self.borrower}, lender: {self.lender}, Amount: {self.amount}"
        )
