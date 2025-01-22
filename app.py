from flask import Flask, jsonify, request
import sqlite3

DATABASE = 'change_history.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount REAL NOT NULL,
                multiplied_change REAL NOT NULL,
                change_breakdown TEXT NOT NULL
            )
        ''')
        conn.commit()

def log_change(user_id, amount, multiplied_change, change_breakdown):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO history (user_id, amount, multiplied_change, change_breakdown)
            VALUES (?, ?, ?, ?)
        ''', (user_id, amount, multiplied_change, str(change_breakdown)))
        conn.commit()

def fetch_history(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, amount, multiplied_change, change_breakdown 
            FROM history 
            WHERE user_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()
    return rows



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
    user_id = request.args.get('user_id', type=str, default='anonymous')
    if amount is None:
        return jsonify({"error": "Amount parameter is required"}), 400

    multiplied_change = amount * 100
    print(f"Multiplying the amount {amount} by 100: {multiplied_change}")
    result = change(amount)  

    log_change(user_id, amount, multiplied_change, result)

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

@app.route('/history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id', type=str, default='anonymous')
    rows = fetch_history(user_id)
    history = [
        {
            "id": row[0],
            "amount": row[1],
            "multiplied_change": row[2],
            "change_breakdown": row[3],
        }
        for row in rows
    ]
    return jsonify({"user_id": user_id, "history": history})

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=8080, debug=True)

