from flask import Flask, render_template
from accountsdb import load_from_accounts_db

app = Flask(__name__)

@app.route("/")
def mainmenu(): 
  return render_template('home.html')

@app.route("/account")
def account():
  return render_template('account.html')

@app.route("/login")
def login():
  accounts = load_from_accounts_db()
  return render_template('login.html', accounts=accounts)

@app.route("/lessons")
def lessons():
  return render_template('lessons.html')

@app.route("/quiz")
def quiz():
  return render_template('quiz.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)


