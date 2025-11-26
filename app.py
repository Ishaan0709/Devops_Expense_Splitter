from flask import Flask, request, redirect, url_for, render_template_string, session
import json
import math

app = Flask(__name__)
app.secret_key = 'devops-expense-tracker-secret-key-2024'

# Exchange rates
EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
    'INR': 83.0,
    'JPY': 150.0,
    'CAD': 1.35,
    'AUD': 1.52,
    'CNY': 7.23
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💰 Smart Expense Splitter</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366F1;
            --primary-dark: #4F46E5;
            --secondary: #10B981;
            --danger: #EF4444;
            --dark: #1F2937;
            --light: #F9FAFB;
            --gray: #6B7280;
            --border: #E5E7EB;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            gap: 30px;
            justify-content: center;
            align-items: flex-start;
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border: 1px solid var(--border);
        }
        
        .form-card {
            flex: 1;
            max-width: 500px;
        }
        
        .summary-card {
            flex: 1;
            max-width: 400px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        
        h1 {
            color: var(--dark);
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: var(--gray);
            font-size: 1.1rem;
            font-weight: 400;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--dark);
        }
        
        input, select, textarea {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border);
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            width: 100%;
            justify-content: center;
        }
        
        .btn:hover {
            background: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
        }
        
        .btn-secondary {
            background: var(--secondary);
        }
        
        .btn-secondary:hover {
            background: #0DA271;
        }
        
        .btn-danger {
            background: var(--danger);
        }
        
        .btn-danger:hover {
            background: #DC2626;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(239, 68, 68, 0.3);
        }
        
        .currency-selector {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 20px;
            justify-content: center;
        }
        
        .expense-card {
            background: var(--light);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 4px solid var(--primary);
        }
        
        .expense-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .expense-title {
            font-weight: 600;
            color: var(--dark);
        }
        
        .expense-amount {
            font-weight: 700;
            color: var(--primary);
        }
        
        .split-details {
            font-size: 14px;
            color: var(--gray);
        }
        
        .balance-card {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .balance-amount {
            font-size: 2rem;
            font-weight: 700;
            margin: 10px 0;
        }
        
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid var(--border);
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: var(--gray);
        }
        
        .tab-container {
            margin-bottom: 20px;
        }
        
        .tabs {
            display: flex;
            background: var(--light);
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 20px;
        }
        
        .tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            background: var(--primary);
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        /* Center align everything in summary */
        .balance-summary-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            height: fit-content;
        }
        
        .balance-summary-card h3,
        .balance-summary-card h4 {
            text-align: center;
            width: 100%;
        }
        
        .balance-summary-card .expense-card {
            margin: 10px 0;
            text-align: center;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 15px;
        }
        
        .balance-summary-card .stats {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
            width: 100%;
        }
        
        .balance-summary-card .stat-card {
            text-align: center;
            min-width: 120px;
        }
        
        .balance-summary-card .balance-card {
            width: 100%;
        }
        
        .reset-section {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            width: 100%;
        }
        
        .split-options {
            background: var(--light);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
        }
        
        .split-option {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .split-option:hover {
            background: white;
        }
        
        .split-option.selected {
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.1);
        }
        
        .split-option input[type="radio"] {
            width: auto;
        }
        
        .split-description {
            font-size: 0.9rem;
            color: var(--gray);
            margin-top: 5px;
        }
        
        @media (max-width: 968px) {
            .main-container {
                flex-direction: column;
                align-items: center;
            }
            
            .form-card, .summary-card {
                max-width: 100%;
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Left Column: Form -->
        <div class="card form-card">
            <div class="header">
                <div class="logo">💸</div>
                <h1>Smart Expense Splitter</h1>
                <p class="subtitle">Split expenses, convert currencies, and settle up effortlessly</p>
            </div>

            <!-- Currency Selector -->
            <div class="currency-selector">
                <label>Base Currency:</label>
                <select name="currency" onchange="updateCurrency(this.value)">
                    {% for curr, rate in exchange_rates.items() %}
                    <option value="{{ curr }}" {% if curr == current_currency %}selected{% endif %}>{{ curr }}</option>
                    {% endfor %}
                </select>
            </div>

            <form method="POST" action="{{ url_for('add_expense') }}">
                <div class="form-group">
                    <label>🏷️ Expense Description</label>
                    <input type="text" name="description" placeholder="Dinner, Rent, Groceries..." required>
                </div>

                <div class="form-group">
                    <label>💵 Amount</label>
                    <input type="number" name="amount" step="0.01" placeholder="Enter amount" required>
                </div>

                <div class="form-group">
                    <label>👥 People Involved (comma separated)</label>
                    <input type="text" name="people" placeholder="John, Jane, Bob..." required id="peopleInput">
                    <small>Enter names separated by commas</small>
                </div>

                <div class="form-group">
                    <label>⚡ Split Type</label>
                    <div class="split-options">
                        <div class="split-option selected" onclick="selectSplitType('equal')">
                            <input type="radio" name="split_type" value="equal" checked>
                            <div>
                                <strong>Equal Split</strong>
                                <div class="split-description">Divide equally among all people</div>
                            </div>
                        </div>
                        
                        <div class="split-option" onclick="selectSplitType('custom')">
                            <input type="radio" name="split_type" value="custom">
                            <div>
                                <strong>Custom Amounts</strong>
                                <div class="split-description">Specify exact amounts for each person</div>
                            </div>
                        </div>
                        
                        <div class="split-option" onclick="selectSplitType('percentage')">
                            <input type="radio" name="split_type" value="percentage">
                            <div>
                                <strong>Percentage Split</strong>
                                <div class="split-description">Split by percentages (must total 100%)</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label>💳 Paid By</label>
                    <select name="paid_by" required id="paidBySelect">
                        <option value="">Select who paid</option>
                    </select>
                </div>

                <button type="submit" class="btn">
                    <span>💾 Add Expense & Split</span>
                </button>
            </form>
        </div>

        <!-- Right Column: Summary -->
        <div class="card summary-card balance-summary-card">
            <h3>💰 Balance Summary</h3>
            
            {% if expenses %}
            <div class="balance-card">
                <div>Total Expenses</div>
                <div class="balance-amount">{{ "%.2f"|format(total_amount) }} {{ current_currency }}</div>
                <div>Across {{ total_people }} people</div>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{{ total_expenses }}</div>
                    <div class="stat-label">Total Expenses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ "%.2f"|format(avg_expense) }}</div>
                    <div class="stat-label">Avg per Expense</div>
                </div>
            </div>

            <h4>🧮 Individual Balances</h4>
            {% for person, balance in person_balances.items() %}
            <div class="expense-card" style="border-left-color: {% if balance >= 0 %}#10B981{% else %}#EF4444{% endif %};">
                <strong>{{ person }}</strong>: 
                <span style="color: {% if balance >= 0 %}#10B981{% else %}#EF4444{% endif %};">
                    {{ "%.2f"|format(balance) }} {{ current_currency }}
                </span>
                {% if balance > 0 %}
                <small style="color: var(--gray);">(owed to them)</small>
                {% elif balance < 0 %}
                <small style="color: var(--gray);">(they owe)</small>
                {% endif %}
            </div>
            {% endfor %}
            
            <!-- Reset Button -->
            <div class="reset-section">
                <a href="{{ url_for('clear_all') }}" class="btn btn-danger" onclick="return confirm('Are you sure you want to clear ALL expenses? This action cannot be undone.')">
                    🗑️ Reset Everything
                </a>
            </div>
            
            {% else %}
            <div class="balance-card">
                <div>No Expenses Yet</div>
                <div class="balance-amount">0.00 {{ current_currency }}</div>
                <div>Add your first expense to see balances</div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">0</div>
                    <div class="stat-label">Total Expenses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">0.00</div>
                    <div class="stat-label">Avg per Expense</div>
                </div>
            </div>
            
            <h4>🧮 Individual Balances</h4>
            <div class="expense-card">
                <strong>No balances to display</strong>
                <div style="color: var(--gray); margin-top: 5px;">Add expenses to see who owes what</div>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        function updateCurrency(currency) {
            window.location.href = `/set_currency?currency=${currency}`;
        }

        function selectSplitType(type) {
            // Update radio buttons
            document.querySelectorAll('input[name="split_type"]').forEach(radio => {
                radio.checked = radio.value === type;
            });
            
            // Update visual selection
            document.querySelectorAll('.split-option').forEach(option => {
                if (option.querySelector('input').value === type) {
                    option.classList.add('selected');
                } else {
                    option.classList.remove('selected');
                }
            });
            
            // Show/hide custom input fields based on selection
            updateSplitInputs();
        }

        function updateSplitInputs() {
            const splitType = document.querySelector('input[name="split_type"]:checked').value;
            const people = document.getElementById('peopleInput').value.split(',').map(p => p.trim()).filter(p => p);
            
            // Remove existing custom inputs
            document.querySelectorAll('.custom-split-inputs, .percentage-split-inputs').forEach(el => {
                el.remove();
            });
            
            if (splitType === 'custom' && people.length > 0) {
                const container = document.createElement('div');
                container.className = 'custom-split-inputs';
                container.innerHTML = '<h4>Custom Amounts:</h4>';
                
                people.forEach(person => {
                    const inputGroup = document.createElement('div');
                    inputGroup.style.margin = '10px 0';
                    inputGroup.innerHTML = `
                        <label>${person}'s share:</label>
                        <input type="number" name="custom_${person}" step="0.01" placeholder="Amount" required>
                    `;
                    container.appendChild(inputGroup);
                });
                
                document.querySelector('.split-options').after(container);
            }
            else if (splitType === 'percentage' && people.length > 0) {
                const container = document.createElement('div');
                container.className = 'percentage-split-inputs';
                container.innerHTML = '<h4>Percentage Split:</h4>';
                
                people.forEach(person => {
                    const inputGroup = document.createElement('div');
                    inputGroup.style.margin = '10px 0';
                    inputGroup.innerHTML = `
                        <label>${person}'s percentage:</label>
                        <input type="number" name="percentage_${person}" step="0.01" placeholder="%" required>
                    `;
                    container.appendChild(inputGroup);
                });
                
                document.querySelector('.split-options').after(container);
            }
        }

        // Populate paid_by dropdown based on people input
        document.getElementById('peopleInput').addEventListener('input', function(e) {
            const people = e.target.value.split(',').map(p => p.trim()).filter(p => p);
            const paidBySelect = document.getElementById('paidBySelect');
            
            // Clear existing options except the first one
            paidBySelect.innerHTML = '<option value="">Select who paid</option>';
            
            // Add new options
            people.forEach(person => {
                const option = document.createElement('option');
                option.value = person;
                option.textContent = person;
                paidBySelect.appendChild(option);
            });
            
            // Update split inputs if needed
            updateSplitInputs();
        });

        // Initialize split type selection
        document.addEventListener('DOMContentLoaded', function() {
            selectSplitType('equal');
        });
    </script>
