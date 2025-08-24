import json
import nbformat
import re
import sys

# Define the correct answers based on the solution file you provided.
CORRECT_ANSWERS = {
    1: 'B',
    2: 'B',
    3: 'C',
    4: 'C',
    5: 'B',
    6: 'B',
    7: 'B',
    8: 'C',
    9: 'B',
    10: 'B'
}

def extract_student_answers(notebook_path):
    """
    Extracts answers from the student's Jupyter Notebook file.
    It looks for the pattern 'Answer X: [answer]' in Markdown cells.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        return {}, f"Error: The file '{notebook_path}' was not found."
    except Exception as e:
        return {}, f"An error occurred while reading the notebook: {e}"

    student_answers = {}
    # Regex to find "Answer X:" followed by the student's response
    answer_pattern = re.compile(r"\*\*Answer\s*(\d+):\s*\[?([A-Da-d])\]?")

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            matches = answer_pattern.findall(cell.source)
            for match in matches:
                try:
                    q_num = int(match[0])
                    answer = match[1].upper()
                    student_answers[q_num] = answer
                except (ValueError, IndexError):
                    continue
    
    if not student_answers:
        return {}, "Could not extract any answers. Please ensure answers are in the format '**Answer X:** [Y]'."
        
    return student_answers, "Answers extracted successfully."

def grade_answers(student_answers):
    """
    Compares student answers to the correct answers and calculates the score.
    """
    score = 0
    total_questions = len(CORRECT_ANSWERS)
    feedback_lines = ["**Grading Summary:**\n"]
    
    for q_num in range(1, total_questions + 1):
        correct_ans = CORRECT_ANSWERS.get(q_num)
        student_ans = student_answers.get(q_num)
        
        if student_ans and student_ans == correct_ans:
            score += 1
            feedback_lines.append(f"- Question {q_num}: Correct ({student_ans})")
        else:
            student_ans_display = student_ans if student_ans else "No Answer"
            feedback_lines.append(f"- Question {q_num}: Incorrect. Your answer: {student_ans_display}, Correct answer: {correct_ans}")
            
    return score, "\n".join(feedback_lines)

def main():
    """
    Main function to run the grading and output results as JSON.
    """
    notebook_path = 'L9_Pareto_Quiz.ipynb'
    student_answers, message = extract_student_answers(notebook_path)
    
    if not student_answers:
        score = 0
        feedback = message
    else:
        score, feedback = grade_answers(student_answers)

    # The autograding action expects a JSON output to assign points.
    test_result = {
        'tests': [
            {
                'name': 'Multiple Choice Quiz',
                'score': score,
                'max_score': 10,
                'output': feedback,
            }
        ]
    }
    
    # Print the JSON to standard output
    print(json.dumps(test_result))

if __name__ == "__main__":
    main()
