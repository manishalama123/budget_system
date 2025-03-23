from django.shortcuts import render, redirect
from django.http import HttpResponse  
from . import models
from .models import Income, Expense
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Sum 

# def home(request):
#     context = {}
#     return render(request, 'dashboard.html', context)
def dashboard(request):
    total_income= Income.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    remaining = total_income - total_expense
    context = {
        'total_income' : total_income,
        'total_expense' : total_expense,
        'remaining': remaining,
        'incomes': Income.objects.all().order_by('-date')[:5],
        'expenses': Expense.objects.all().order_by('-date')[:5]
    }
    return render(request, 'dashboard.html', context)

def new_income(request):
    return render(request, 'new_income.html')

def new_expense(request):
    return render(request, 'new_expense.html')

def add_income(request):
    if request.method == "POST":
        amount = Decimal(request.POST["amount"])
        description = request.POST["description"]
        date = request.POST["date"]
        Income.objects.create(amount=amount, description=description, date=date)
        return redirect('dashboard')
    return HttpResponse("Invalid response", status=404)

def add_expense(request):
    if request.method == "POST":
        amount = Decimal(request.POST["amount"])
        description = request.POST["description"]
        category = request.POST["category"]        
        date = request.POST["date"]
        Expense.objects.create(amount=amount, description=description, category=category, date=date)
        return redirect('dashboard')
    return HttpResponse("Invalid response", status=404)


def history(request):
    # Fetch income and expenses from the database
    incomes = Income.objects.all()
    expenses = Expense.objects.all()

    # Convert to a unified transaction format
    transactions = [
        {
            "date": income.date,
            "category": "Income",  # Default category for Income
            "amount": income.amount,
            "description": income.description,
            "type": "Income"
        }
        for income in incomes
    ] + [
        {
            "date": expense.date,
            "category": expense.category,  # Use category for Expense
            "amount": expense.amount,
            "description": expense.description,
            "type": "Expense"
        }
        for expense in expenses
    ]

    # Sort transactions by date (latest first)
    transactions.sort(key=lambda x: x["date"], reverse=True)
     # Add Pagination (5 transactions per page)
    paginator = Paginator(transactions, 5)  # Change 5 to any number of transactions per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "history.html", {"page_obj": page_obj})

