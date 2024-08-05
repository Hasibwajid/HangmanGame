from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Words categorized by their types and languages
categories = {
    'en': {
        'Animals': ['lion', 'cat', 'tiger', 'dog', 'elephant'],
        'Objects': ['table', 'chair', 'lamp', 'phone', 'pencil'],
        'Fruits': ['apple', 'banana', 'cherry', 'grape', 'orange'],
        'Countries': ['brazil', 'canada', 'china', 'france', 'germany']
    },
    'es': {
        'Animales': ['león', 'gato', 'tigre', 'perro', 'elefante'],
        'Objetos': ['mesa', 'silla', 'lámpara', 'teléfono', 'lápiz'],
        'Frutas': ['manzana', 'plátano', 'cereza', 'uva', 'naranja'],
        'Países': ['brasil', 'canadá', 'china', 'francia', 'alemania']
    }
}

languages = {'en': 'English', 'es': 'Español'}
current_language = 'en'
category, words = random.choice(list(categories[current_language].items()))
random_word = random.choice(words)
guessed_word = ['_'] * len(random_word)
tries = 0
num_of_guess = len(random_word)

@app.route('/')
def index():
    return render_template('index.html', category=category, guessed_word=' '.join(guessed_word), tries=num_of_guess, languages=languages, current_language=current_language)

@app.route('/guess', methods=['POST'])
def guess():
    global guessed_word, tries
    inp = request.form['character'].lower()

    if inp and len(inp) == 1:
        if inp not in random_word:
            tries += 1
            if tries >= num_of_guess:
                return jsonify(status='gameover', guessed_word=' '.join(guessed_word), word=random_word)
        else:
            indices = [j for j, x in enumerate(random_word) if x == inp]
            for index in indices:
                guessed_word[index] = inp
            if '_' not in guessed_word:
                return jsonify(status='win', guessed_word=' '.join(guessed_word), word=random_word)
        return jsonify(status='continue', guessed_word=' '.join(guessed_word), tries=num_of_guess-tries)
    return jsonify(status='invalid')

@app.route('/hint', methods=['GET'])
def hint():
    hint_char = random.choice([ch for ch in random_word if ch not in guessed_word])
    return jsonify(hint=hint_char)

@app.route('/change_language', methods=['POST'])
def change_language():
    global current_language, category, words, random_word, guessed_word, tries, num_of_guess
    current_language = request.form['language']
    category, words = random.choice(list(categories[current_language].items()))
    random_word = random.choice(words)
    guessed_word = ['_'] * len(random_word)
    tries = 0
    num_of_guess = len(random_word)
    return jsonify(status='success', category=category, guessed_word=' '.join(guessed_word), tries=num_of_guess, current_language=current_language)

if __name__ == "__main__":
    app.run(debug=True)
