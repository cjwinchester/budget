from __future__ import unicode_literals
from django.db import models


HUMANS = (
    ("laurel", "Laurel"),
    ("cody", "Cody"),
    ("both", "Both"),
)


class Budget(models.Model):
    category = models.CharField(max_length=100)
    monthly_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    autopay = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ('category',)
        verbose_name = "Budget item"
        verbose_name_plural = "Budget items"


class Recipient(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name',)


class Spending(models.Model):
    cat = models.ForeignKey(
        Budget,
        verbose_name="Category",
        on_delete=models.CASCADE
    )
    spending_date = models.DateField(
        verbose_name="Date"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    human = models.CharField(
        max_length=20,
        choices=HUMANS
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.spending_date)

    class Meta:
        ordering = ('-spending_date',)
        verbose_name = "Spending"
        verbose_name_plural = "Spending"


class Income(models.Model):
    income_date = models.DateField(
        verbose_name="Date"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    human = models.CharField(
        max_length=20,
        choices=HUMANS
    )
    notes = models.TextField(
        blank=True
    )
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.income_date)

    class Meta:
        ordering = ('-income_date',)
        verbose_name = "Incoming payment"
        verbose_name_plural = "Incoming payments"
