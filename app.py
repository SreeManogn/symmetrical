from flask import Flask, render_template, request, redirect
from collections import Counter
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# --- Helper functions ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data.get('candidates', []), data.get('votes', []), data.get('voting_open', True)
    return [], [], True

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump({'candidates': candidates, 'votes': votes, 'voting_open': voting_open}, f)

# --- Load initial data ---
candidates, votes, voting_open = load_data()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/candidate', methods=['GET', 'POST'])
def candidate():
    if request.method == 'POST':
        name = request.form['name']
        if name not in candidates:
            candidates.append(name)
            save_data()
        return redirect('/candidate')
    return render_template('candidate.html', candidates=candidates)


@app.route('/student', methods=['GET', 'POST'])
def student():
    global votes
    if not voting_open:
        # If voting has ended
        return render_template('student.html', candidates=[], message="⚠️ Voting has ended. Please wait for the results.")
    
    if request.method == 'POST':
        selected_candidate = request.form['candidate']
        votes.append(selected_candidate)
        save_data()
        return render_template('student.html', candidates=candidates, message="✅ Your vote has been recorded anonymously!")
    
    return render_template('student.html', candidates=candidates)


@app.route('/teacher')
def teacher():
    global voting_open
    summary = Counter(votes)
    winners = []
    if summary:
        max_votes = max(summary.values())
        winners = [name for name, count in summary.items() if count == max_votes]

    # Close voting once teacher page is opened
    voting_open = False
    save_data()

    return render_template('teacher.html', summary=summary, winners=winners)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
