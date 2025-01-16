from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)


def generate_equation():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    while num2 == num1:
        num2 = random.randint(1, 10)
    num3 = num1 * num2
    return num1, num2, num3


def generate_quadratic_equation():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    delta = b ** 2 - 4 * a * c
    if delta > 0:
        sol1 = (-b + delta ** 0.5) / (2 * a)
        sol2 = (-b - delta ** 0.5) / (2 * a)
        solutions = {sol1, sol2}
    elif delta == 0:
        sol = -b / (2 * a)
        solutions = {sol}
    else:
        solutions = {None}
    return a, b, c, solutions


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user's selections and choices
        difficulty = request.form.get('difficulty')
        total_questions = int(request.form.get('total_questions'))

        # Redirect based on the difficulty level
        if difficulty == 'simple':
            return redirect(url_for('simple', total_num_questions=total_questions))
        else:
            return redirect(url_for('quadratic', total_num_questions=total_questions))

    # Render the index page
    return render_template('index.html')


@app.route('/simple/<total_num_questions>', methods=['GET', 'POST'])
def simple(total_num_questions: int):

    if request.method == 'GET':
        global questions_list
        questions_list = []
        for q_num in range(int(total_num_questions)):
            num1, num2, num3 = generate_equation()
            solution = [num1, num2, num3][random.randint(0, 2)]
            question_str = f"Q{q_num + 1}: {num1 if num1 != solution else 'x'} * {num2 if num2 != solution else 'x'} = {num3 if num3 != solution else 'x'}"
            questions_list.append((question_str, solution))

    elif request.method == 'POST':
        final_score = 0
        mistakes = {}
        for q_num in range(int(total_num_questions)):
            user_ans = int(request.form.get(f'user_answer_{q_num}'))
            question_str, solution = questions_list[q_num]
            if user_ans == solution:
                final_score += 1
            else:
                mistakes[
                    q_num] = f"{question_str}, Your answer was {user_ans}, but the correct answer was {solution}."

        final_score_percentage = round(final_score * 100 / int(total_num_questions), 2)
        return render_template('results.html', final_score=final_score, total_questions=total_num_questions,
                               final_score_percentage=final_score_percentage, mistakes=mistakes)

    return render_template('simple.html', questions_list=questions_list, submitted=False)


@app.route('/quadratic/<total_num_questions>', methods=['GET', 'POST'])
def quadratic(total_num_questions: int):
    questions_list = []
    for q_num in range(int(total_num_questions)):
        a, b, c, solutions = generate_quadratic_equation()
        question_str = f"Q{q_num + 1}: {a}x^2 + {b}x + {c} = 0. What are the real solutions of x?"
        questions_list.append((question_str, solutions))

    if request.method == 'POST':
        final_score = 0
        mistakes = {}
        for q_num in range(int(total_num_questions)):
            user_ans = request.form.get(f'user_answer_{q_num}')
            user_ans_set = set()
            for ans in user_ans.split():
                if ans.lower() != "none":
                    user_ans_set.add(float(ans))
                else:
                    user_ans_set = {None}
            _, solutions = questions_list[q_num]
            if user_ans_set == solutions:
                final_score += 1
            else:
                mistakes[
                    q_num] = f"{a}x^2 + {b}x + {c} = 0, Your answer was {user_ans_set}, but the correct answer was {solutions}."

        final_score_percentage = round(final_score * 100 / total_num_questions, 2)
        return render_template('results.html', final_score=final_score, total_questions=total_num_questions,
                               final_score_percentage=final_score_percentage, mistakes=mistakes)

    return render_template('quadratic.html', questions=questions_list, submitted=False)


if __name__ == "__main__":
    app.run(debug=True)