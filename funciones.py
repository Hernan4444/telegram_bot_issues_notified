import requests
import os
from random import choice
from requests import Session
from dotenv import load_dotenv
from pathlib import Path  # python3 only

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Token del bot cuando se crea
TOKEN = os.environ['TOKEN']

session = Session()
# Usuario y contraseña de github
session.auth = (os.environ['USER'], os.environ['PASSWORD'])

organization = os.environ['organization']
repo = os.environ['repo']

LINK = "https://api.github.com/repos/{}/{}/issues".format(organization, repo)


def send_message(text, id_, markdown=False):
    print(text)
    url = "https://api.telegram.org/bot{}/".format(TOKEN)
    params = {"method": "sendMessage", "text": text, "chat_id": id_}

    if markdown:
        params["parse_mode"] = "Markdown"
        params["disable_web_page_preview"] = "True"
    result = requests.get(url, params=(params))
    return result.status_code


def random(text, id_):
    argument = text[8:].strip("[").strip("]")
    random_elements = argument.split(",")

    text = "De la lista [{}]." \
        " Escogere a \n --> {}".format(','.join(random_elements),
                                       choice(random_elements))

    send_message(text, id_)


def issues_without_answer(autores):
    issues = session.get(LINK)
    issues_array = issues.json()

    while (issues and issues.links and 'next' in issues.links):
        issues = session.get(issues.links['next']['url'])
        issues_array.extend(issues.json())

    counter = 0
    counter_array = []
    without_answer_array = []
    without_answer_counter = 0
    for index, issue in enumerate(issues_array):
        print(index, len(issues_array))
        number = issue["number"]

        # GET /repos/:owner/:repo/issues/:number/labels
        link_labels = f"{LINK}/{number}/labels"
        labels = session.get(link_labels)
        print(link_labels)

        done_issue = False
        for label in labels.json():
            if label["name"].lower() == "resuelto":
                done_issue = True

        if done_issue:
            continue

        link = f"{LINK}/{number}/comments"
        print(link)

        comments = session.get(link)
        if comments:
            comments = comments.json()

            if len(comments) == 0:
                if issue["user"]["login"].lower() not in autores:
                    without_answer_counter += 1
                    without_answer_array.append(number)

            elif comments[-1]["user"]["login"].lower() not in autores:
                counter_array.append(number)
                counter += 1

    return counter, without_answer_counter, without_answer_array, counter_array


if __name__ == "__main__":
    import time

    counter_comment = {
        x.strip("\n").lower(): 0
        for x in open("teacher_assistant.txt")
    }
    counter_issues = {
        x.strip("\n").lower(): 0
        for x in open("teacher_assistant.txt")
    }

    for number in range(1, 677):
        print(number)
        time.sleep(0.1)
        link = f"{LINK}/{number}/comments"
        comments = session.get(link)
        work_this_issue = {
            x.strip("\n").lower(): False
            for x in open("teacher_assistant.txt")
        }

        if comments:
            comments = comments.json()
            for comment in comments:
                author = comment["user"]["login"].lower()
                if author in counter_comment:
                    counter_comment[author] += 1
                if author in work_this_issue and not work_this_issue[author]:
                    work_this_issue[author] = True
                    counter_issues[author] += 1

    print("Ayudante - Issues participadas - Comentarios realizados")
    for i in counter_comment:
        print("{:15s} - {} - {}".format(i, counter_issues[i],
                                        counter_comment[i]))
