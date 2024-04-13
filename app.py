from flask import Flask, render_template
from accountsdb import load_from_accounts_db

app = Flask(__name__)

@app.route("/")
def mainmenu(): 
  accounts = load_from_accounts_db()
  return render_template('home.html', accounts=accounts)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)