</body>
</html>
"""

def convert_amount(amount, from_currency, to_currency):
    """Convert amount between currencies"""
    if from_currency == to_currency:
        return amount
    usd_amount = amount / EXCHANGE_RATES[from_currency]
    return usd_amount * EXCHANGE_RATES[to_currency]

def init_session():
    """Initialize session data if not exists"""
    if 'expenses' not in session:
        session['expenses'] = []
    if 'people' not in session:
        session['people'] = []
    if 'currency' not in session:
        session['currency'] = 'USD'

@app.route("/")
def index():
    # Initialize session data
    init_session()
    
    expenses = session.get('expenses', [])
    current_currency = session.get('currency', 'USD')
    
    # Calculate totals in current currency
    total_amount = 0
    person_balances = {}
    
    for expense in expenses:
        # Convert expense amount to current currency
        amount_in_current = convert_amount(expense['amount'], expense['currency'], current_currency)
        total_amount += amount_in_current
        
        # Calculate person balances
        paid_by = expense['paid_by']
        people = expense['people']
        
        # Handle different split types
        if expense['split_type'] == 'equal':
            split_amount = amount_in_current / len(people)
        elif expense['split_type'] == 'custom':
            # For custom splits, use the provided amounts
            # This is simplified - in a real app you'd store custom amounts
            split_amount = amount_in_current / len(people)
        elif expense['split_type'] == 'percentage':
            # For percentage splits, use percentages
            # This is simplified - in a real app you'd store percentages
            split_amount = amount_in_current / len(people)
        else:
            split_amount = amount_in_current / len(people)
        
        if paid_by not in person_balances:
            person_balances[paid_by] = 0
        person_balances[paid_by] += amount_in_current
        
        for person in people:
            if person not in person_balances:
                person_balances[person] = 0
            if person != paid_by:
                person_balances[person] -= split_amount
            else:
                person_balances[person] -= split_amount
    
    # Calculate statistics
    total_expenses = len(expenses)
    avg_expense = total_amount / total_expenses if total_expenses > 0 else 0
    
    # Get all unique people
    all_people = set()
    for expense in expenses:
        all_people.update(expense['people'])
        all_people.add(expense['paid_by'])
    total_people = len(all_people)
    
    return render_template_string(
        HTML_TEMPLATE,
        expenses=expenses,
        total_amount=total_amount,
        total_expenses=total_expenses,
        avg_expense=avg_expense,
        total_people=total_people,
        person_balances=person_balances,
        exchange_rates=EXCHANGE_RATES,
        current_currency=current_currency
    )

@app.route("/add", methods=["POST"])
def add_expense():
    # Initialize session data
    init_session()
    
    description = request.form["description"]
    amount = float(request.form["amount"])
    people = [p.strip() for p in request.form["people"].split(",") if p.strip()]
    split_type = request.form["split_type"]
    paid_by = request.form["paid_by"]
    currency = session.get('currency', 'USD')
    
    expense = {
        "description": description,
        "amount": amount,
        "currency": currency,
        "people": people,
        "split_type": split_type,
        "paid_by": paid_by
    }
    
    expenses = session.get('expenses', [])
    expenses.append(expense)
    session['expenses'] = expenses
    
    # Update people list
    all_people = session.get('people', [])
    for person in people + [paid_by]:
        if person not in all_people:
            all_people.append(person)
    session['people'] = all_people
    
    return redirect(url_for("index"))

@app.route("/set_currency")
def set_currency():
    currency = request.args.get('currency', 'USD')
    session['currency'] = currency
    return redirect(url_for("index"))

@app.route("/clear_all")
def clear_all():
    """Clear all expenses and reset the application"""
    session['expenses'] = []
    session['people'] = []
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    # 🚀 testing CI live run!
