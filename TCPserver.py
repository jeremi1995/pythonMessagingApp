#############################################################################
# Program:
#    Lab PythonWebServer, Computer Networks
#    Brother Jones, CSE354
# Author:
#    Jeremy Duong
# Summary:
#    This is my implementation of the TCP server for lab02
#    Function getHTTPResponse() was created to craft 1 http response
#       to be sent back to the client by the server. Within this function,
#       the http response message is created manually without the help of
#       any outside library.
#
##############################################################################

#############################################################################
# Final project:
# This file is the source code for the server of my messaging App.
# It has 4 POST endpoints:
# - /signUp
# - /sendMessage
# - /getCorrespondents
# - /getConversation
#
##############################################################################


from socket import *
from usersDao import UsersDao
from conversationsDao import ConversationsDao
import sys
import os
import threading
import urllib.parse as urlp
import http
import json

USER_DAO = UsersDao()
CONVERSATION_DAO = ConversationsDao()
CRLF = "\n\n" #For some reason, the \r doesn't work, but the \n does...
POST_ENDPOINTS = [ "signUp", "sendMessage", "getCorrespondents", "getConversation"]
# Return proper content type
def contentType(requestType, filepath):

    if requestType == "GET":
        # Based on the file extension, return the content type
        # that is part  of the "Content-type:" header"
        extension = filepath.split(".")[1]
        if extension == "gif":
            return "image/gif"
        elif extension == "jpg":
            return "image/jpg"
        elif extension == "html":
            return "text/html"
        elif extension == "txt":
            return "text/plain"
        elif extension == "css":
            return "text/css"
        elif extension == "js":
            return "text/javascript"
        else:
            return "text/plain"
    else:
        return "text/plain"

def forbidden(filePath):
    folder = filePath.split("/")[0]
    if folder == 'database':
        return True
    return False

def getStatusString(status):
    if status == 404:
        return "Not Found"
    elif status == 403:
        return "Forbidden"
    elif status == 200:
        return "OK"

def getStatus(requestType, filePath):

    if requestType == "POST":
        print("from getStatus:", filePath)
        if filePath in POST_ENDPOINTS:
            return 200
        else:
            return 404
    else:
        #  -make sure the file exists
        #     -all files are to be relative to the directory
        #      in which the web server was started
        fileExists = os.path.exists(filePath)
        if (forbidden(filePath)):
            return 403

        #  -create the status line and put it in the response
        return 200 if fileExists else 404

def handleGETResponse(status, filePath, response, parameters):
    # If the file exist, put the file's data into the response' body:
    if status == 200:
        #     -open a file in binary like ... = open(filepath, "rb")
        data = b""
        with open(filePath, "rb") as f:
            line = f.readline()
            while (line):
                data += line
                line = f.readline()
        return response.encode() + data

    #  If the file doesn't exist, put the 404 message in the response' body
    elif status == 404:
        response += "<h1>404 - Request Not Found!<h1>"
        return response.encode()
    
    # Any other status. We won't ever go here but just in case we want
    # to add more status
    else:
        response += "Status: " + str(status)
        return response.encode()

def getParamsDict(parameters):
    paramsList = parameters.split("&")
    params = {}
    for param in paramsList:
        key = urlp.unquote(urlp.unquote_plus(param.split("=")[0]))
        value = urlp.unquote(urlp.unquote_plus(param.split("=")[1]))
        print(f"({key}: {value})")
        params[key] = value
    return params

# POST /signUp
def signUp(response, parameters):
    params = getParamsDict(parameters)
    retVal = USER_DAO.signUp(params)
    response += str(retVal)
    return response.encode()

# POST /sendMessage
def sendMessage(response, parameters):
    # 0: Message sent successfully
    # 1: A new conversation created
    # 2: Authentication failed
    params = getParamsDict(parameters)
    authCode = USER_DAO.authenticate({"username":params["sender"], "password": params["password"]})
    if (authCode == 1):
        response += str(2)
        return response.encode()
    
    receiverExists = USER_DAO.userExists({"username":params["receiver"]})
    if (receiverExists == 1):
        response += str(3)
        return response.encode()

    retVal = CONVERSATION_DAO.sendMessage(params)
    response += str(retVal)
    return response.encode()

