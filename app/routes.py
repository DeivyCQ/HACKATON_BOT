from app import app
from flask import request
from random import choice
from requests import get, post
from json import dumps
import os

@app.route('/')
@app.route('/index')
def index():
    return 'Hola'

@app.route('/webhook', methods=['GET'])
def webhook():
    if request.args.get('hub.verify_token') == os.getenv('VERIFY_TOKEN'):
        return request.args.get('hub.challenge')
    else:
        return 'Token invalido'

@app.route('/webhook', methods=['POST'])
def webhook_handle_message():
    data = request.get_json()
    for event in data['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    # response_sent_text = messages_random(message['message'].get('text'))
                    response = messages_random(message['message'].get('text'))
                    response_sent_text = response["message"]
                    quick_replies = response["quick_replies"]
                    sender_graph({
                        "sender_id": recipient_id,
                        "message": response_sent_text,
                        "quick_replies": quick_replies
                    })
    return 'ok'

def sender_graph(object_message):
    response = post("https://graph.facebook.com/v8.0/me/messages", 
        params = {
            "access_token": os.getenv('PAGE_ACCESS_TOKEN')
        },
        headers = {
            "Content-Type": "application/json"
        },
        data = dumps({
            "messaging_type": "RESPONSE",
            "recipient": {
                "id": object_message['sender_id']
            },
            "message": {
                "text": object_message['message'], #"¿Como podemos ayudarte?"
                "quick_replies": object_message['quick_replies']
                #"quick_replies": [
                #    {
                #        "content_type":"text",
                #        "title":"Red",
                #        "payload":"1",
                #        "image_url":"https://upload.wikimedia.org/wikipedia/commons/b/b9/Solid_red.png"
                #    },{
                #        "content_type":"text",
                #        "title":"Green",
                #        "payload":"2",
                #        "image_url":"https://upload.wikimedia.org/wikipedia/commons/f/f3/Green.PNG"
                #    }
                #]
            }
        })
    )
    

def messages_random(text = ''):
    # list_messages = ['Hola... ¿En que le podemos ayudar?']
    # return choice(list_messages)
    
    estructura_respuesta = response_structure()
    respuesta = estructura_respuesta[text]
    #{'texto': '¿Cómo puedo ayudarte?', 'opcion': [{'title': 'Facial', 'payload': 'OPC1'}, {'texto': 'Manicure', 'payload': 'OPC2'}, {'texto': 'Pedicure', 'payload': 'OPC3'}, {'texto': 'Capilar', 'payload': 'OPC4'}, {'texto': 'Corporal', 'payload': 'OPC5'}]}
    quick_replies = options(respuesta["opcion"])
    return {
        "message": respuesta["texto"],
        "quick_replies": quick_replies
    }

def options(lista = []):

    list_quick_replies = []

    for response in lista:
        quick_replies = {
            "content_type" : "text",
            'title' : response['title'],
            "payload" : response["payload"],
            "image_url" : ""
        }
        list_quick_replies.append(quick_replies)

    return list_quick_replies


def response_structure():

    ddic_response = {
        "hola" : {
            "texto" : "¿Cómo puedo ayudarte?",
            "opcion" : [{
                "title" : '\nFacial',
                "payload" : "OPC1"
            }, {
                "title" : '\nManicure',
                "payload" : "OPC2"
            },{
                "title" : '\nPedicure',
                "payload" : "OPC3"
            },{
                "title" : "Capilar",
                "payload" : "OPC4"
            },{
                "title" : 'Corporal',
                "payload" : "OPC5"
            }]
        },
        'Quiero chatear con alguien.' : {
            "texto" : "¿Cómo puedo ayudarte?",
            "opcion" : [{
                "title" : 'Facial',
                "payload" : "OPC1"
            }, {
                "title" : 'Manicure',
                "payload" : "OPC2"
            },{
                "title" : 'Pedicure',
                "payload" : "OPC3"
            },{
                "title" : "Capilar",
                "payload" : "OPC4"
            },{
                "title" : 'Corporal',
                "payload" : "OPC5"
            }]            
        },
        "Facial" : {
                "texto" : "Facial",
                "opcion" : [{
                    "title" : 'Comprar productos',
                    "payload" : "OPC11"
                },{
                    "title" : 'Consultar tratamientos',
                    "payload" : "OPC12"
                },{
                    "title" : 'Contactar con un asesor',
                    "payload" : "OPC11"
                }]
        },
        'Contactar con un ase...' : {
            "texto" : "¿Cómo puedo ayudarte?",
            "opcion" : [{
                "title" : 'Facial',
                "payload" : "OPC1"
            }, {
                "title" : 'Manicure',
                "payload" : "OPC2"
            },{
                "title" : 'Pedicure',
                "payload" : "OPC3"
            },{
                "title" : "Capilar",
                "payload" : "OPC4"
            },{
                "title" : 'Corporal',
                "payload" : "OPC5"
            }]            
        }
    }
    return ddic_response