import yaml
import json

class ConversationsDao:
    def __init__(self):
        self.write_lock = False

    def acquire_lock(self):
        while self.write_lock:
            continue
        self.write_lock = True
    
    def release_lock(self):
        # Release the write lock
        self.write_lock = False

    def rewriteFile(self, fileObject):
        # Open and write to file
        with open("database/conversations.yaml", "w") as rC:
            rC.write(yaml.dump(fileObject))

    def conversationExists(self, participants):
        # return conversationId: conversation exists
        # return -1: conversation doesn't exist
        with open("database/conversations.yaml", "r") as rC:
            convDO = yaml.load(rC.read())
            
            for conversation in convDO["conversations"]:
                numIn = 0
                for participant in participants:
                    if participant in conversation["participants"]:
                        numIn += 1
                if numIn == len(participants):
                    return conversation["conversationId"]
        return -1
    
    def addConversation(self, participants, messages):
        convDO = {}

        self.acquire_lock()
        
        with open("database/conversations.yaml", "r") as rC:
            convDO = yaml.load(rC.read())
        
        conversation = {}
        conversation["conversationId"] = convDO["nextId"]
        conversation["participants"] = participants
        conversation["messages"] = messages
        
        convDO["conversations"].append(conversation)
        convDO["nextId"] = convDO["nextId"] + 1
        self.rewriteFile(convDO)
        
        self.release_lock()

    def addMessageToConversation(self, conversationId, message):
        # Write to the object
        convDO = {}

        self.acquire_lock()

        with open("database/conversations.yaml", "r") as rC:
            convDO = yaml.load(rC.read())
            for conversation in convDO["conversations"]:
                if conversationId == conversation["conversationId"]:
                    conversation["messages"].append(message)
                    break
        # Write the object to the file
        self.rewriteFile(convDO)

        self.release_lock()

    def sendMessage(self, params):
        # 0: conversation found, add message to conversation
        # 1: new conversation created
        
        participants = [params["sender"], params["receiver"]]
        message = {"by": params["sender"], "content": params["content"]}

        conversationId = self.conversationExists(participants)

        # If conversation exists, write to existing conversation
        if (conversationId != -1):
            self.addMessageToConversation(conversationId, message)
            return 0
        
        # If conversation doesn't exist
        else: 
            self.addConversation(participants, [message])
            return 1

    def getCorrespondents(self, username):
        # Expect: username
        correspondents = []
        with open("database/conversations.yaml", "r") as rC:
            convDO = yaml.load(rC.read())
            for conversation in convDO["conversations"]:
                if username in conversation["participants"]:
                    convCorrespondent = conversation["participants"]
                    convCorrespondent.remove(username)
                    correspondents += convCorrespondent
        return correspondents
    
    def getMessages(self, conversationId):
        with open("database/conversations.yaml", "r") as rC:
            convDO = yaml.load(rC.read())
            for conversation in convDO["conversations"]:
                if conversation["conversationId"] == conversationId:
                    return conversation["messages"]

    def getConversation(self, participants):
        conversationId = self.conversationExists(participants)
        return self.getMessages(conversationId)
        
# convDao = ConversationsDao()
# print(convDao.getCorrespondents("jeremi1995"))