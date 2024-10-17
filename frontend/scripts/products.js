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

                load_products();
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


    // product loading handling
    function load_products() {
        $.ajax({
            url: "http://127.0.0.1:5000/get_products",
            type: "GET",
            success: function(response) {
                if (response.status === "success") {
                    const products = response.products;
                    const product_body = $("#product-body");
                    product_body.empty(); // clear existing rows

                    // loop through products and create table rows
                    products.forEach(function(product) {
                        const row = `
                            <tr id="product-${product.id}">
                                <td>${product.id}</td>
                                <td>${product.name}</td>
                                <td>${product.price}</td>
                                <td>${product.amount}</td>
                                <td>${product.description}</td>
                                <td>
                                    <button class="add-to-cart-button" data-id="${product.id}">Add to cart</button>
                                </td>
                            </tr>
                        `;
                        product_body.append(row);
                    });

                    // add to cart button handling
                    $(".add-to-cart-button").click(function() {
                        alert("Added product to cart.");
                        const product_id = $(this).data("id");
                        add_product_to_cart(product_id);
                    });
                } else {
                    alert("Failed to fetch products.");
                }
            },
            error: function() {
                alert("Error fetching products.");
            }
        });
    }
});
