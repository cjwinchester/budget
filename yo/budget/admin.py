from django.contrib import admin
from django.db.models import Sum, DateField
from budget.models import Budget, Spending, Recipient, Income
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.humanize.templatetags import humanize


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'monthly_budget', 'complete',)
    save_on_top = True


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_sum',)
    search_fields = ('name',)

    def total_sum(self, obj):
        sum = obj.spending_set.aggregate(Sum('amount'))['amount__sum']
        if sum:
            return '$' + humanize.intcomma(sum)
        else:
            return '$0.00'

    total_sum.short_description = 'Total spending'


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('income_date', 'human', 'amount',)


@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ('amount', 'recipient', 'spending_date', 'cat', 'human')
    formfield_overrides = {
        DateField: {'widget': AdminDateWidget}
    }
    search_fields = ('recipient__name',)
    list_filter = ('human', 'cat',)
    save_on_top = True
