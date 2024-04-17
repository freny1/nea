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

@app.route("/quiz-history")
def quiz_history():
  return render_template('quiz history.html')

@app.route("/lessons/blood-vessels")
def lessons_blood_vessels():
  return render_template('bloodvessels.html')

@app.route("/lessons/heart-walls")
def lessons_walls():
  return render_template('walls.html')

@app.route("/lessons/heart-chambers")
def lessons_chambers():
  return render_template('chambers.html')

@app.route("/lessons/heart-valves")
def lessons_valves():
  return render_template('valves.html')

@app.route("/lessons/electrical-conduction-system")
def lessons_ecs():
  return render_template('ecs.html')




if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)



