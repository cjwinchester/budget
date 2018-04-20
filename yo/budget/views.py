from django.shortcuts import render
from django.db.models import Sum, Avg
from django.db import connection

from budget.models import Budget, Spending, Recipient, Income

from datetime import datetime
from calendar import monthrange
from decimal import Decimal


def main(request):

    all_spending = Spending.objects.all()
    all_income = Income.objects.all()

    all_time_income = all_income.aggregate(Sum('amount'))['amount__sum']

    # spending total minus savings transfers
    savings_cat = Budget.objects.get(category='Transfer to savings')
    all_time_spending = all_spending.exclude(cat=savings_cat) \
                                    .aggregate(Sum('amount'))['amount__sum']

    today = datetime.today()
    this_year = today.year
    this_month = today.month
    this_day = today.day

    spending_this_year = all_spending.filter(
                            spending_date__year=this_year
                         )

    spent_this_year = spending_this_year.exclude(cat=savings_cat) \
                                        .aggregate(Sum('amount'))['amount__sum']

    earned_this_year = all_income.filter(
                          income_date__year=this_year
                       ).aggregate(Sum('amount'))['amount__sum']

    if not spent_this_year:
        spent_this_year = Decimal(0.0)

    if not earned_this_year:
        earned_this_year = Decimal(0.0)

    balance_this_year = earned_this_year - spent_this_year

    savings_this_year = spending_this_year.filter(
                            cat=savings_cat
                        ).aggregate(Sum('amount'))['amount__sum']

    recent_spending = all_spending[:10]

    spent_this_month = all_spending.filter(
                           spending_date__month=this_month,
                           spending_date__year=this_year
                       ).aggregate(Sum('amount'))['amount__sum']

    spent_this_month_no_ubdis = all_spending.filter(
                           spending_date__month=this_month,
                           spending_date__year=this_year,
                           ubdi=True
    ).aggregate(Sum('amount'))['amount__sum']

    budget_items = Budget.objects.filter(complete=False)

    budget_total = budget_items.aggregate(
                       Sum('monthly_budget')
                    )['monthly_budget__sum']

    if not spent_this_month:
        spent_this_month = Decimal(0.0)

    if not budget_total:
        budget_total = Decimal(0.0)

    days_left_this_month = monthrange(this_year, this_month)[1] - this_day

    try:
        last_updated = all_spending.latest('last_modified').last_modified
    except:
        last_updated = None

    recipients_with_totals = Recipient.objects.annotate(
                                  total_sum=Sum('spending__amount')
                              ).order_by('-total_sum')

    budget_categories = []

    for item in budget_items.order_by('-monthly_budget'):
        item_d = {}

        item_d['category_name'] = item.category
        item_d['amount_budgeted'] = item.monthly_budget
        if item.autopay:
            item_d['autopay'] = True

        amount_spent = item.spending_set.filter(
                           spending_date__month=this_month,
                           spending_date__year=this_year
                       ).aggregate(Sum('amount'))['amount__sum']

        if not amount_spent:
            amount_spent = Decimal(0.0)
            pct = 0
        else:
            pct = (amount_spent / item.monthly_budget) * 100

        item_d['amount_spent'] = amount_spent
        item_d['pct'] = pct

        category_spending_this_year = all_spending.filter(
                                          cat=item
                                      ).filter(spending_date__year=this_year)

        spending_total_this_year = category_spending_this_year.aggregate(
                                       Sum('amount')
                                   )['amount__sum']

        if not spending_total_this_year:
            spending_total_this_year = 0

        item_d['spending_total'] = spending_total_this_year

        truncate_date = connection.ops.date_trunc_sql(
            'month', 'spending_date')

        qs = category_spending_this_year.extra({'month': truncate_date})
        spending_by_month = qs.values('month').annotate(
                                Sum('amount')
                            ).order_by('month')

        spending_by_month_avg = spending_by_month.aggregate(
                                    Avg('amount__sum')
                                )['amount__sum__avg']

        if not spending_by_month_avg:
            spending_by_month_avg = 0

        item_d['monthly_avg'] = spending_by_month_avg

        # unanticipated big-dollar items
        ubdis = item.spending_set.filter(
            spending_date__month=this_month,
            spending_date__year=this_year,
            ubdi=True
        )

        item_d['ubdis'] = ubdis
        ubdi_total = ubdis.aggregate(Sum('amount'))['amount__sum']

        if not ubdi_total:
            ubdi_total = Decimal(0.0)

        item_d['ubdi_diff'] = amount_spent - ubdi_total

        budget_categories.append(item_d)

    d = {
        'last_updated': last_updated,
        'recipients_with_totals': recipients_with_totals,
        'spent_this_year': spent_this_year,
        'earned_this_year': earned_this_year,
        'balance_this_year': balance_this_year,
        'recent_spending': recent_spending,
        'budget_total': budget_total,
        'spent_this_month': spent_this_month,
        'spent_this_month_no_ubdis': spent_this_month_no_ubdis,
        'left_this_month': budget_total - spent_this_month,
        'left_this_month_no_ubdis': budget_total - spent_this_month_no_ubdis,
        'days_left_this_month': days_left_this_month,
        'budget_categories': budget_categories,
        'savings_this_year': savings_this_year,
        'all_time_income': all_time_income,
        'all_time_spending': all_time_spending,
        'all_time_balance': all_time_income - all_time_spending,
    }

    return render(request, 'budget/main.html', d)
