from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = 'recipes.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def add_recipe_page():
    return render_template('add.html')

@app.route('/view')
def view_recipes_page():
    return render_template('view.html')

@app.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify(load_data())

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = load_data()
    new_recipe = {
        "id": len(data) + 1,
        "name": request.form['name'],
        "category": request.form['category'],
        "ingredients": request.form['ingredients'],
        "steps": request.form['steps']
    }
    data.append(new_recipe)
    save_data(data)
    return jsonify({"message": "Recipe added successfully!"})

@app.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    data = load_data()
    data = [r for r in data if r['id'] != recipe_id]
    save_data(data)
    return jsonify({"message": "Recipe deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
