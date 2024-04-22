from flask import Flask, render_template
from accountsdb import engine
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql8697943:2HSgWDVuLg@sql8.freemysqlhosting.net/sql8697943'
db = SQLAlchemy(app)

class accounts(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  username = db.Column(db.String(25), unique=True, nullable=False)
  pasword = db.Column(db.String(25), nullable=False)
  email = db.Column(db.String(40), unique=True, nullable=False)


class quiz(db.Model):
  quiz_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  quiz_name = db.Column(db.String(250), nullable=False)
  questions = db.relationship('question', secondary='quiz_question', backref='quizzes')

class taken_quiz(db.Model):
  taken_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  score = db.Column(db.Integer, nullable=False)
  currentq_id = db.Column(db.Integer)
  user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False) #foreign key
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False) #foreign key

class question(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  qnumber = db.Column(db.Integer, nullable=False)
  question = db.Column(db.String(250), nullable=False)
  difficulty_level = db.Column(db.Integer, nullable=False)
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False) #foreign key
  answers = db.relationship('answer', backref='question')
  
class quiz_question(db.Model):
  qq_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  position = db.Column(db.Integer)
  question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False) #foreign key
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False) #foreign key

class answer(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  answer = db.Column(db.String(250), nullable=False)
  question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False) #foreign key
  correct = db.Column(db.Boolean, default=False, nullable=False)


@app.route("/")
def mainmenu_route(): 
  return render_template('home.html')

@app.route("/account")
def account_route():
  return render_template('account.html')

@app.route("/login")
def login_route():
  return render_template('login.html')

@app.route("/lessons")
def lessons_route():
  return render_template('lessons.html')

@app.route("/quiz")
def quiz_route():
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

@app.route("/quiz/heart-walls")
def quiz_walls():
  first_quiz = quiz.query.first()
  if first_quiz:
    first_quiz_name = first_quiz.quiz_name
  else:
    first_quiz_name = 'No quizzes available'
  return render_template('wallsquiz.html', quiz_title = first_quiz_name)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)



