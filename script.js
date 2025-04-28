// JavaScript Code for Malik Ab Hannan's Online Dukaan

// Backend API URL
const API_URL = 'http://127.0.0.1:5000/api'; // Flask server ka address aur port

// Wait until the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {

    // Select the product grid element
    const productGrid = document.querySelector('.product-grid');
    // Select the cart count element
    const cartCountSpan = document.querySelector('.cart-count');

    // Function to fetch products from the backend API
    async function fetchProducts() {
        try {
            // Loading message dikhayein
            productGrid.innerHTML = '<p class="loading-message">Products load ho rahe hain...</p>';

            // Backend API se products data fetch karein
            const response = await fetch(`${API_URL}/products`);

            // Check karein ke response theek hai (status code 200-299)
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Response ko JSON mein convert karein
            const products = await response.json();

            // Products ko webpage par display karein
            displayProducts(products);

        } catch (error) {
            // Error handling: Agar data fetch na ho sake toh console mein error dikhayein aur user ko batayein
            console.error('Error fetching products:', error);
            productGrid.innerHTML = '<p class="error-message">Products load nahi ho sake. Server chal raha hai ya check karein.</p>';
        }
    }

    // Function to display products on the webpage
    function displayProducts(products) {
        // Pehle se maujood content (loading message) ko hata dein
        productGrid.innerHTML = '';

        // Agar koi products nahi hain
        if (products.length === 0) {
            productGrid.innerHTML = '<p>Koi products dastiyab nahi hain.</p>';
            return;
        }

        // Har product ke liye HTML card banayein aur grid mein add karein
        products.forEach(product => {
            const productCardHTML = `
                <div class="product-card">
                    <img src="${product.image_url}" alt="${product.name}">
                    <div class="product-info">
                        <h3>${product.name}</h3>
                        <p>${product.description}</p>
                        <span class="price">Rs. ${product.price}</span>
                        <button class="add-to-cart" data-product-id="${product.id}">Cart mein shamil karein</button>
                    </div>
                </div>
            `;
            productGrid.innerHTML += productCardHTML; // Product card ko grid mein add karein
        });

        // Naye add kiye gaye buttons par event listeners lagayein
        attachAddToCartListeners();
    }

    // Function to attach click event listeners to 'Add to Cart' buttons
    function attachAddToCartListeners() {
         // Saare 'Add to Cart' buttons ko select karein
         const addToCartButtons = document.querySelectorAll('.add-to-cart');

         // Har button par click listener lagayein
         addToCartButtons.forEach(button => {
             // Ensure no duplicate listeners are attached
             button.removeEventListener('click', handleAddToCartClick); // Remove if already exists
             button.addEventListener('click', handleAddToCartClick); // Add the listener
         });
    }

    // Event handler for 'Add to Cart' button click
    async function handleAddToCartClick(event) {
         const button = event.target;
         const productId = button.dataset.productId; // Button ke data attribute se product ID lein

         try {
             // Backend API ko request bhejein cart mein item add karne ke liye
             const response = await fetch(`${API_URL}/cart/add/${productId}`, {
                 method: 'POST', // POST request istemal karein
                 headers: {
                     'Content-Type': 'application/json'
                 }
                 // Agar aapko product ki quantity ya doosri details bhejni hon toh body mein bhej sakte hain
                 // body: JSON.stringify({ quantity: 1 })
             });

             if (!response.ok) {
                 throw new Error(`HTTP error! status: ${response.status}`);
             }

             const result = await response.json();
             console.log('Add to cart response:', result);

             // Cart count update karein (backend se milne wale count ka istemal karein)
             updateCartCount();

             // User ko success message dikhayein (aik simple alert for now)
             // Asli application mein behtar UI notification istemal karein
             alert(`Product ID ${productId} cart mein shamil kiya gaya!`);

         } catch (error) {
             console.error('Error adding product to cart:', error);
             alert('Product cart mein shamil nahi ho saka. Server check karein.');
         }
    }

    // Function to fetch and update the cart count from the backend
    async function updateCartCount() {
        try {
            const response = await fetch(`${API_URL}/cart/count`);
             if (!response.ok) {
                 throw new Error(`HTTP error! status: ${response.status}`);
             }
            const data = await response.json();
            cartCountSpan.textContent = data.count; // Backend se milne wala count dikhayein
        } catch (error) {
            console.error('Error fetching cart count:', error);
            // Agar count fetch na ho sake toh default 0 dikha sakte hain ya error message
            cartCountSpan.textContent = '0';
        }
    }


    // Page load hone par products fetch karein aur cart count update karein
    fetchProducts();
    updateCartCount();

});
