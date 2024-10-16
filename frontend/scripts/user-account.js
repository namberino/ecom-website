$(document).ready(function() {
    // logout handling
    $("#logout-button").click(function() {
        if (confirm("Are you sure you want to logout?")) {
            sessionStorage.setItem("session_string", "");
            window.open("./index.html", "_self");
        }
    });


    // session string validation request
    let session_string = sessionStorage.getItem("session_string");
    if (session_string != null && session_string != "") {
        $.ajax({
            url: "http://127.0.0.1:5000/validate_session",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ session_string: session_string }),
            success: function(response) {
                // alert(response.message);
                if (response.status == "fail") {
                    alert("Session string validation failed");
                    sessionStorage.setItem("session_string", "");
                    window.open("./index.html", "_self");
                }

                display_user_info();
            },
            error: function() {
                alert("Error during session string validation.");
                sessionStorage.setItem("session_string", "");
                window.open("./index.html", "_self");
            }
        });
    } else {
        alert("Must be logged in to access page.");
        window.open("./index.html", "_self");
    }


    // get and display user information
    function display_user_info() {
        $.ajax({
            url: "http://127.0.0.1:5000/get_info_from_session",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ session_string: session_string }),
            success: function(response) {
                if (response.status == "success") {
                    let account = response.account;
                    $("#name-input").val(account.name);
                    $("#email-input").val(account.email);
                }
            },
            error: function() {
                alert("Error during get info from session string request.")
            }
        });
    }
});
