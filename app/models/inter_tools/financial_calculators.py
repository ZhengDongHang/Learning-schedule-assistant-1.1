def calculate_loan(data):
    principal = float(data.get('principal', 0))
    annual_rate = float(data.get('annual_rate', 0)) / 100
    years = float(data.get('years', 0))

    monthly_rate = annual_rate / 12
    number_of_payments = years * 12

    # Calculate monthly payment
    if monthly_rate > 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** number_of_payments) / ((1 + monthly_rate) ** number_of_payments - 1)
    else:
        monthly_payment = principal / number_of_payments

    # Calculate total cost
    total_cost = monthly_payment * number_of_payments

    # Calculate remaining balance
    remaining_balance = principal

    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_cost': round(total_cost, 2),
        'remaining_balance': round(remaining_balance, 2)
    }

def calculate_investment(data):
    initial_investment = float(data.get('initial_investment', 0))
    annual_rate = float(data.get('annual_rate', 0)) / 100
    years = float(data.get('years', 0))

    # Calculate future value
    future_value = initial_investment * (1 + annual_rate) ** years

    # Calculate ROI
    roi = (future_value - initial_investment) / initial_investment * 100

    return {
        'future_value': round(future_value, 2),
        'roi': round(roi, 2)
    }

def calculate_retirement(data):
    monthly_savings = float(data.get('monthly_savings', 0))
    annual_rate = float(data.get('annual_rate', 0)) / 100
    years = float(data.get('years', 0))

    number_of_payments = years * 12
    monthly_rate = annual_rate / 12

    # Calculate future value of savings
    future_value = monthly_savings * (((1 + monthly_rate) ** number_of_payments - 1) / monthly_rate)

    return {
        'future_value': round(future_value, 2)
    }

def calculate_tax(data):
    income = float(data.get('income', 0))
    tax_rate = float(data.get('tax_rate', 0)) / 100

    # Calculate tax
    tax = income * tax_rate

    # Calculate net income
    net_income = income - tax

    return {
        'tax': round(tax, 2),
        'net_income': round(net_income, 2)
    }

def calculate_budget(data):
    income = float(data.get('income', 0))
    expenses = float(data.get('expenses', 0))

    # Calculate surplus or deficit
    surplus_or_deficit = income - expenses

    return {
        'surplus_or_deficit': round(surplus_or_deficit, 2)
    }

def calculate_currency(data):
    amount = float(data.get('amount', 0))
    exchange_rate = float(data.get('exchange_rate', 0))

    # Calculate converted amount
    converted_amount = amount * exchange_rate

    return {
        'converted_amount': round(converted_amount, 2)
    }

def calculate_asset(data):
    assets = float(data.get('assets', 0))
    growth_rate = float(data.get('growth_rate', 0)) / 100
    years = float(data.get('years', 0))

    # Calculate asset value
    future_value = assets * (1 + growth_rate) ** years

    return {
        'future_value': round(future_value, 2)
    }

def calculate_debt(data):
    total_debt = float(data.get('total_debt', 0))
    interest_rate = float(data.get('interest_rate', 0)) / 100
    monthly_payment = float(data.get('monthly_payment', 0))

    # Calculate remaining balance
    remaining_balance = total_debt

    while remaining_balance > 0:
        remaining_balance = remaining_balance * (1 + interest_rate / 12) - monthly_payment
        if remaining_balance < 0:
            remaining_balance = 0

    return {
        'remaining_balance': round(remaining_balance, 2)
    }
