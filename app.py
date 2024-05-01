from flask import Flask, render_template, request, redirect, url_for, session
from accountsdb import engine
from sqlalchemy import text, func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, relationship, aliased
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql8697943:2HSgWDVuLg@sql8.freemysqlhosting.net/sql8697943'
db = SQLAlchemy(app)

class accounts(db.Model):
  user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
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
  user_id = db.Column(db.Integer, db.ForeignKey('accounts.user_id'), nullable=False) #foreign key
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False) #foreign key

class question(db.Model):
  question_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  qnumber = db.Column(db.Integer, nullable=False)
  question = db.Column(db.String(250), nullable=False)
  difficulty_level = db.Column(db.Integer, nullable=False)
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False) #foreign key
  answers = db.relationship('answer', backref='question')

class quiz_question(db.Model):
  qq_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  position = db.Column(db.Integer)
  question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False) #foreign key
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False) #foreign 
  question = db.relationship('question', backref='quiz_questions')

class answer(db.Model):
  answer_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  answer = db.Column(db.String(250), nullable=False)
  question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False) #foreign key
  correct = db.Column(db.Boolean, default=False, nullable=False)

@app.route("/")
def mainmenu_route(): 
  return render_template('home.html')

@app.route("/account")
def account_route():
  return render_template('account.html')

@app.route("/login", methods=['GET', 'POST'])
def login_route():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user = accounts.query.filter_by(username=username, pasword=password).first()
    if user:
      session['user_id'] = user.user_id
      return redirect(url_for('mainmenu_route'))
    else:
      error_message = 'Invalid username or password. Please try again, or create an account to continue.'
      return render_template('login.html', error_message=error_message)
  return render_template('login.html')

@app.route("/lessons")
def lessons_route():
  return render_template('lessons.html')

@app.route("/quiz")
def quiz_route():
  session['quiz_score'] = 0
  session.pop('answered_questions', None)
  session.pop('answered_correctly', None)
  if 'user_id' in session:
    user_id = session['user_id']
    first_quiz = quiz.query.first()
    if first_quiz:
      quiz_id = first_quiz.quiz_id
      taken_quiz_record = taken_quiz.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
      if taken_quiz_record:
        taken_quiz_record.score = 0
        db.session.commit()
      else:
        taken_quiz_record = taken_quiz(user_id=user_id, quiz_id=quiz_id, score=0)
        db.session.add(taken_quiz_record)
      db.session.commit()
  return render_template('quiz.html')


@app.route("/quiz-history")
def quiz_history():
    if 'user_id' in session:
        user_id = session['user_id']
        subquery = db.session.query(taken_quiz.quiz_id, func.max(taken_quiz.taken_id).label('max_taken_id')).group_by(taken_quiz.quiz_id).subquery()
        user_quizzes = db.session.query(taken_quiz).join(subquery, taken_quiz.taken_id == subquery.c.max_taken_id).filter(taken_quiz.user_id == user_id).all()

        quizzes = {quiz.quiz_id: quiz for quiz in quiz.query.all()}
        return render_template('quiz history.html', user_quizzes=user_quizzes, quizzes=quizzes)
    else:
        return redirect(url_for('login_route'))


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


@app.route("/quiz/heart-chambers")
def quiz_chambers():
  first_quiz = quiz.query.first()
  if first_quiz:
    first_quiz_name = first_quiz.quiz_name
  else:
    first_quiz_name = 'No quizzes available'
  return render_template('chambersquiz.html', quiz_title = first_quiz_name)



@app.route("/quiz/<int:quiz_id>/<int:question_number>", methods=['GET', 'POST'])
def quiz_questions(quiz_id, question_number):
    current_question = question.query.filter_by(quiz_id=quiz_id, qnumber=question_number).first_or_404()
    if 'answered_questions' not in session:
        session['answered_questions'] = []

    if current_question.question_id in session['answered_questions']:
        return redirect(url_for('quiz_summary', quiz_id=quiz_id))

    answers = answer.query.filter_by(question_id=current_question.question_id).all()
    quiz_obj = quiz.query.get(quiz_id)

    if request.method == 'POST':
        selected_answer_id = int(request.form['answer'])
        selected_answer = answer.query.get(selected_answer_id)

        if selected_answer and selected_answer.correct:
            if 'user_id' in session:
                user_id = session['user_id']
                if current_question.question_id not in session.get('answered_correctly', []):
                    taken_quiz_record = taken_quiz.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
                    if taken_quiz_record:
                        taken_quiz_record.score += 1
                    else:
                        taken_quiz_record = taken_quiz(user_id=user_id, quiz_id=quiz_id, score=1)
                        db.session.add(taken_quiz_record)
                    db.session.commit()
                    session.setdefault('answered_correctly', []).append(current_question.question_id)
            session['answered_questions'].append(current_question.question_id)

        next_question_number = question_number + 1
        next_question = question.query.filter_by(quiz_id=quiz_id, qnumber=next_question_number).first()
        if next_question:
            return redirect(url_for('quiz_questions', quiz_id=quiz_id, question_number=next_question_number))
        else:
            return redirect(url_for('quiz_summary', quiz_id=quiz_id))

    return render_template('chambersq.html', current_question=current_question, answers=answers, quiz=quiz_obj)




@app.route("/quiz/<int:quiz_id>/summary")
def quiz_summary(quiz_id):
  if 'user_id' in session:
    user_id = session['user_id']
    taken_quiz_record = taken_quiz.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
    score = taken_quiz_record.score if taken_quiz_record else 0

    quiz_obj = quiz.query.get(quiz_id)
    questions = quiz_obj.questions 
    num_questions = len(quiz_obj.questions)

    return render_template('quiz summary.html', score=score, quiz=quiz_obj, questions=questions, num_questions=num_questions)
  else:
    return render_template('login.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

