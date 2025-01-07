import math
import random


def generate_equation() -> (int, int, int):
    """
    Generates a simple equation with one unknown and two numbers in the format: num1 * x = num2
    :return: num1, num2 as required in the equation as well as the solution for the value of x
    """
    num1 = random.randint(-20, 20)
    num2 = random.randint(-20, 20)
    num3 = num1 * num2
    while (num1 == num2) | (num1 == num3) | (num2 == num3):
        num1 = random.randint(-20, 20)
        num2 = random.randint(-20, 20)
        num3 = num1 * num2
    return num1, num2, num3


def generate_quadratic_equation() -> (int, int, int, set[int]):
    """
    Generates a quadratic equation and calculates solutions using quadratic formula
    :return: a, b, c which are the coefficients in the formula and the solutions as a set()
    """
    a, b, c = random.randint(-10,10), random.randint(-50,50), random.randint(-100, 100)
    solutions = set()
    solutions.add(round((b*-1 + math.sqrt((b**2 - 4*a*c)))/(2*a), 2) if b**2 - 4*a*c >= 0  else None)
    solutions.add(round((b*-1 - math.sqrt((b**2 - 4*a*c)))/(2*a), 2) if b**2 - 4*a*c >= 0  else None)
    return a, b, c, solutions


def get_int_input(msg:str) -> int:
    """
    Function to get inputs from users while including error checking to ensure that the input is an int as desired
    :param msg: The message that needs to be printed when the input is required
    :return: The user's input as long as it's an int
    """
    while True:
        try:
            user_inp = int(input(msg))
            break
        except ValueError:
            print("That's not a number. Please try again")
    return user_inp


def main():
    """
    Main function that calls other functions and loops through all the questions.
    """
    print("Welcome to your algebra test")
    final_score = 0
    # Dictionary to store all the mistakes so that it can be reviewed later
    # In the format: "Q_num: tuple(Full question, user's answer, solution)"
    mistakes = {}
    # Asks the user for the number of questions they want to complete for flexibility
    total_qs = get_int_input("How many questions do you want to complete?\n")
    simple = True if get_int_input("Choose from the following difficulties:\n\t1)Simple equations\n\t2)Quadratic equations\n") == 1 else False
    for q_num in range(total_qs):
        # Conditional statement that varies question by chosen difficulty
        # Simple equation style questions below
        if simple:
            num1, num2, num3 = generate_equation()
            solution = [num1, num2, num3][random.randint(0, 2)]
            question_str = f"Q{q_num + 1}: {num1 if num1 != solution else "x"} * {num2 if num2 != solution else "x"}"\
                           f" = {num3 if num3 != solution else "x"}\n"
            user_ans = get_int_input(f"{question_str}What is the value of x?\n")
            if user_ans == solution:
                final_score += 1 # Counts the number of correctly answered questions
                print("That's the correct answer!")
            else:
                print(f"That's not quite right. Your answer was {user_ans} but the correct answer was {solution}.")
                mistakes[q_num] = tuple((f"Q{q_num + 1}: {num1} * x = {num2}", user_ans, solution))

        # Quadratic equation style questions below
        else:
            a, b, c, solutions = generate_quadratic_equation()
            user_ans = input(f"Q{q_num + 1}: {a}x^2 + {b}x + {c} = 0.\nWhat are the real solutions of x?\n"
                                     f"Note: Enter your answers split by a space and rounded to 2 d.p. "
                                        f"and enter \"None\" when there are no real solutions.\n")
            user_ans_set = set() # Use of a set to prevent duplicate answers
            for ans in user_ans.split(): # Takes single line of input and unpacks into multiple values
                if ans.lower() != "none":
                    user_ans_set.add(float(ans))
                else:
                    user_ans_set = {None}
            if user_ans_set == solutions:
                final_score += 1
                print(f"That's correct!")
            else:
                print(f"That answer isn't quite correct.")
                mistakes[q_num] = tuple((f"{a}x^2 + {b}x + {c} = 0", user_ans_set, solutions))

    print(f"Your final score is {final_score}/{total_qs} = {round(final_score*100/total_qs, 2)}%")

    # Navigation following the end of the test only if the user didn't get 100%
    if final_score != total_qs:
        nav = input("\nPlease enter E to exit or R to review your mistakes and exit\n")
        if nav.upper() == "E": # Input handling in case the user typed a lower case e/r
            print("The test has now concluded!")
            exit()
        elif nav.upper() == "R":
            print(f"Here are your mistakes:")
            for wrong_q_num in mistakes.keys():
                # Appends the incorrect answer to the dictionary
                print(f"{mistakes[wrong_q_num][0]} and your answer was {mistakes[wrong_q_num][1]} "
                      f"but the correct answer was {mistakes[wrong_q_num][2]}.")
            exit()
        else:
            while nav.upper() not in {"E", "R"}: # Faster looping with sets
                print("That's not a valid input.")
                nav = input("Please enter E to exit or R to review your mistakes and exit\n")

    else:
        print("Congratulations you have got full marks! The test will now conclude!")
        exit()


main()
