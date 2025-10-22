from flask import Flask, render_template, request, redirect
from collections import Counter
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# --- Helper functions ---
def load_data():
    if not os.path.exists(DATA_FILE):
        data = {"candidates": [], "votes": [], "voting_open": True}
        save_data(data)
        return data
    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {"candidates": [], "votes": [], "voting_open": True}
    return data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Load data ---
data = load_data()


# ---------------- ROUTES ----------------

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
        return render_template('student.html', candidates=[], message="⚠️ Voting has ended. Check results.", voting_open=False)

    if request.method == 'POST':
        selected_candidate = request.form.get('candidate')
        if selected_candidate in data["candidates"]:
            data["votes"].append(selected_candidate)
            save_data(data)
            return render_template('student.html', candidates=data["candidates"], message="✅ Your vote has been recorded!", voting_open=True)

    return render_template('student.html', candidates=data["candidates"], voting_open=True)


@app.route('/results', methods=['GET', 'POST'])
def results():
    global data
    if request.method == 'POST':
        # Reset election
        data.clear()
        data.update({"candidates": [], "votes": [], "voting_open": True})
        save_data(data)
        summary = {}
        winners = []
        return render_template('results.html', summary=summary, winners=winners, message="✅ Election has been reset!")

    # Close voting automatically when results page is viewed
    data["voting_open"] = False
    save_data(data)

    summary = Counter(data["votes"])
    winners = []
    if summary:
        max_votes = max(summary.values())
        winners = [name for name, count in summary.items() if count == max_votes]

    return render_template('results.html', summary=summary, winners=winners, message=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
