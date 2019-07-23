import numpy as np
from crypto import generate_answerid
from datetime import datetime


def _print(*args):
    # double, make common module
    time = datetime.now().time().isoformat()[:8]
    print (time)
    print ("".join(map(str, args)))

def answerQuestion(message, nodeid, factory):

    answers = {}
    question = np.asarray(message["question"]).reshape(1, -1)
    answer = factory.ml.classify(question)
    guess = str(answer[0][0])
    certainty = answer[1][0]
    answerID = generate_answerid()

    _print( " [ ] Response to " ,  message["questionID"], " is ", answer)

    if message["answer"]: # If the message has other answers already
        answers = message["answer"]
        if guess in answers:
            answers[guess].append([certainty, answerID])
        else:
            answers[guess] = ([[certainty, answerID]])
    else:
        answers[guess] = ([[certainty, answerID]])

    if message["IDS"]: # If the message has IDS of nodes that have responded, add own ID to it
        IDS = message["IDS"]
        IDS.append(nodeid)

    else:
        IDS = [nodeid]

    factory.answeredQuestions.append(message["questionID"]) # Update the facotry
    factory.questions[message["questionID"]] = (message["questionID"], message["question"], answers, IDS)

def answeredQuestion(message, sentResponse, factory):

    answers = factory.questions[message["questionID"]][2]
    IDS = factory.questions[message["questionID"]][3]

    answersRecieved = message["answer"]

    for key, value in answers.items(): # Adding new ansers of keys taht excist
        if key in answersRecieved:
            for valueR in answersRecieved[key]:
                if valueR in value: # If the value is already in it, go to next one
                    continue
                else:
                    answers[key].append(valueR)

    for key, value in answersRecieved.items(): # Adding new keys to answers
        if key not in answers:
            answers[key] = value

    for ID in message["IDS"]: # Adding IDS
        if ID not in IDS:
            IDS.append(ID)

    factory.questions[message["questionID"]] = (message["questionID"], message["question"], answers, IDS)
    if message["questionID"] in sentResponse:
        sentResponse.remove(message["questionID"])

def addPeerState(self):

    def add_peer(self, kind):
        entry = (self.remote_ip, kind)
        self.factory.peers[self.remote_nodeid] = entry

    if self.remote_type == "NODE":
        if self.state == "HELLO" :
            add_peer(self, "SPEAKER")
        elif self.state == "SENTHELLO":
            add_peer(self, "LISTENER")
    else:
        add_peer(self, "CO")
