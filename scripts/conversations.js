var auth = {};
var correspondents;

function createOptions(correspondents) {
    dropDownElement = document.getElementById("friendsDropdown")
    dropDownElement.removeAttribute("disabled")
    for (correspondent of correspondents) {
        optionElement = document.createElement("option")
        optionElement.innerHTML = correspondent
        optionElement.value = correspondent

        dropDownElement.appendChild(optionElement)
    }
}

function displayMessage(message, mode) {
    if (mode == "danger") {
        document.getElementById("serverResponse").className = "alert alert-danger"
    }
    else if (mode =="success") {
        document.getElementById("serverResponse").className = "alert alert-success"
    }
    else if (mode == "clear") {
        document.getElementById("serverResponse").className = ""
    }
    else {
        document.getElementById("serverResponse").className = "alert alert-primary"
    }
    document.getElementById("serverResponse").innerHTML = message
}

function displayConversation(messages) {
    conversationDiv = document.getElementById("conversation")
    conversationDiv.innerHTML = ""
    for (message of messages) {
        messageElement = document.createElement("div")
        htmlStr = "<span class='by'>" + message.by + "</span><br>" + "<span class='content'>" + message.content + "</span>"
        messageElement.innerHTML = htmlStr
        if (message.by == auth.username) {
            messageElement.className = "message alert alert-primary"
        }
        else {
            messageElement.className = "message alert alert-secondary"
        }

        conversationDiv.appendChild(messageElement)

    }
}

function getCorrespondents() {
    
    username = document.getElementById("username").value
    password = document.getElementById("password").value
    auth.username = username
    auth.password = password

    // disable input:

    document.getElementById("username").disabled = true
    document.getElementById("password").disabled = true
    document.getElementById("getCorrespondents").disabled = true

    //Send request:
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            jsonResponse = JSON.parse(this.responseText)
            if (jsonResponse.status == 1) {
                displayMessage("Username of password is incorrect!", "danger")
            }
            else {
                displayMessage("", "clear")
                createOptions(jsonResponse.correspondents)
                getConversation()
            }
        }
    };

    paramString = encodeURI("username=" + username + "&"
                        + "password=" + password);

    console.log(paramString)
    
    xhttp.open("POST", "/getCorrespondents"); 
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(paramString)
}

function getConversation() {
    username = auth.username
    password = auth.password
    correspondent = document.getElementById("friendsDropdown").value
    
    //Send request:
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            jsonResponse = JSON.parse(this.responseText)
            if (jsonResponse.status == 2) {
                displayMessage("Failed to authenticate! Please refresh the page and try again", "danger")
            }
            else if (jsonResponse.status == 1) {
                displayMessage("Conversation not found!", "danger")
            }
            else {
                displayMessage("", "clear")
                displayConversation(jsonResponse.messages)
            }
        }
    };

    paramString = encodeURI("username=" + username + "&"
                        + "password=" + password + "&"
                        + "correspondent=" + correspondent);

    console.log(paramString)
    
    xhttp.open("POST", "/getConversation"); 
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(paramString)
}

document.getElementById("getCorrespondents").addEventListener("click", getCorrespondents)
document.getElementById("friendsDropdown").addEventListener("change", getConversation)
