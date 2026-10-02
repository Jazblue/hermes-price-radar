// Hermes Price Radar - Frontend JavaScript
// This file handles displaying data from the JSON files

document.addEventListener('DOMContentLoaded', function() {
    loadData();
});

function loadData() {
    // Fetch products data
    fetch('data/products.json')
        .then(response => response.json())
        .then(products => {
            displayProducts(products);
            document.getElementById('product-count').textContent = Object.keys(products).length;
        })
        .catch(error => {
            console.error('Error loading products:', error);
            document.getElementById('product-count').textContent = 'Error';
        });
    
    // Fetch price history data
    fetch('data/price-history.json')
        .then(response => response.json())
        .then(history => {
            document.getElementById('history-count').textContent = history.length;
            displayRecentChanges(history);
        })
        .catch(error => {
            console.error('Error loading price history:', error);
            document.getElementById('history-count').textContent = 'Error';
        });
    
    // Update last updated time
    const now = new Date();
    document.getElementById('last-updated').textContent = 
        `Last updated: ${now.toLocaleString()}`;
}

function displayProducts(products) {
    const container = document.getElementById('products-container');
    
    if (Object.keys(products).length === 0) {
        container.innerHTML = '<p>No products being tracked yet. Add products to config/products.json to start tracking.</p>';
        return;
    }
    
    let html = '';
    for (const [id, product] of Object.entries(products)) {
        html += `
            <div class="product-card">
                <h3>${product.product || 'Unknown Product'}</h3>
                <div class="price">£${product.current_price || 'N/A'}</div>
                <div class="retailer">${product.retailer || 'Unknown Retailer'}</div>
                ${product.availability ? `<div>Availability: ${product.availability}</div>` : ''}
                ${product.url ? `<div class="url"><a href="${product.url}" target="_blank">View Product</a></div>` : ''}
                ${product.lowest_recorded !== undefined ? 
                    `<div>Lowest: £${product.lowest_recorded}</div>` : ''}
                ${product.highest_recorded !== undefined ? 
                    `<div>Highest: £${product.highest_recorded}</div>` : ''}
            </div>
        `;
    }
    container.innerHTML = html;
}

function displayRecentChanges(history) {
    const changesList = document.getElementById('changes-list');
    
    if (history.length === 0) {
        changesList.textContent = 'No price history yet';
        return;
    }
    
    // Show last 5 changes
    const recentChanges = history.slice(-5).reverse();
    let html = '';
    
    for (const entry of recentChanges) {
        const date = new Date(entry.timestamp);
        html += `<div><strong>${entry.product || 'Unknown'}</strong> at ${entry.retailer || 'Unknown'}: £${entry.price} (${date.toLocaleDateString()})</div>`;
    }
    
    changesList.innerHTML = html;
}
