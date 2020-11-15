import json

class Question:
    # prompt: text of question asked
    # response: type of response.
    # first char = type
    # i = int, s = string

    def __init__(self, prompt, response):
        self.prompt = prompt
        self.response = response

def load_questions(jsonString):
    ret = []
    questions = json.loads(jsonString).get("questions")

    for q in questions:
        p = q['prompt']
        r = q['response']
        ret.append(Question(prompt=p, response=r))

    return ret

# def load_questions_container(jsonString):
#     q = load_questions(jsonString)

class UserInfo:

    def __init__(self):
        pass