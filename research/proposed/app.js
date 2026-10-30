// Proposed rewrite of app.js for schema v2 — NOT DEPLOYED, review only.
// Two changes:
//   1. products.json is now { _schema_version, products: {...} } — unwrap the .products map.
//   2. price-history.json is now an object, not an array — read .observations.
// Old code read: Object.keys(products) and history.length / history.slice(-5) / entry.timestamp.
// Those all break silently (count becomes 1, cards render "Unknown Product") rather than erroring,
// so the unwrap must be explicit.

document.addEventListener('DOMContentLoaded', function() {
    loadData();
});

function loadData() {
    fetch('data/products.json')
        .then(response => response.json())
        .then(payload => {
            const products = payload.products || payload;   // tolerate both shapes during rollout
            displayProducts(products);
            const count = Object.keys(products).length;
            document.getElementById('product-count').textContent = count;
        })
        .catch(error => {
            console.error('Error loading products:', error);
            document.getElementById('product-count').textContent = 'Error';
        });

    fetch('data/price-history.json')
        .then(response => response.json())
        .then(payload => {
            const observations = payload.observations || payload;   // tolerate both shapes
            document.getElementById('history-count').textContent = observations.length;
            displayRecentChanges(observations);
        })
        .catch(error => {
            console.error('Error loading price history:', error);
            document.getElementById('history-count').textContent = 'Error';
        });

    const now = new Date();
    document.getElementById('last-updated').textContent =
        `Last updated: ${now.toLocaleString()}`;
}

function escapeHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function displayProducts(products) {
    const container = document.getElementById('products-container');

    if (Object.keys(products).length === 0) {
        container.innerHTML = '<p>No products being tracked yet.</p>';
        return;
    }

    let html = '';
    for (const [partNumber, product] of Object.entries(products)) {

        // lowest_verified is the only price allowed on the page.
        // null means nothing was verified this run — show that plainly, never a fallback number.
        const lowest = product.lowest_verified;
        let priceBlock;
        if (lowest && lowest.price !== null && lowest.price !== undefined) {
            priceBlock = `
                <div class="price">&pound;${escapeHtml(lowest.price)}</div>
                <div class="retailer">${escapeHtml(lowest.retailer_slug)}</div>
                <div class="meta">${escapeHtml(lowest.retailers_verified_and_purchasable)} of
                    ${escapeHtml(lowest.retailers_checked)} retailers verified and in stock</div>
                ${lowest.product_url ?
                    `<div class="url"><a href="${escapeHtml(lowest.product_url)}" target="_blank" rel="noopener">View Product</a></div>` : ''}
            `;
        } else {
            priceBlock = `
                <div class="price">No verified price</div>
                <div class="meta">${escapeHtml(lowest ? lowest.retailers_checked : 0)} retailers checked,
                    none could be verified</div>
            `;
        }

        // Per-retailer breakdown, so BLOCKED and out-of-stock are visible rather than hidden.
        let retailerRows = '';
        for (const listing of Object.values(product.retailers || {})) {
            const priceText = listing.price === null || listing.price === undefined
                ? '&mdash;'
                : '&pound;' + escapeHtml(listing.price);
            retailerRows += `
                <tr>
                    <td>${escapeHtml(listing.retailer)}</td>
                    <td>${priceText}</td>
                    <td>${escapeHtml(listing.availability)}</td>
                    <td>${escapeHtml(listing.verification_status)}</td>
                    <td>${listing.product_url ?
                        `<a href="${escapeHtml(listing.product_url)}" target="_blank" rel="noopener">link</a>` : '&mdash;'}</td>
                </tr>
            `;
        }

        // An unresolved spec conflict must be surfaced, not buried.
        const conflicts = (product.spec_conflicts || []).filter(c => !c.resolved);
        const conflictBlock = conflicts.length
            ? `<div class="warning">Specification conflict unresolved: ${conflicts.map(c => escapeHtml(c.field)).join(', ')}</div>`
            : '';

        html += `
            <div class="product-card">
                <h3>${escapeHtml(product.product || product.model || 'Unknown Product')}</h3>
                <div class="part-number">Part number: ${escapeHtml(product.manufacturer_part_number || partNumber)}</div>
                ${priceBlock}
                ${conflictBlock}
                <table class="retailer-table">
                    <thead><tr><th>Retailer</th><th>Price</th><th>Availability</th><th>Status</th><th>URL</th></tr></thead>
                    <tbody>${retailerRows}</tbody>
                </table>
            </div>
        `;
    }
    container.innerHTML = html;
}

function displayRecentChanges(observations) {
    const changesList = document.getElementById('changes-list');

    if (!observations || observations.length === 0) {
        changesList.textContent = 'No price history yet';
        return;
    }

    const recent = observations.slice(-5).reverse();
    let html = '';

    for (const entry of recent) {
        // Field renamed timestamp -> observed_at. Accept both so mixed history renders.
        const rawDate = entry.observed_at || entry.timestamp;
        const date = new Date(rawDate);
        const shown = isNaN(date.getTime()) ? 'unknown date' : date.toLocaleDateString();
        const priceText = entry.price === null || entry.price === undefined ? 'no price' : `&pound;${entry.price}`;
        const status = entry.verification_status ? ` [${escapeHtml(entry.verification_status)}]` : '';
        html += `<div><strong>${escapeHtml(entry.product || 'Unknown')}</strong> at ` +
                `${escapeHtml(entry.retailer || 'Unknown')}: ${priceText} (${shown})${status}</div>`;
    }

    changesList.innerHTML = html;
}