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

function passwordMatches(password, confirmedPassword) {
    return password.localeCompare(confirmedPassword) == 0
}

function handleServerResponse(responseCode) {
    if (responseCode == 0) {
        displayMessage("Sign-up successful! You can now send messages by navigating to the Send Message tab", "success")
    }
    else if (responseCode == 1) {
        displayMessage("Username has already been used! Please try a differen username!", "danger")
    }
    else {
        displayMessage("Something bad happened!", "danger")
    }
}

function sendSignUpRequest(username, password) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            handleServerResponse(Number(this.responseText))
        }
    };

    paramString = encodeURI("username=" + username + "&"
                        + "password=" + password);
    
    console.log(paramString)

    xhttp.open("POST", "/signUp");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(paramString)
}

function signUp() {

    username = document.getElementById("username").value
    password = document.getElementById("password").value
    confirmedPassword = document.getElementById("confirm_password").value
    if (passwordMatches(password, confirmedPassword)) {
        sendSignUpRequest(username, password)
    }
    else {
        displayMessage("Password and confirmed password don't match! Please try again", "danger")
    }
    return false
}

document.getElementById("signUpButton").addEventListener("click", signUp)