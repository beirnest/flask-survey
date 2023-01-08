from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "nobody-knows"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

counter = [0]

@app.route('/')
def root():
    """Show Survey Home Page with survey title and instructions."""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("base.html", title = title, instructions = instructions)

@app.route('/start', methods=["POST"])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<question_number>')
def show_questions(question_number):
    """Show each question and its answers."""
    if counter[0] < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[counter[0]].question
        choices = satisfaction_survey.questions[counter[0]].choices
        if question_number != (str(counter[0])):
            flash("You're attempting to access a restricted question!")
        return render_template("questions.html", question = question, choices = choices, question_number = counter[0], satisfaction_survey_length = len(satisfaction_survey.questions))
    
    else:
        return render_template("thanks.html")

@app.route('/answer/<question_number>', methods=["POST"])
def post_answers(question_number):
    """Post answers to reponses"""

    if counter[0] < len(satisfaction_survey.questions):

        answer = request.form["answer"]

        responses = session['responses']
        responses.append(answer)
        session['responses'] = responses

        question_num = int(question_number) + 1

        counter[0] = counter[0] + 1

        if question_num < len(satisfaction_survey.questions):
            return redirect("/questions/" + str(counter[0]))

        elif question_num >= len(satisfaction_survey.questions):
            return redirect("/thanks")
    
    else:
        return render_template("thanks.html")

@app.route('/thanks')
def show_end():
    """Show the confirmation page."""

    return render_template("thanks.html")