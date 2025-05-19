from .classifier import predict_category
from django.shortcuts import render, redirect
from django.http import HttpResponse  
from . import models
from django.contrib.auth.models import User
from .models import Income, Expense, Budget
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Sum 
from django.utils import timezone
from django.http import JsonResponse



def predict_category_view(request):
    description = request.GET.get('description', '')
    if description:
        predicted = predict_category(description)  # Get prediction
        return JsonResponse({'category': predicted})  # Send it back as a JSON response
    return JsonResponse({'category': ''})


# def home(request):
#     context = {}
#     return render(request, 'dashboard.html', context)
def dashboard(request):
    total_income= Income.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    remaining = total_income - total_expense
    

    expenses = Expense.objects.all()
    expense_data = {}

    for expense in expenses:
        category = expense.category
        expense_data[category] = expense_data.get(category, 0) + float(expense.amount)
    
    labels = list(expense_data.keys())
    values = list(expense_data.values())
    
    context = {
        'total_income' : total_income,
        'total_expense' : total_expense,
        'remaining': remaining,
        'incomes': Income.objects.all().order_by('-date')[:5],
        'expenses': Expense.objects.all().order_by('-date')[:5],
        'labels': labels,
        'values': values,
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

# def add_expense(request):
#     if request.method == "POST":
#         amount = Decimal(request.POST["amount"])
#         description = request.POST["description"]
#         category = request.POST["category"]        
#         date = request.POST["date"]
#         Expense.objects.create(amount=amount, description=description, category=category, date=date)
#         return redirect('dashboard')
#     return HttpResponse("Invalid response", status=404)

def add_expense(request):
    if request.method == "POST":
        amount = Decimal(request.POST["amount"])
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]

        # 🔮 Only predict if category is set to "other"
        if category.lower() == "other":
            category = classifier_instance.predict_category(description)

        Expense.objects.create(
            amount=amount,
            description=description,
            category=category,
            date=date
        )
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

def budget(request):
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        end_date = request.POST.get('end_date')

        # Ensure the date is in the correct format
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Create and save the new Budget
        new_budget = Budget(
            name=name,
            amount=amount,
            category=category,
            start_date=timezone.now().date(),  # Current date as start date
            end_date=end_date
        )
        new_budget.save()

        return redirect('dashboard')  # Redirect to the dashboard after saving
    

    budgets = Budget.objects.all()
    budget_data = []

    for budget in budgets:
        # Debug print — to check if expenses are matching
        print(f"---\nBudget: {budget.name}, Category: {budget.category}")
        print(f"Date Range: {budget.start_date} to {budget.end_date}")
        # Filter matching expenses
        budget_category = budget.category.strip().lower()
        matching_expenses = Expense.objects.filter(
            category__iexact=budget_category,
            date__gte=budget.start_date,
            date__lte=budget.end_date
        )

        
        for e in matching_expenses:
            print(f"Matched: {e.amount} on {e.date} in {e.category}")
        total_spent = matching_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        # For each budget, append info for UI
        budget_data.append({
            'budget': budget,
            'spent': total_spent,
            'remaining': budget.amount - total_spent,
            'percentage': round((total_spent / budget.amount) * 100, 2) if budget.amount > 0 else 0
        })

    return render(request, 'budget.html', {'budget_data': budget_data})