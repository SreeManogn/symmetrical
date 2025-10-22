from flask import Flask, render_template, request, redirect
from collections import Counter
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'


# --- Helper functions ---
def load_data():
    """Safely load existing data from JSON or create a new one."""
    if not os.path.exists(DATA_FILE):
        data = {"candidates": [], "votes": [], "voting_open": True}
        save_data(data)
        return data
    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # In case file gets corrupted
            data = {"candidates": [], "votes": [], "voting_open": True}
    return data


def save_data(data):
    """Save the entire voting data dictionary to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# --- Load data into memory ---
data = load_data()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/candidate', methods=['GET', 'POST'])
def candidate():
    if request.method == 'POST':
        name = request.form['name'].strip()
        if name and name not in data["candidates"]:
            data["candidates"].append(name)
            save_data(data)
        return redirect('/candidate')
    return render_template('candidate.html', candidates=data["candidates"])


@app.route('/student', methods=['GET', 'POST'])
def student():
    if not data["voting_open"]:
        return render_template('student.html', candidates=[], message="⚠️ Voting has ended. Please wait for the results.")

    if request.method == 'POST':
        selected_candidate = request.form.get('candidate')
        if selected_candidate in data["candidates"]:
            data["votes"].append(selected_candidate)
            save_data(data)
            return render_template('student.html', candidates=data["candidates"], message="✅ Your vote has been recorded anonymously!")

    return render_template('student.html', candidates=data["candidates"])


@app.route('/teacher')
def teacher():
    # Close voting once teacher checks results
    data["voting_open"] = False
    save_data(data)

    summary = Counter(data["votes"])
    winners = []
    if summary:
        max_votes = max(summary.values())
        winners = [name for name, count in summary.items() if count == max_votes]

    return render_template('teacher.html', summary=summary, winners=winners)


@app.route('/reset')
def reset():
    """Reset everything for a new election."""
    data.clear()
    data.update({"candidates": [], "votes": [], "voting_open": True})
    save_data(data)
    return "<h3>✅ Election has been reset successfully. <a href='/'>Return Home</a></h3>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

