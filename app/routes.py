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
                "quick_replies": object_message['quick_replies'],
                #"attachments":[
                #    {
                #      "type":"fallback",
                #      "payload":"null",
                #    	"title":"google",
                #    	"URL":"www.google.com",
                #    }
                #    ]
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
            "texto" : "¿Cómo puedo ayudarte? \n\n1) Facial \n2) Manicure \n3) Pedicure \n4) Capilar \n5) Corporal",
            "opcion" : [{
                "title" : 'OPC 1',
                "payload" : "OPC1"
            }, {
                "title" : 'OPC 2',
                "payload" : "OPC2"
            },{
                "title" : 'OPC 3',
                "payload" : "OPC3"
            },{
                "title" : "OPC 4",
                "payload" : "OPC4"
            },{
                "title" : 'OPC 5',
                "payload" : "OPC5"
            }]
        },
        "HOLA" : {
            "texto" : "¿Cómo puedo ayudarte? \n\n1) Facial \n2) Manicure \n3) Pedicure \n4) Capilar \n5) Corporal",
            "opcion" : [{
                "title" : 'OPC 1',
                "payload" : "OPC1"
            }, {
                "title" : 'OPC 2',
                "payload" : "OPC2"
            },{
                "title" : 'OPC 3',
                "payload" : "OPC3"
            },{
                "title" : "OPC 4",
                "payload" : "OPC4"
            },{
                "title" : 'OPC 5',
                "payload" : "OPC5"
            }]
        },
        'Quiero chatear con alguien.' : {
            "texto" : "¿Cómo puedo ayudarte? \n\n1) Facial \n2) Manicure \n3) Pedicure \n4) Capilar \n5) Corporal",
            "opcion" : [{
                "title" : 'OPC 1',
                "payload" : "OPC1"
            }, {
                "title" : 'OPC 2',
                "payload" : "OPC2"
            },{
                "title" : 'OPC 3',
                "payload" : "OPC3"
            },{
                "title" : "OPC 4",
                "payload" : "OPC4"
            },{
                "title" : 'OPC 5',
                "payload" : "OPC5"
            }]            
        },
        'Quiero más información sobre el negocio.' : {
            "texto" : "¿Cómo puedo ayudarte? \n\n1) Facial \n2) Manicure \n3) Pedicure \n4) Capilar \n5) Corporal",
            "opcion" : [{
                "title" : 'OPC 1',
                "payload" : "OPC1"
            }, {
                "title" : 'OPC 2',
                "payload" : "OPC2"
            },{
                "title" : 'OPC 3',
                "payload" : "OPC3"
            },{
                "title" : "OPC 4",
                "payload" : "OPC4"
            },{
                "title" : 'OPC 5',
                "payload" : "OPC5"
            }]            
        },
        'Quiero más información sobre ti.' : {
        "texto" : "¿Cómo puedo ayudarte? \n\n1) Facial \n2) Manicure \n3) Pedicure \n4) Capilar \n5) Corporal",
            "opcion" : [{
                "title" : 'OPC 1',
                "payload" : "OPC1"
            }, {
                "title" : 'OPC 2',
                "payload" : "OPC2"
            },{
                "title" : 'OPC 3',
                "payload" : "OPC3"
            },{
                "title" : "OPC 4",
                "payload" : "OPC4"
            },{
                "title" : 'OPC 5',
                "payload" : "OPC5"
            }]            
        },
        "OPC 1" : {
                "texto" : "Facial : ¿Que desea realizar? \n\n1.1) Productos \n1.2) Tratamientos \n1.3) Asesoria",
                "opcion" : [{
                    "title" : 'OPC 1.1',
                    "payload" : "OPC11"
                },{
                    "title" : 'OPC 1.2',
                    "payload" : "OPC12"
                },{
                    "title" : 'OPC 1.3',
                    "payload" : "OPC11"
                }]
        },
        "OPC 2" : {
                "texto" : "Manicure : ¿Que desea realizar? \n\n2.1) Productos \n2.2) Tratamientos \n2.3) Asesoria",
                "opcion" : [{
                    "title" : 'OPC 2.1',
                    "payload" : "OPC11"
                },{
                    "title" : 'OPC 2.2',
                    "payload" : "OPC12"
                },{
                    "title" : 'OPC 2.3',
                    "payload" : "OPC11"
                }]
        },
        "OPC 3" : {
                "texto" : "Pedicure : ¿Que desea realizar? \n\n3.1) Productos \n3.2) Tratamientos \n3.3) Asesoria",
                "opcion" : [{
                    "title" : 'OPC 3.1',
                    "payload" : "OPC11"
                },{
                    "title" : 'OPC 3.2',
                    "payload" : "OPC12"
                },{
                    "title" : 'OPC 3.3',
                    "payload" : "OPC11"
                }]
        },
        "OPC 4" : {
                "texto" : "Capilar : ¿Que desea realizar? \n\n4.1) Productos \n4.2) Tratamientos \n4.3) Asesoria",
                "opcion" : [{
                    "title" : 'OPC 4.1',
                    "payload" : "OPC11"
                },{
                    "title" : 'OPC 4.2',
                    "payload" : "OPC12"
                },{
                    "title" : 'OPC 4.3',
                    "payload" : "OPC11"
                }]
        },
        "OPC 5" : {
                "texto" : "Corporal : ¿Que desea realizar? \n\n5.1) Productos \n5.2) Tratamientos \n5.3) Asesoria",
                "opcion" : [{
                    "title" : 'OPC 5.1',
                    "payload" : "OPC11"
                },{
                    "title" : 'OPC 5.2',
                    "payload" : "OPC12"
                },{
                    "title" : 'OPC 5.3',
                    "payload" : "OPC11"
                }]
        }
    }
    return ddic_response