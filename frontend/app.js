// ========================================
// LOGIN
// ========================================

const loginForm = document.querySelector("#login-form");

if (loginForm) {

    const loginError =
        document.querySelector("#login-error");

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const username =
                document.querySelector("#username").value;

            const email =
                document.querySelector("#email").value;

            const password =
                document.querySelector("#password").value;

            try {

                const response = await fetch(
                    "/users/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            username: username,
                            email: email,
                            password: password
                        })
                    }
                );

                const data =
                    await response.json();

                if (response.status === 201) {

                    sessionStorage.setItem(
                        "userId",
                        data.id
                    );

                    sessionStorage.setItem(
                        "username",
                        data.username
                    );

                    window.location.href =
                        "/frontend/products.html";

                } else {

                    loginError.textContent =
                        data.detail || "Login failed";
                }

            } catch (error) {

                console.error(error);

                loginError.textContent =
                    "Unable to connect to the server.";
            }
        }
    );
}


// ========================================
// CART
// ========================================

function addToCart(id, name, price) {

    let cart = JSON.parse(
        sessionStorage.getItem("cart") || "[]"
    );

    const existingProduct = cart.find(
        product => product.id === id
    );

    if (existingProduct) {

        existingProduct.quantity += 1;

    } else {

        cart.push({
            id: id,
            name: name,
            price: price,
            quantity: 1
        });
    }

    sessionStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );
}


// ========================================
// OPEN CART
// ========================================

function openCart() {

    window.location.href =
        "/frontend/cart.html";
}


const cartButton = document.querySelector(
    '[data-testid="cart-button"]'
);

if (cartButton) {

    cartButton.addEventListener(
        "click",
        openCart
    );
}