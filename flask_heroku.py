# coding=utf-8
import flask
import json
from funciones import send_message, random, issues_without_answer
import os
import threading
import time
from dotenv import load_dotenv
from pathlib import Path  # python3 only

app = flask.Flask(__name__)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

MY_USER = os.environ['TELEGRAM_USER']

organization = os.environ['ORGANIZATION']
repo = os.environ['REPO']

LINK = "https://api.github.com/repos/{}/{}/issues".format(organization, repo)

template_1 = "*Nueva Issue\n\nTítulo:* {}\n*Texto:*\n\t{}\n\nVer en este [link]({})"
template_2 = "*Nuevo Comentario\n\nTítulo:* {}\n*Texto:*\n\t{}\n\nVer en este [link]({})"
template_3 = "*Nueva Issue\n\nTítulo:* {}\n*Texto:*\n\tNo es posible mostrar el text\n\nVer en este [link]({})"
template_4 = "*Nuevo Comentario\n\nTítulo:* {}\n*Texto:*\n\tNo es posible mostrar el text\n\nVer en este [link]({})"

teacher_assistant = [
    x.strip("\n").lower() for x in open("teacher_assistant.txt")
]
print(teacher_assistant)

# Id chat donde se mandará los mensajes de issues
ID_COURSE = os.environ['ID_COURSE']

# Id personal
ID_PERSONAL = os.environ['ID_PERSONAL']


@app.route('/TOKEN', methods=["POST", "GET"])
def telegram_bot():
    try:
        data = json.loads(flask.request.data)
        print(data)
        if "message" in data and str(data["message"]["text"]).lower().strip() == "/start":
            id_ = str(data["message"]["chat"]["id"])
            send_message("Hola, nuestro ID de chat es {}".format(id_), ID_PERSONAL)
            return "202"

        if 'new_chat_members' in data['message'] and 'new_chat_member' in data[
                'message'] and 'new_chat_participant' in data['message']:
            if data['message']['new_chat_member']['username'] != 'Hernybot':
                return "202"
            id_ = str(data["message"]["chat"]["id"])
            chat = str(data['message']['chat']['title'])
            send_message(
                "HernyBot ha sido incluido al grupo {} con id {}".format(
                    chat, id_), ID_PERSONAL)
            return "202"

        if "edited_message" not in data:

            text = str(data["message"]["text"])
            user = data["message"]["from"]["username"]
            id_ = str(data["message"]["chat"]["id"])

            if text.lower().startswith("/"):

                if text.lower().startswith("/random "):
                    random(text, id_)

                elif text.lower().startswith("/github"):
                    if user != MY_USER and id_ not in  [ID_PERSONAL, ID_COURSE]:
                        text = f"Hola {user}. Lamento informar que no tienes autorización para ejecutar este comando"
                        send_message(text, id_)
                        return "202"

                    def vew_detail_github(teacher_assistant):
                        counter, without_answer, without_answer_array, isses_array = issues_without_answer(
                            teacher_assistant)

                        text = f"Hay {counter} issues abiertas cuya última respuesta es de un alumno\n"
                        for number in isses_array:
                            text += "\t - Issue [{}]({}/{})\n".format(
                                number, LINK, number)

                        text += f"\nHay {without_answer} issues abiertas sin ningún comentario\n"
                        for number in without_answer_array:
                            text += "\t - Issue [{}]({}/{})\n".format(
                                number, LINK, number)

                        print(text)
                        send_message(text, id_, True)

                    thread = threading.Thread(target=vew_detail_github,
                                              args=(teacher_assistant, ),
                                              daemon=True)
                    thread.start()

        return "202"

    except Exception as e:
        text = str(e) + " " + str(e.args) + " " + str(type(e))
        text += "\n" + str(json.loads(flask.request.data))
        print(text)
        return "403"


@app.route('/course', methods=["POST", "GET"])
def github_bot_avanzada():
    try:
        data = flask.request.get_json()
        if "zen" in data:
            send_message("HernyBot ha sido incluido a un webhook de Github", ID_PERSONAL)
            return "202"

        type_event = data["action"]
        print(type_event)

        if type_event == "opened":  # Abrir issue
            autor = data["issue"]["user"]["login"].lower()
            if autor not in teacher_assistant:
                title = data["issue"]["title"]
                text = data["issue"]["body"]
                link = data["issue"]["html_url"]

                text = template_1.format(title, text, link)
                result = send_message(text, ID_COURSE, True)
                if result == 400:
                    text = template_3.format(title, link)
                    result = send_message(text, ID_COURSE, True)

        elif type_event == "created":  # Comentar issue
            autor = data["comment"]["user"]["login"].lower()
            if autor not in teacher_assistant:
                title = data["issue"]["title"]
                text = data["comment"]["body"]
                link = data["issue"]["html_url"]

                text = template_2.format(title, text, link)
                result = send_message(text, ID_COURSE, True)
                if result == 400:
                    text = template_4.format(title, link)
                    result = send_message(text, ID_COURSE, True)

        return "202"

    except Exception as e:
        text = str(e) + " " + str(e.args) + " " + str(type(e))
        send_message(text, ID_PERSONAL)
        return "403"


if __name__ == '__main__':
    app.run()
