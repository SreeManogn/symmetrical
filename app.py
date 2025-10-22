from flask import Flask, render_template, request, redirect
from collections import Counter

app = Flask(__name__)

candidates = []
votes = []  # Only stores candidate names, no voter details

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/candidate', methods=['GET', 'POST'])
def candidate():
    if request.method == 'POST':
        name = request.form['name']
        if name not in candidates:
            candidates.append(name)
        return redirect('/candidate')
    return render_template('candidate.html', candidates=candidates)

@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        selected_candidate = request.form['candidate']
        votes.append(selected_candidate)
        return render_template('student.html', candidates=candidates, message=" Your vote has been recorded anonymously!")
    return render_template('student.html', candidates=candidates)

@app.route('/teacher')
def teacher():
    summary = Counter(votes)
    if summary:
        max_votes = max(summary.values())
        winners = [name for name, count in summary.items() if count == max_votes]
    else:
        winners = []
    return render_template('teacher.html', summary=summary, winners=winners)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
