from flask import Blueprint, render_template, request, jsonify
from app.models.inter_tools import financial_calculators

tools_bp = Blueprint('tools', __name__)

@tools_bp.route('/financial_calculator', methods=['GET'])
def financial_calculator():
    return render_template('financial_calculator.html')

@tools_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    calculator_type = data.get('type')

    if calculator_type == 'loan':
        result = financial_calculators.calculate_loan(data)
    elif calculator_type == 'investment':
        result = financial_calculators.calculate_investment(data)
    elif calculator_type == 'retirement':
        result = financial_calculators.calculate_retirement(data)
    elif calculator_type == 'tax':
        result = financial_calculators.calculate_tax(data)
    elif calculator_type == 'budget':
        result = financial_calculators.calculate_budget(data)
    elif calculator_type == 'currency':
        result = financial_calculators.calculate_currency(data)
    elif calculator_type == 'asset':
        result = financial_calculators.calculate_asset(data)
    elif calculator_type == 'debt':
        result = financial_calculators.calculate_debt(data)
    else:
        result = {'error': 'Invalid calculator type'}

    return jsonify(result)
