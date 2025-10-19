from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
API_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'meta-llama/llama-3.2-3b-instruct:free'

def call_ai(messages):
    if not OPENROUTER_API_KEY:
        raise Exception('Configuration requise')
    
    response = requests.post(
        API_URL,
        headers={
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={'model': MODEL, 'messages': messages},
        timeout=90
    )
    
    if response.status_code != 200:
        raise Exception(f"Erreur {response.status_code}")
    
    return response.json()['choices'][0]['message']['content']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lesson', methods=['POST'])
def get_lesson():
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        if not topic:
            return jsonify({'error': 'Sujet requis', 'success': False}), 400
        
        prompt = f"Cree une lecon complete sur: {topic}. Format: 1.EXPLICATION 2.EXEMPLES 3.EXERCICES 4.CORRIGES"
        result = call_ai([
            {'role': 'system', 'content': 'Tu es un professeur de francais.'},
            {'role': 'user', 'content': prompt}
        ])
        return jsonify({'result': result, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/conjugate', methods=['POST'])
def conjugate_verb():
    try:
        data = request.get_json()
        verb = data.get('verb', '').strip()
        if not verb:
            return jsonify({'error': 'Verbe requis', 'success': False}), 400
        
        prompt = f"Conjugue le verbe: {verb} au present, passe compose, futur simple et imparfait"
        result = call_ai([
            {'role': 'system', 'content': 'Expert en conjugaison francaise.'},
            {'role': 'user', 'content': prompt}
        ])
        return jsonify({'result': result, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/test', methods=['POST'])
def generate_test():
    try:
        data = request.get_json()
        level = data.get('level', 'intermediaire')
        prompt = f"Cree un test de 10 questions niveau {level} avec reponses"
        result = call_ai([
            {'role': 'system', 'content': 'Createur de tests.'},
            {'role': 'user', 'content': prompt}
        ])
        return jsonify({'result': result, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json()
        level = data.get('level', 'intermediaire')
        theme = data.get('theme', 'quotidien')
        prompt = f"Cree une histoire niveau {level} theme: {theme} avec vocabulaire et questions"
        result = call_ai([
            {'role': 'system', 'content': 'Createur dhistoires.'},
            {'role': 'user', 'content': prompt}
        ])
        return jsonify({'result': result, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/correct', methods=['POST'])
def correct_sentence():
    try:
        data = request.get_json()
        sentence = data.get('sentence', '').strip()
        if not sentence:
            return jsonify({'error': 'Phrase requise', 'success': False}), 400
        
        prompt = f"Corrige cette phrase et explique: {sentence}"
        result = call_ai([
            {'role': 'system', 'content': 'Correcteur francais.'},
            {'role': 'user', 'content': prompt}
        ])
        return jsonify({'result': result, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/exercise', methods=['POST'])
def generate_exercise():
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        level = data.get('level', 'intermediaire')
        if not topic:
            return jsonify({'error': 'Sujet requis', 'success': False}), 400
        
        prompt = f"Cree 5 exercices niveau {level} sur: {topic}"
        result = call_ai([
            {'role': 'system', 'content': 'Createur dexercices.'},
            {'role': 'user', 'content': prompt}
        ])
        return jsonify({'result': result, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/assistant', methods=['POST'])
def assistant():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        if not question:
            return jsonify({'error': 'Question requise', 'success': False}), 400
        
        result = call_ai([
            {'role': 'system', 'content': 'Assistant pedagogique.'},
            {'role': 'user', 'content': question}
        ])
        return jsonify({'result': result, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
