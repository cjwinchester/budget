from django.shortcuts import render
from django.db.models import Sum, Avg, Q

from budget.models import Budget, Spending, Recipient, Income, MajorExpense

from datetime import datetime
from django.db import connection
from calendar import monthrange

budget_color_conf = {
    "meeting_budget": {
        "color": "#398439",
        "accent_color": "#dff0d8"
    },
    "over_budget": {
        "color": "#d43f3a",
        "accent_color": "#f2dede"
    }
}


def main(request):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    grand_total_spending = Spending.objects.aggregate(Sum("amount"))
    grand_total_income = Income.objects.aggregate(Sum("amount"))
    balance = grand_total_income['amount__sum'] - grand_total_spending['amount__sum']
    monthly_budget_total = Budget.objects.aggregate(Sum('monthly_budget'))['monthly_budget__sum']
    earliest_date = Spending.objects.earliest('spending_date').spending_date
    transfer_to_savings_total = Spending.objects.filter(cat__category__icontains="savings").aggregate(Sum("amount"))['amount__sum']
    n = datetime.now()
    current_day = n.day
    current_month = n.month
    current_year = n.year
    days_left_this_month = monthrange(current_year, current_month)[1] - current_day
    total_this_month = Spending.objects.filter(spending_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
    if not total_this_month:
        total_this_month = 0
        monthly_diff_pct = 0
    else:
        monthly_diff_pct = (total_this_month / monthly_budget_total) * 100

    monthly_col = budget_color_conf["meeting_budget"].get("color", "#000")
    monthly_col_accent = budget_color_conf["meeting_budget"].get("accent_color", "#000")

    if monthly_diff_pct > 100:
        monthly_col = budget_color_conf["over_budget"].get("color", "#000")
        monthly_col_accent = budget_color_conf["over_budget"].get("accent_color", "#000")

    top_recips = Recipient.objects.annotate(total_sum=Sum('spending__amount')).order_by('-total_sum')[:10]
    recent_spending = Spending.objects.all()[:10]
    
    this_month = []
    for budget_item in Budget.objects.order_by('-monthly_budget'):
        d = {}
        d['category'] = budget_item.category
        d['category_pk'] = budget_item.pk
        d['budgeted_amount'] = budget_item.monthly_budget
        if budget_item.autopay:
            d['autopay'] = True
        total_spent = budget_item.spending_set.filter(spending_date__month=current_month).aggregate(Sum("amount"))['amount__sum']
        if not total_spent:
            total_spent = 0
            pct = 0
        else:
            pct = (total_spent / budget_item.monthly_budget) * 100
        col = budget_color_conf["meeting_budget"].get("color", "#000")
        col_accent = budget_color_conf["meeting_budget"].get("accent_color", "#000")

        if pct > 100:
            col = budget_color_conf["over_budget"].get("color", "#000")
            col_accent = budget_color_conf["over_budget"].get("accent_color", "#000")

        d['total_spent'] = total_spent
        d['pct'] = int(pct)
        d['col'] = col
        d['col_accent'] = col_accent
        this_month.append(d)

    active_major_expenses = [x for x in MajorExpense.objects.all() if \
                             x.get_total_spent() < x.amount]
        
    d = {
        'top_recips': top_recips,
        'earliest_date': earliest_date,
        'active_major_expenses': active_major_expenses,
        'monthly_budget_total': monthly_budget_total,
        'this_month': this_month,
        'total_this_month': total_this_month,
        'monthly_diff_pct': monthly_diff_pct,
        'monthly_col': monthly_col,
        'monthly_col_accent': monthly_col_accent,
        'days_left_this_month': days_left_this_month,
        'last_updated_at': last_updated_at,
        'grand_total_spending': grand_total_spending,
        'grand_total_income': grand_total_income,
        'balance': balance,
        'transfer_to_savings_total': transfer_to_savings_total,
        'recent_spending': recent_spending
    }
    return render(request, 'budget/main.html', d)
    
    
def category(request, pk):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    grand_total_spending = Spending.objects.aggregate(Sum("amount"))
    categories = Budget.objects.all()
    budget_item = categories.get(pk=pk)
    spending = Spending.objects.filter(cat=pk)
    spending_total = spending.aggregate(Sum('amount'))['amount__sum']
    if not spending_total:
        spending_total = 0
    latest = spending[:100]
    pct_of_total_spending = (spending_total / grand_total_spending['amount__sum']) * 100
    budgeted_pct = (budget_item.monthly_budget / categories.aggregate(Sum('monthly_budget'))['monthly_budget__sum']) * 100
    truncate_date = connection.ops.date_trunc_sql('month', 'spending_date')
    qs = spending.extra({'month': truncate_date})
    spending_by_month = qs.values('month').annotate(Sum('amount')).order_by('month')
    spending_by_month_avg = spending_by_month.aggregate(Avg('amount__sum'))['amount__sum__avg']
    top_recipients = spending.values("recipient", "recipient__name").order_by().annotate(Sum("amount")).order_by('-amount__sum')[:10]
    recent_spending = spending[:100]

    d = {
        'spending': spending,
        'budget_item': budget_item,
        'spending_total': spending_total,
        'latest': latest,
        'spending_by_month': spending_by_month,
        'spending_by_month_avg': spending_by_month_avg,
        'pct_of_total_spending': pct_of_total_spending,
        'budgeted_pct': budgeted_pct,
        'categories': categories,
        'top_recipients': top_recipients,
        'recent_spending': recent_spending,
        'last_updated_at': last_updated_at
    }
    return render(request, 'budget/category.html', d)


def category_index(request):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    categories = Budget.objects.all()
    cats = categories.values('pk', 'category').annotate(Sum('spending__amount')).order_by('-spending__amount__sum')

    d = {
        'cats': cats,
        'last_updated_at': last_updated_at
    }
    return render(request, 'budget/category-index.html', d)


def expense(request, exp_id):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    single_expense = Spending.objects.get(pk=exp_id)
    d = {
        'single_expense': single_expense,
        'last_updated_at': last_updated_at
    }
    return render(request, 'budget/expense.html', d)
    
    
def recipient(request, pk):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    grand_total_spending = Spending.objects.aggregate(Sum("amount"))
    categories = Budget.objects.all()
    spending = Spending.objects.filter(recipient=pk).order_by('-spending_date')
    spending_total = spending.aggregate(Sum('amount'))['amount__sum']
    latest = spending[:100]
    pct_of_total_spending = (spending_total / grand_total_spending['amount__sum']) * 100
    truncate_date = connection.ops.date_trunc_sql('month', 'spending_date')
    qs = spending.extra({'month': truncate_date})
    spending_by_month = qs.values('month').annotate(Sum('amount')).order_by('month')
    
    d = {
        'spending_total': spending_total,
        'latest': latest,
        'grand_total_spending': grand_total_spending,
        'pct_of_total_spending': pct_of_total_spending,
        'spending_by_month': spending_by_month,
        'categories': categories,
        'last_updated_at': last_updated_at
    }
    return render(request, 'budget/recipient.html', d)
    

def day(request, year, month, day):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    spending = Spending.objects.filter(
        spending_date__year=year,
        spending_date__month=int(month),
        spending_date__day=int(day),
    ).order_by('-pk')
    try:
        previous = spending.last().get_previous_by_spending_date()
    except:
        previous = None
    try:
        next = spending[0].get_next_by_spending_date()
    except:
        next = None
        
    total_sum = spending.aggregate(Sum('amount'))

    d = {
        'time_value': 'day',
        'spending': spending.order_by('-amount'),
        'total_sum': total_sum['amount__sum'],
        'previous': previous,
        'next': next,
        'display_date': spending[0].spending_date,
        'last_updated_at': last_updated_at
    }
    return render(request, 'budget/day.html', d)


def month(request, year, month):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    monthly_budget_total = Budget.objects.aggregate(Sum('monthly_budget'))['monthly_budget__sum']
    spending = Spending.objects.filter(
        spending_date__year=year,
        spending_date__month=int(month),
    )
    display_date = spending[0].spending_date
    truncate_date = connection.ops.date_trunc_sql('day', 'spending_date')
    qs = spending.extra({'day': truncate_date})
    spending_by_day = qs.values('day').annotate(Sum('amount')).order_by('day')
    total_sum = spending.aggregate(Sum('amount'))['amount__sum']
        
    if not total_sum:
        total_sum = 0
        monthly_diff_pct = 0
    else:
        monthly_diff_pct = (total_sum / monthly_budget_total) * 100

    monthly_col = budget_color_conf["meeting_budget"].get("color", "#000")
    monthly_col_accent = budget_color_conf["meeting_budget"].get("accent_color", "#000")

    if monthly_diff_pct > 100:
        monthly_col = budget_color_conf["over_budget"].get("color", "#000")
        monthly_col_accent = budget_color_conf["over_budget"].get("accent_color", "#000")
    
    days_in_this_month = monthrange(int(year), int(month))[1]
    
    spending_all_days = []
    
    for num in range(1, days_in_this_month+1):
        d = {}
        d['day'] = datetime(int(year), int(month), num)
        d['amount'] = '0.00'
        d['spending'] = []
        
        for item in spending_by_day:
            day = int(item['day'][-2:])
            if day == num:
                d['amount'] = str(item['amount__sum'])
                
        for spend in spending:
            if spend.spending_date.day == num:
                z = {}
                z['expense_pk'] = spend.pk
                z['recipient'] = spend.recipient.name
                z['recipient_pk'] = spend.recipient.pk
                z['category'] = spend.cat.category
                z['category_pk'] = spend.cat.pk
                z['amount'] = spend.amount
                d['spending'].append(z)
              
        spending_all_days.append(d)

    # ugh
    months_of_the_year = {
        "1": "January",
        "2": "February",
        "3": "March",
        "4": "April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
        
    previous_month = str(int(month) - 1)
    previous_year = year
    if previous_month == 0:
        previous_month = "12"
        previous_year = str(int(year) - 1)
        
    next_month = str(int(month) + 1)
    next_year = year
    if next_month == 13:
        next_month = "1"
        next_year = str(int(next_year) + 1)

    next_month_qs = Spending.objects.filter(
        spending_date__year=next_year,
        spending_date__month=next_month,
    )

    if next_month_qs.count() > 0:
        next_up = {
            "month": next_month,
            "verbose_month": months_of_the_year.get(next_month),
            "year": next_year
        }
    else:
        next_up = None

    previous_month_qs = Spending.objects.filter(
        spending_date__year=previous_year,
        spending_date__month=int(previous_month),
    )
    if previous_month_qs.count() > 0:
        previous_up = {
            "month": previous_month,
            "verbose_month": months_of_the_year.get(previous_month),
            "year": previous_year
        }
    else:
        previous_up = None
        
    d = {
        'time_value': 'month',
        'monthly_budget_total': monthly_budget_total,
        'spending_by_time': spending_all_days,
        'total_sum': total_sum,
        'display_date': display_date,
        'monthly_diff_pct': monthly_diff_pct,
        'monthly_col': monthly_col,
        'monthly_col_accent': monthly_col_accent,
        'last_updated_at': last_updated_at,
        'next': next_up,
        'previous': previous_up,
    }
    return render(request, 'budget/month.html', d)


def year(request, year):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    spending = Spending.objects.filter(
        spending_date__year=year
    )

    truncate_date = connection.ops.date_trunc_sql('month', 'spending_date')
    qs = spending.extra({'month': truncate_date})
    spending_by_month = qs.values('month').annotate(Sum('amount')).order_by('month')

    d = {
        'time_value': 'year',
        'spending': spending,
        'display_date': year,
        'last_updated_at': last_updated_at
    }
    return render(request, 'budget/year.html', d)

    
def search(request):
    last_updated_at = Spending.objects.latest("last_modified").last_modified
    query = request.GET.get('q', '')
    exploded = query.split(" ")
    q_objects = Q()
    for term in exploded:
        q_objects &= Q(name__icontains=term)
    if query:
        qset = (q_objects)
        results = Recipient.objects.filter(qset).annotate(total_sum=Sum("spending__amount"))
    else:
        results = []

    d = {
        'results': results,
        'query': query,
        'last_updated_at': last_updated_at
    }
    return render(request, 'budget/search.html', d)