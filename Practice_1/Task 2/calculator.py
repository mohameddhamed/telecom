import json
import sys

"""
Write a script that computes how many points you have to score for each grade. 
The input is a json file that contains the maximal,minimum, and received scores for the mininet and homeworks, 
also, the maximal score attainable for the exam as well as the minimal percentage needed for passing the exam.  
"""


def calculate_required_exam_points(data_file_path):
    """
    This function calculates the minimum exam points required to achieve each possible passing grade (2 through 5)
    based on the provided scores in the JSON file. It assumes the course has three equally weighted components:
    - Homework
    - Mininet
    - Exam (referred to as 'zh' in the JSON)

    Each component is weighted at 1/3 of the final grade. To pass the course and achieve grades 2-5:
    - Each component must individually achieve at least its minimum qualifying percentage (default 50%).
    - The overall weighted average percentage must meet or exceed the threshold for the desired grade.

    If homework or mininet scores are below their minimum, achieving grades 2-5 is impossible regardless of exam performance.

    Grade thresholds (minimum overall percentages):
    - Grade 2: 40%
    - Grade 3: 60%
    - Grade 4: 80%
    - Grade 5: 100% (perfect score required for the highest grade)

    The function reads the JSON, performs checks, and computes the required exam points for each grade.
    """

    # Step 1: Load the JSON data from the provided file path
    # We use try-except to handle common errors like file not found or invalid JSON format
    try:
        with open(data_file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{data_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from '{data_file_path}'. Check file format."
        )
        sys.exit(1)

    # Step 2: Extract data for each component from the JSON
    # We use .get() to safely access keys, with defaults if not present
    # Note: Adjusted keys to match the example JSON ('homework', 'mininet', 'zh')
    # 'min' values are treated as factors (e.g., 0.5 for 50%)
    homework_data = data.get("homework", {})
    exam_data = data.get("zh", {})
    mininet_data = data.get("mininet", {})

    # Homework details
    hw_max = homework_data.get("max", 20)  # Maximum possible points for homework
    hw_received = homework_data.get("received", 0)  # Points already received
    hw_min_qualify_factor = homework_data.get(
        "min", 0.5
    )  # Minimum qualifying factor (e.g., 0.5 = 50%)

    # Mininet details
    mininet_max = mininet_data.get("max", 20)
    mininet_received = mininet_data.get("received", 0)
    mininet_min_qualify_factor = mininet_data.get("min", 0.5)

    # Exam details (exam not yet taken, so only max and min qualify)
    exam_max = exam_data.get("max", 20)
    exam_min_qualify_factor = exam_data.get("min", 0.5)

    # Step 3: Calculate achieved percentages for homework and mininet
    # Percentage = (received / max) * 100, with safeguard for division by zero
    hw_percent = (hw_received / hw_max * 100) if hw_max > 0 else 0
    mininet_percent = (mininet_received / mininet_max * 100) if mininet_max > 0 else 0

    # Step 4: Check if homework or mininet fail the minimum qualification
    # If either is below min, print a warning and flag that passing grades are impossible
    hw_min_qualify_percent = hw_min_qualify_factor * 100
    mininet_min_qualify_percent = mininet_min_qualify_factor * 100

    impossible_due_to_components = False
    if hw_percent < hw_min_qualify_percent:
        print(
            f"Warning: Homework score ({hw_percent:.1f}%) is below required minimum ({hw_min_qualify_percent:.1f}%). Grades 2-5 are impossible."
        )
        impossible_due_to_components = True
    if mininet_percent < mininet_min_qualify_percent:
        print(
            f"Warning: Mininet score ({mininet_percent:.1f}%) is below required minimum ({mininet_min_qualify_percent:.1f}%). Grades 2-5 are impossible."
        )
        impossible_due_to_components = True

    # Step 5: Define component weights and target overall percentages for each grade
    # All components are equally weighted at 1/3
    weight_per_component = 1 / 3

    # Target minimum overall percentages for each grade
    target_percentages = {
        2: 40,  # Minimum for grade 2
        3: 60,  # Minimum for grade 3
        4: 80,  # Minimum for grade 4
        5: 100,  # Minimum for grade 5 (requires perfect overall score)
    }

    # Dictionary to store results for each grade
    results = {}

    # Step 6: For each grade, calculate the required exam points
    for grade, target_overall in target_percentages.items():
        # If components already fail, skip calculations and mark as impossible for passing grades
        if impossible_due_to_components:
            results[grade] = "Impossible"
            continue

        # Calculate current contribution from homework and mininet to the overall percentage
        # This is the sum of their weighted percentages: (hw_percent * weight) + (mininet_percent * weight)
        current_contribution = (hw_percent * weight_per_component) + (
            mininet_percent * weight_per_component
        )

        # Required contribution from exam: target_overall - current_contribution
        required_exam_contribution = target_overall - current_contribution

        # Required exam percentage = required_contribution / weight (since contribution = percent * weight)
        required_exam_percent = (
            required_exam_contribution / weight_per_component
            if weight_per_component > 0
            else float("inf")
        )

        # Exam must also meet its own minimum qualification (e.g., 50%)
        min_exam_percent = exam_min_qualify_factor * 100

        # Effective required exam percent is the maximum of:
        # - What's needed for the overall target
        # - The component's own minimum
        effective_required_percent = max(required_exam_percent, min_exam_percent)

        # Step 7: Check if the required percentage is achievable (<= 100%)
        if effective_required_percent > 100:
            results[grade] = "Impossible"
        else:
            # Convert percentage to points: (percent / 100) * exam_max, rounded to 1 decimal place
            points_needed = round((effective_required_percent / 100) * exam_max, 1)

            # Safeguard: If points exceed max (due to rounding), mark as impossible
            if points_needed > exam_max:
                results[grade] = "Impossible"
            else:
                # Ensure non-negative points
                results[grade] = max(0.0, points_needed)

    return results


# Main execution: Run the script with the JSON file path as a command-line argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python calculator.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    calculated_grades = calculate_required_exam_points(json_file_path)

    # Print results sorted by grade
    for grade in sorted(calculated_grades.keys()):
        print(f"{grade} : {calculated_grades[grade]}")
