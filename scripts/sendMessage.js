function displayMessage(code) {
    responseElement = document.getElementById("serverResponse")
    if (code == 0) {
        responseElement.innerHTML = "Message Sent Successfully! Check out your conversations!"
        responseElement.className = "alert alert-success"
    }
    else if (code == 1) {
        responseElement.innerHTML = "Message Sent Successfully! New conversation created!"
        responseElement.className = "alert alert-success"
    }
    else if (code == 2) {
        responseElement.innerHTML = "Incorrect username or password!"
        responseElement.className = "alert alert-danger"
    }
    else if (code == 3) {
        responseElement.innerHTML = "Receiver doesn't exist!"
        responseElement.className = "alert alert-danger"
    }

}

function sendMessage() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            displayMessage(Number(this.responseText))
        }
    };
    sender = document.getElementById("username").value
    password = document.getElementById("password").value
    receiver = document.getElementById("receiver").value
    content = document.getElementById("content").value

    paramString = encodeURI("sender=" + sender + "&"
                        + "password=" + password + "&"
                        + "receiver=" + receiver + "&"
                        + "content=" + content);
    
    console.log(paramString)

    xhttp.open("POST", "/sendMessage");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(paramString)
}

document.getElementById("sendButton").addEventListener("click", sendMessage)

