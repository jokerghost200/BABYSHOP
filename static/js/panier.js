document.addEventListener("DOMContentLoaded", () => {
    const addToCartButtons = document.querySelectorAll(".btn.btn-primary");
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    addToCartButtons.forEach(button => {
        button.addEventListener("click", () => {
            const card = button.closest(".product-card");
            const name = card.querySelector(".card-title").textContent;
            const image = card.querySelector("img").src;
            const price = 5000; // Tu peux remplacer par une vraie valeur dynamique

            // Vérifie si le produit existe déjà
            const existing = cart.find(item => item.name === name);
            if (existing) {
                existing.quantity++;
            } else {
                cart.push({ name, image, price, quantity: 1 });
            }

            localStorage.setItem("cart", JSON.stringify(cart));

            // Mise à jour du badge panier
            const cartCount = document.getElementById("cart-count");
            if (cartCount) {
                cartCount.textContent = cart.reduce((acc, i) => acc + i.quantity, 0);
                cartCount.classList.add("animate__animated", "animate__bounce");
                setTimeout(() => cartCount.classList.remove("animate__animated", "animate__bounce"), 600);
            }

            alert(`${name} ajouté au panier !`);
        });
    });
});
