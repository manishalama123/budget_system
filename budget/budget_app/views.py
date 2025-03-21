from django.shortcuts import render, redirect
from django.http import HttpResponse  
from . import models
from .models import Income, Expense
from decimal import Decimal
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
    incomes = Income.objects.all().order_by('-date')
    expenses = Expense.objects.all().order_by('-date')

    context ={
        'incomes' : incomes,
        'expenses': expenses,
    }
    return render(request, 'history.html', context)