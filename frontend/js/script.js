$(document).ready(function() {
    // register form toggle
    $("#show-register").click(function() {
        $("#login-form").hide();
        $("#register-form").show();
    });

    // login form toggle
    $("#show-login").click(function() {
        $("#register-form").hide();
        $("#login-form").show();
    });

    // login button handling
    $("#login-btn").click(function() {
        let email = $("#login-email").val();
        let password = $("#login-password").val();
        if(email && password) {
            $.ajax({
                url: "http://127.0.0.1:5000/login",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ email: email, password: password }),
                success: function(response) {
                    alert(response.message);
                },
                error: function() {
                    alert("Error during login request.");
                }
            });
        } else {
            alert("Missing data. Please fill in all fields.");
        }
    });

    // register button handling
    $("#register-btn").click(function() {
        let name = $("#register-name").val();
        let email = $("#register-email").val();
        let password = $("#register-password").val();

        if(name && email && password) {
            $.ajax({
                url: "http://127.0.0.1:5000/register",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ name: name, email: email, password: password }),
                success: function(response) {
                    alert(response.message);
                    alert("Please login to your new account.")
                },
                error: function() {
                    alert("Error during registration request.");
                }
            });
        } else {
            alert("Missing data. Please fill in all fields.");
        }
    });
});
