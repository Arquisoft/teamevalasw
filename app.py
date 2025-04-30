from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import os
from filelock import FileLock

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for production
LOCK_FILE = "evaluations.xlsx.lock"
EVALUATIONS_FILE = "evaluations.xlsx"

# Load credentials
def load_credentials():
    with open('users.txt') as f:
        lines = f.readlines()
    return dict(line.strip().split(':') for line in lines)

# Load user metadata
def load_user_data():
    return pd.read_excel('data.xlsx')

# Save evaluation
def save_evaluation(evaluator, evaluations):
    df = pd.DataFrame(evaluations)
    df['evaluator'] = evaluator
    with FileLock(LOCK_FILE):
        file_exists = os.path.exists(EVALUATIONS_FILE)
        if file_exists:
            existing = pd.read_excel(EVALUATIONS_FILE)
            existing = existing[existing["evaluator"] != evaluator]
            df = pd.concat([existing, df], ignore_index=True)
        df.to_excel(EVALUATIONS_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        credentials = load_credentials()
        if username in credentials and credentials[username] == password:
            session['username'] = username
            return redirect(url_for('evaluate'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    data = load_user_data()
    user_row = data[data['user'] == username].iloc[0]
    group_users = data[(data['group'] == user_row['group']) & (data['user'] != username)]
    group_name = user_row['group']

    previous_evals = {}
    with FileLock(LOCK_FILE):
        if os.path.exists(EVALUATIONS_FILE):
            eval_df = pd.read_excel(EVALUATIONS_FILE)
            user_evals = eval_df[eval_df["evaluator"] == username]
            for _, row in user_evals.iterrows():
                previous_evals[row["evaluatee"]] = {
                    "respeto_empatia": row["respeto_empatia"],
                    "participacion": row["participacion"],
                    "cumplimiento": row["cumplimiento"],
                    "git": row["git"],
                }

    if request.method == 'POST':
        evaluations = []
        for user in group_users['user']:
            evaluation = {
                'evaluatee': user,
                'respeto_empatia': int(request.form[f'respeto_{user}']),
                'participacion': int(request.form[f'participacion_{user}']),
                'cumplimiento': int(request.form[f'cumplimiento_{user}']),
                'git': int(request.form[f'git_{user}'])
            }
            evaluations.append(evaluation)
        save_evaluation(username, evaluations)
        return render_template('success.html')

    return render_template("evaluate.html", group_users=group_users, group_name=group_name, previous_evals=previous_evals)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False, port=5000)
