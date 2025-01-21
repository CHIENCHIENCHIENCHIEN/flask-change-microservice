from flask import Flask
from flask import jsonify
app = Flask(__name__)

def change(amount):
    # calculate the resultant change and store the result (res)
    res = []
    coins = [1,5,10,25] # value of pennies, nickels, dimes, quarters
    coin_lookup = {25: "quarters", 10: "dimes", 5: "nickels", 1: "pennies"}

    # divide the amount*100 (the amount in cents) by a coin value
    # record the number of coins that evenly divide and the remainder
    coin = coins.pop()
    num, rem  = divmod(int(amount*100), coin)
    # append the coin type and number of coins that had no remainder
    res.append({num:coin_lookup[coin]})

    # while there is still some remainder, continue adding coins to the result
    while rem > 0:
        coin = coins.pop()
        num, rem = divmod(rem, coin)
        if num:
            if coin in coin_lookup:
                res.append({num:coin_lookup[coin]})
    return res


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Hello World! I can make change at route: /change'

@app.route('/change/<dollar>/<cents>')
def changeroute(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    result = change(float(amount))
    return jsonify(result)
    
    
@app.route('/100/change/<dollar>/<cents>')
def change100route(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    amount100 = float(amount) * 100
    print(f"This is the {amount} X 100")
    result = change(amount100)
    return jsonify(result)

@app.route('/multiply_change', methods=['GET'])
def multiply_change():
    # Extract 'amount' from query parameters
    amount = request.args.get('amount', type=float)
    if amount is None:
        return jsonify({"error": "Amount parameter is required"}), 400

    # Multiply the amount by 100
    multiplied_change = amount * 100

    # Print a logging message
    print(f"This is the {amount} X 100: {multiplied_change}")

    # Return the result as JSON
    return jsonify({"multiplied_change": multiplied_change})

@app.route('/multiply_change_post', methods=['POST'])
def multiply_change_post():
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({"error": "JSON payload with 'amount' is required"}), 400

    amount = float(data['amount'])
    multiplied_change = amount * 100
    print(f"This is the {amount} X 100: {multiplied_change}")
    return jsonify({"multiplied_change": multiplied_change})



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
