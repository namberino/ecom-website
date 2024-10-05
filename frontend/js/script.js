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
            alert("Login successful!");
            // send login data to backend here
        } else {
            alert("Please fill in both fields.");
        }
    });

    // register button handling
    $("#register-btn").click(function() {
        let name = $("#register-name").val();
        let email = $("#register-email").val();
        let password = $("#register-password").val();

        if(name && email && password) {
            alert("Registration successful!");
            // send registration data to backend here
        } else {
            alert("Please fill in all fields.");
        }
    });
});
