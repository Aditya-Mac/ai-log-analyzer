from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from ai_analysis import get_ai_analysis

import json
import os
import traceback


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the uploads folder automatically if it does not exist.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def analyze_log(filepath):
    info_count = 0
    warning_count = 0
    error_count = 0

    warnings = []
    errors = []

    with open(
        filepath,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as log_file:

        for line in log_file:
            upper_line = line.upper()

            if "ERROR" in upper_line:
                error_count += 1
                errors.append(line.strip())

            elif "WARNING" in upper_line:
                warning_count += 1
                warnings.append(line.strip())

            elif "INFO" in upper_line:
                info_count += 1

    return (
        info_count,
        warning_count,
        error_count,
        warnings,
        errors
    )


def generate_summary(error_count, warning_count):
    if error_count > 0:
        return (
            f"The log contains {error_count} errors and "
            f"{warning_count} warnings. "
            "Immediate investigation is recommended."
        )

    return (
        "No errors were found. "
        f"The log contains {warning_count} warnings."
    )


def generate_recommendations(errors, warnings):
    recommendations = []

    for error_message in errors:
        normalized_error = error_message.lower()

        if "database" in normalized_error:
            recommendations.append(
                "Check database connectivity and credentials."
            )

        if "timeout" in normalized_error:
            recommendations.append(
                "Investigate API response times and network latency."
            )

    for warning_message in warnings:
        normalized_warning = warning_message.lower()

        if "memory" in normalized_warning:
            recommendations.append(
                "Monitor memory utilization."
            )

        if "disk" in normalized_warning:
            recommendations.append(
                "Check available disk space and disk utilization."
            )

    # Remove duplicate recommendations while preserving order.
    recommendations = list(dict.fromkeys(recommendations))

    if not recommendations:
        recommendations.append(
            "No specific rule-based recommendations were generated."
        )

    return recommendations


def build_ai_prompt(errors, warnings):
    error_text = "\n".join(errors)
    warning_text = "\n".join(warnings)

    if not error_text:
        error_text = "No errors found."

    if not warning_text:
        warning_text = "No warnings found."

    prompt = f"""
You are a senior cloud support engineer.

Analyze the following application log entries.

Errors:
{error_text}

Warnings:
{warning_text}

Provide a concise response containing:

1. Root Cause Analysis
2. Severity Level: Low, Medium, High, or Critical
3. Recommended Actions
4. Short Summary

Do not invent details that are not supported by the supplied logs.
"""

    return prompt.strip()


def save_analysis_history(
    filename,
    info_count,
    warning_count,
    error_count
):
    analysis_record = {
        "filename": filename,
        "info": info_count,
        "warning": warning_count,
        "error": error_count
    }

    try:
        with open(
            "analysis_history.json",
            "r",
            encoding="utf-8"
        ) as history_file:
            history = json.load(history_file)

        if not isinstance(history, list):
            history = []

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):
        history = []

    history.append(analysis_record)

    with open(
        "analysis_history.json",
        "w",
        encoding="utf-8"
    ) as history_file:
        json.dump(
            history,
            history_file,
            indent=4
        )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "logfile" not in request.files:
        return "Log file was not included in the request.", 400

    file = request.files["logfile"]

    if file.filename == "":
        return "No file selected.", 400

    filename = secure_filename(file.filename)

    if filename == "":
        return "Invalid file name.", 400

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    (
        info_count,
        warning_count,
        error_count,
        warnings,
        errors
    ) = analyze_log(filepath)

    summary = generate_summary(
        error_count,
        warning_count
    )

    recommendations = generate_recommendations(
        errors,
        warnings
    )

    ai_prompt = build_ai_prompt(
        errors,
        warnings
    )

    print("\n========== AI PROMPT ==========\n")
    print(ai_prompt)
    print("\n===============================\n")

    try:
        ai_result = get_ai_analysis(ai_prompt)

        print("AI result successfully received.")
        print(
            f"AI result length: "
            f"{len(ai_result)} characters"
        )

    except Exception as error:
        print(
            f"AI analysis failed: "
            f"{type(error).__name__}: {error}"
        )

        traceback.print_exc()

        ai_result = (
            "AI analysis is temporarily unavailable. "
            "The standard log analysis is shown below."
        )

    save_analysis_history(
        filename,
        info_count,
        warning_count,
        error_count
    )

    return render_template(
        "result.html",
        filename=filename,
        info=info_count,
        warning=warning_count,
        error=error_count,
        warnings=warnings,
        errors=errors,
        summary=summary,
        recommendations=recommendations,
        ai_result=ai_result
    )


@app.route("/history")
def history():
    try:
        with open(
            "analysis_history.json",
            "r",
            encoding="utf-8"
        ) as history_file:
            records = json.load(history_file)

        if not isinstance(records, list):
            records = []

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):
        records = []

    return render_template(
        "history.html",
        records=records
    )


if __name__ == "__main__":
    app.run(debug=True)