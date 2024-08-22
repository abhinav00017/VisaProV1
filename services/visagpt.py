import os

from flask import jsonify, session
from utils.backendopenai import BackendOpenAI

from dotenv import load_dotenv
load_dotenv()

BackendOpenAI = BackendOpenAI(os.getenv('OPENAI_API_KEY'))

class Visagpt:

    def load_chat(thread_id):
        # thread_id = request.json.get('threadId')
        thread = BackendOpenAI.get_thread_data(thread_id)
        print(thread)
        messages = []
        for message in thread['data']:
            messages.append({
                'id': message['id'],
                'sender': message['role'],
                'content': message['content'][0]['text']['value']
            })
        messages = messages[::-1]
        history = {
            'id': thread_id,
            'title': thread_id,
            'messages': messages
        }
        
        session["threads"].append(history)
        print(session["threads"])
        return jsonify(session["threads"])