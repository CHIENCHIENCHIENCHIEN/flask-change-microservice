from flask import Flask, jsonify, request

app = Flask(__name__)

def change(amount):
    res = []
    coins = [25, 10, 5, 1]  # value of quarters, dimes, nickels, pennies
    coin_lookup = {25: "quarters", 10: "dimes", 5: "nickels", 1: "pennies"}

    for coin in coins:
        num, amount = divmod(int(amount * 100), coin)
        if num > 0:
            res.append({coin_lookup[coin]: num})
    return res


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Hello World! I can make change at route: /change'


@app.route('/change/<dollar>/<cents>')
def changeroute(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = float(f"{dollar}.{cents}")
    result = change(amount)
    return jsonify(result)


@app.route('/100/change/<dollar>/<cents>')
def change100route(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = float(f"{dollar}.{cents}") * 100
    print(f"This is the {amount / 100} X 100")
    result = change(amount / 100)  # Divide by 100 to normalize to dollars
    return jsonify(result)


@app.route('/multiply_change', methods=['GET'])
def multiply_change():
    amount = request.args.get('amount', type=float)
    if amount is None:
        return jsonify({"error": "Amount parameter is required"}), 400

    multiplied_change = amount * 100
    print(f"This is the {amount} X 100: {multiplied_change}")

    result = change(amount)  
    return jsonify({"multiplied_change": multiplied_change, "change_breakdown": result})


@app.route('/multiply_change_post', methods=['POST'])
def multiply_change_post():
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({"error": "JSON payload with 'amount' is required"}), 400

    amount = float(data['amount'])
    multiplied_change = amount * 100
    print(f"This is the {amount} X 100: {multiplied_change}")

    result = change(amount)  
    return jsonify({"multiplied_change": multiplied_change, "change_breakdown": result})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

