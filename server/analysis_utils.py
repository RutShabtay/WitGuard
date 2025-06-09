import ast
import os
import matplotlib.pyplot as plt
import csv
from datetime import datetime



def analyze_code(code_text:str,file_name:str,history_dir: str)->dict:
    tree = ast.parse(code_text)
    function_lengths = {}
    issues = {
        "long_functions": [],
        "long_file": [],
        "unused_variables": [],
        "missing_docstrings": [],
        "non_english_variables": []
    }

    #check if the file length is longer than 200
    lines=code_text.splitlines()
    if len(lines) > 200:
        issues["long_file"].append(f"{file_name}: File is longer than 200 lines ({len(lines)})")

    #Identifying functions that are too long and without a docstring
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            line_numbers = [child.lineno for child in ast.walk(node) if hasattr(child, 'lineno')]

            if line_numbers:
                end = max(line_numbers)
            else:
                end = start

            length = end - start + 1
            function_lengths[node.name] = length

            if length > 20:
                issues["long_functions"].append(f"{file_name}: Function '{node.name}' is too long ({length} lines)")

            if not ast.get_docstring(node):
                issues["missing_docstrings"].append(f"{file_name}: Function '{node.name}' missing docstring")

    #Unused variables
    used_names = set()
    assigned_names = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Assign):
                    for target in subnode.targets:
                        if isinstance(target, ast.Name):
                            assigned_names[target.id] = (subnode.lineno, func_name)

        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used_names.add(node.id)

    for var, (lineno, func_name) in assigned_names.items():
        if var not in used_names:
            issues["unused_variables"].append(
                f"{file_name}: Variable '{var}' assigned in function '{func_name}' but never used"
            )

        if not var.isascii():
            issues["non_english_variables"].append(
                f"{file_name}: Variable '{var}' in function '{func_name}' is not in English"
            )
    issue_counts = {k: len(v) for k, v in issues.items()}
    total_issues = sum(issue_counts.values())
    log_analysis(file_name,total_issues,history_dir)

    return{
        "issues": issues,
        "function_lengths": function_lengths
    }



#Histogram of Function Lengths
def plot_histogram(function_lengths, out_path):
    plt.figure(figsize=(8,6))
    plt.hist(function_lengths, bins=range(1, max(function_lengths)+2), edgecolor='black')
    plt.title("Histogram of Function Lengths")
    plt.xlabel("Function Length (lines)")
    plt.ylabel("Number of Functions")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

#Issue Types Distribution
def plot_pie(issue_counts, out_path):
    plt.figure(figsize=(6, 6))
    labels = list(issue_counts.keys())
    sizes = list(issue_counts.values())
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Issue Types Distribution")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


#Number of Issues per File
def plot_bar(issues_per_file, out_path):
    plt.figure(figsize=(10,6))
    files = list(issues_per_file.keys())
    counts = list(issues_per_file.values())
    plt.bar(files, counts, color='skyblue')
    plt.title("Number of Issues per File")
    plt.xlabel("File Name")
    plt.ylabel("Number of Issues")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


#Generates and saves a line chart showing the trend of total issues over time based on a CSV log file.
def plot_issue_trend(csv_path: str, out_path: str):
    timestamps = []
    issue_counts = []

    if not os.path.exists(csv_path):
        return  # No history yet

    with open(csv_path, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
            issue_counts.append(int(row["total_issues"]))

    if not timestamps:
        return

    plt.figure(figsize=(10,6))
    plt.plot(timestamps, issue_counts, marker='o', linestyle='-', color='green')
    plt.title("Issue Trend Over Time")
    plt.xlabel("Time")
    plt.ylabel("Number of Issues")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


#Logs the results of a code analysis to a CSV file, including timestamp, file name, and total issue count.
def log_analysis(file_name: str, total_issues: int,history_dir: str):
    log_path = os.path.join(history_dir, "analysis_log.csv")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_new_file = not os.path.exists(log_path)

    with open(log_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(["timestamp", "filename", "total_issues"])
        writer.writerow([now, file_name, total_issues])