document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("productForm");
  const grid = document.getElementById("productsGrid");

  // 🌐 Backend API URL
  const API_URL = "http://127.0.0.1:8000/products/";

  // 🧭 Function to load products
  async function loadProducts() {
    grid.innerHTML = "<p style='text-align:center;'>Loading products...</p>";

    try {
      const response = await fetch(API_URL);
      if (!response.ok) throw new Error("Network error");
      const products = await response.json();

      grid.innerHTML = "";

      if (products.length === 0) {
        grid.innerHTML = "<p style='text-align:center; opacity:0.7;'>No products tracked yet.</p>";
        return;
      }

      products.forEach((p, index) => {
        const card = document.createElement("div");
        card.classList.add("product-card");
        card.style.animationDelay = `${index * 0.2}s`;
        card.innerHTML = `
          <h3>${p.name}</h3>
          <p><strong>Current Price:</strong> ₹${p.current_price}</p>
          <p><a href="${p.url}" target="_blank" style="color:#ffd6e0;">View Product</a></p>
        `;
        grid.appendChild(card);
      });
    } catch (err) {
      console.error("Error fetching products:", err);
      grid.innerHTML = "<p style='color:red;'>Failed to load products. Is backend running?</p>";
    }
  }

  // 🆕 Add new product
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const url = document.getElementById("url").value.trim();
    const price = parseFloat(document.getElementById("price").value);

    if (!name || !url || isNaN(price)) {
      alert("Please fill in all fields correctly.");
      return;
    }

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          url: url,
          current_price: price
        })
      });

      if (!res.ok) throw new Error(`Error: ${res.status}`);
      await res.json();

      form.reset();
      loadProducts(); // reload after adding
    } catch (err) {
      alert("❌ Failed to add product. Please check your backend connection.");
      console.error(err);
    }
  });

  // 🚀 Load products when page opens
  loadProducts();
});