# POST /getCorrespondents
def getCorrespondents(response, parameters):
    # 0: correspondents found and returned
    # 1: fail to authenticate
    data = {"status" : 0}
    params = getParamsDict(parameters)
    authCode = USER_DAO.authenticate({"username":params["username"], "password": params["password"]})
    if (authCode == 1):
        data["status"] = 1
        response += json.dumps(data)
        return response.encode()
    
    data["correspondents"] = CONVERSATION_DAO.getCorrespondents(params["username"])
    response += json.dumps(data)
    return response.encode()

# POST /getConversation
def getConversation(response, parameters):
    # 0: Conversation found and returned
    # 1: Conversation not found
    # 2: Failed to authenticate
    data = {"status":0}
    params = getParamsDict(parameters)
    authCode = USER_DAO.authenticate({"username":params["username"], "password": params["password"]})
    if (authCode == 1):
        data["status"] = 2
        response += json.dumps(data)
        return response.encode()

    participants = [params["username"], params["correspondent"]]
    data["messages"] = CONVERSATION_DAO.getConversation(participants)
    response += json.dumps(data)
    return response.encode()

def handlePOSTResponse(status, filePath, response, parameters):
    # execute the post action
    if (filePath == 'signUp'):
        return signUp(response, parameters)
    elif (filePath == 'sendMessage'):
        return sendMessage(response, parameters)
    elif (filePath == 'getCorrespondents'):
        return getCorrespondents(response, parameters)
    elif (filePath == 'getConversation'):
        return getConversation(response, parameters)
    
    return response.encode()

# Craft all the info from the request into ONE response to rule them all :)
def getHTTPResponse(requestType, filePath, httpVersion, parameters):

    response = ""

    # Status
    status = getStatus(requestType, filePath)
    statusString = getStatusString(status)
    response += httpVersion + " " + str(status) + " " + statusString + "\n"
    print(response)

    #  -create the "Content-type:" header and put it in the response
    response += "Content-Type: " + contentType(requestType, filePath)


    #  -What goes between the header lines and the requested file?
    response += CRLF  # this :|

    if requestType == "GET":
        return handleGETResponse(status, filePath, response, parameters)
    elif requestType == "POST":
        return handlePOSTResponse(status, filePath, response, parameters)
    

def handle_request(connectionSocket, addr):
    #  -read the request (if an empty request ignore it)
    request = connectionSocket.recv(1024).decode()
    httpMessageLines = request.split('\n')
    requestBlocks = request.split('\n\r')
    parameters = ""
    if len(requestBlocks) > 1:
        parameters = requestBlocks[1].strip()
    print("from handle request",parameters)
    # if (parameters != ''):
    #     print("Parameters:", parameters)

    #The first line of the http message is the request line, print to console
    print(httpMessageLines[0])
    
    #  -parse token from the request string, including: filePath and httpVersion
    filePath = "/"
    httpVersion = "HTTP/1.1"
    requestType = ""

    if (len(httpMessageLines) > 0 and len(httpMessageLines[0]) >= 3):
        requestType = httpMessageLines[0].split(' ')[0]
        filePath = httpMessageLines[0].split(' ')[1]
        httpVersion = httpMessageLines[0].split(' ')[2].replace('\r','')
    else:
        connectionSocket.close() # If receive an empty httpRequest, just close
        return                 #  ...and move on to the next iteration

    # When there's nothing for the request file, 
    #    how about we make home.html the home page?
    if (filePath == "/"):
        filePath = "home.html"
    
    # If there is not just a '/' but it does start with a '/', take it out.
    #    This is because open() doesn't work if there is a '/' in front
    elif (filePath[0] == '/'):
        filePath = filePath[1:]
    
    # base on the filePath, whether the file exists, and the httpVersion,
    #   craft a binary response to be sent
    response = getHTTPResponse(requestType, filePath, httpVersion, parameters)

    # Finally :( after all the hard work (T_T) I can now send the response...
    connectionSocket.send(response)

    #  -don't forget to close the connection socket
    connectionSocket.close()

# Server Connection Setup
serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("Server is running on port ", str(serverPort))
requestThreads = []

try:
    # Main Server Loop (This is the most messy server in the world, but oh well...)
    while 1:
        # Things to be done include:
        #  -accept a connection
        connectionSocket, addr = serverSocket.accept()
        thread = threading.Thread(target=handle_request, args=[connectionSocket, addr])
        requestThreads.append(thread)
        thread.start()

except KeyboardInterrupt:
    print("\nClosing Server")
    for thread in requestThreads:
        thread.join()
    serverSocket.close()
    quit()
