from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    costs = {}
    return render_template('index.html', costs=costs)

# Dont really know if this is the best way to do this but I was just making some quick
@app.route('/', methods=['POST'])
def split():
    costs = convert_to_dict(request.form)
    total = sum(costs.values())
    share = total / len(costs)

    # Calculate how much each person should owe
    payments = {name: paid - share for name, paid in costs.items()}

    # Find who needs to pay who
    payers = {name: round(-payment, 2) for name, payment in payments.items() if payment < 0}
    receivers = {name: round(payment, 2) for name, payment in payments.items() if payment > 0}

    # Calculate payments
    contracts = []
    for receiver, receiver_amount in receivers.items():
        for payer, amount in payers.items():       
            if receiver_amount==0:    
                break
            elif amount <= receivers[receiver]:
                if amount!=0:
                    receivers.update({receiver: round(receivers[receiver]-amount, 2)})
                    payers.update({payer: 0})
                    contracts.append((payer, receiver, round(amount, 2)))    
            else:
                contracts.append((payer, receiver, round(receivers[receiver], 2))) 
                payers.update({payer: round(amount-receivers[receiver], 2)})
                receivers.update({receiver: 0})
                break

    return render_template('index.html', data=contracts, costs=costs)

# Converts whatever that imutable dict is to a dict we can use
def convert_to_dict(input):
    d = dict(input)
    new_dict = {}

    for i in range(1, len(d)//2 + 1):
        key = d[f'name{i}']
        value = float(d[f'moneys{i}'])
        new_dict[key] = value

    return new_dict

if __name__ == '__main__':
    app.run(debug=True)