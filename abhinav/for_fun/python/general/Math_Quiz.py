import random
import time
import pickle


def load_scores():
    try:
        with open("scores.pkl", "rb") as file:
            scores = pickle.load(file)
    except FileNotFoundError:
        scores = []
    return scores


def save_scores(scores):
    with open("scores.pkl", "wb") as file:
        pickle.dump(scores, file)


def math_quiz(num_questions):
    correct_answers = 0
    total_time = 0
    num_multiplication = int(num_questions * 0.4)
    num_addition = int(num_questions * 0.2)
    num_subtraction = num_questions - num_multiplication - num_addition
    mistakes = []

    print("Welcome to the Math Quiz!")
    print("You will be asked random math questions.")
    print("Please enter your answers as integers.")
    print("Let's begin!\n")

    question_types = ['*', '+', '-']
    print("Ready??")
    input()
    for i in range(num_questions):
        question_type = random.choice(question_types)
        if question_type == '*':
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
        else:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            if question_type == '-':
                num1, num2 = max(num1, num2), min(num1, num2)

        equation = f"{num1} {question_type} {num2}"
        result = eval(equation)

        while True:
            try:
                print(f"Question {i + 1}: What is {equation}?")
                start_time = time.time()
                user_answer = int(input("Your answer: "))
                end_time = time.time()
                total_time += end_time - start_time
                break
            except ValueError:
                print("Invalid input! Please enter an integer.")

        if user_answer == result:
            correct_answers += 1
        else:
            mistakes.append((equation, result, user_answer))

    accuracy = (correct_answers / num_questions) * 100
    avg_time = total_time / num_questions
    overall_score = accuracy * (100 / avg_time)

    print("\nQuiz complete!")
    input()

    print(f"\nAverage time per question: {avg_time:.2f} seconds")
    input()
    print(f"Total time taken: {total_time:.2f} seconds")
    input()
    print(f"Overall score: {overall_score:.2f}")
    input()

    scores = load_scores()
    if scores:
        highest_score = max(scores)
        if overall_score > highest_score:
            print(f"\nCongratulations! You achieved a new high score: {overall_score:.2f}")
        scores.append(overall_score)
        save_scores(scores)
    else:
        print(f"\nCongratulations! You achieved a high score: {overall_score:.2f}")
        scores.append(overall_score)
        save_scores(scores)

    if accuracy != 100:
        show_mistakes = input("Do you want to see the list of mistakes? (yes/no): ")
        if show_mistakes.lower() == "yes":
            print("\nList of Mistakes:")
            for mistake in mistakes:
                equation = mistake[0]
                correct_answer = mistake[1]
                user_answer = mistake[2]
                input("Press any key to show the next mistake...")
                print()
                print(f"{equation} = {correct_answer}; {user_answer}")
                print()
            print("End of mistakes")


def print_scores():
    scores = load_scores()
    if scores:
        print("Scores:")
        for score in scores:
            print(score)
            input()
    else:
        print("No scores found.")


math_quiz(20)
choice = input("Do you want previous scores? (yes/no)")
if choice == "yes":
    print_scores()