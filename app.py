from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use absolute path to avoid unexpected DB location issues
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "payment.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DB model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.Float)

# Home route - form page
@app.route('/')
def home():
    return render_template("payment.html")

# Payment route - handles form submission
@app.route('/pay', methods=["POST"])
def pay():
    name = request.form.get("name")
    amount = request.form.get("amount")

    if not name or not amount:
        return "Name and amount are required", 400

    # Save to DB
    transaction = Payment(name=name, amount=float(amount))
    db.session.add(transaction)
    db.session.commit()

    return f"Payment of ${amount} by {name} saved successfully!"

# View all transactions
@app.route('/transactions')
def show_transactions():
    payments = Payment.query.all()
    return render_template("transactions.html", payments=payments)

# Start app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the DB tables if not already there
    app.run(host="0.0.0.0", port=5006, debug=True)

Print("New project update")