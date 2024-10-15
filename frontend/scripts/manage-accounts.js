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
                if (response.status == "fail") {
                    alert("Session string validation failed");
                    sessionStorage.setItem("session_string", "");
                    window.open("./index.html", "_self");
                }

                if (response.role != "admin") {
                    alert("Invalid role. Please log into an admin account to access the admin page.");
                    window.open("./index.html", "_self");
                }

                load_accounts();
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


    // account loading handling
    function load_accounts() {
        $.ajax({
            url: "http://127.0.0.1:5000/get_accounts",
            type: "GET",
            success: function(response) {
                if (response.status === "success") {
                    const accounts = response.accounts;
                    const account_body = $("#account-body");
                    account_body.empty(); // clear existing rows

                    // loop through accounts and create table rows
                    accounts.forEach(function(account) {
                        buttons = "";

                        if (account.role !== 'admin') {
                            buttons = `
                                <button class="edit-button" data-id="${account.id}">Edit</button>
                                <button class="delete-button" data-id="${account.id}">Delete</button>
                            `;
                        } else {
                            buttons = `
                                <button class="edit-button" data-id="${account.id}">Edit Password</button>
                            `;
                        }

                        const row = `
                            <tr id="account-${account.id}">
                                <td>${account.id}</td>
                                <td>${account.name}</td>
                                <td>${account.email}</td>
                                <td>${account.password}</td>
                                <td>${account.role}</td>
                                <td>${buttons}</td>
                            </tr>
                        `;
                        account_body.append(row);
                    });

                    // delete button handling
                    $(".delete-button").click(function() {
                        const account_id = $(this).data("id");
                        delete_account(account_id);
                    });

                    // edit button handling
                    $(".edit-button").click(function() {
                        const account_id = $(this).data("id");
                        edit_account(account_id);
                    });
                } else {
                    alert("Failed to fetch accounts.");
                }
            },
            error: function() {
                alert("Error fetching accounts.");
            }
        });
    }


    // account deletion handling
    function delete_account(account_id) {
        if (confirm("Are you sure you want to delete this account?")) {
            $.ajax({
                url: `http://127.0.0.1:5000/delete_account?id=${account_id}`,
                type: "DELETE",
                success: function(response) {
                    alert(response.message);
                    if (response.status == "success") {
                        $(`#account-${account_id}`).remove(); // remove row from table 
                    }
                },
                error: function() {
                    alert("Error during account deletion request.");
                }
            });
        }
    }


    function edit_account(account_id) {
        alert("Nothing for now.");
    }
});
