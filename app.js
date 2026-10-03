// Simplified app.js for Price Radar - shows product-store table from Google Sheets data
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});

function loadData() {
    fetch('data/products.json')
        .then(response => response.json())
        .then(payload => {
            const products = payload.products || payload;   // tolerate both shapes during rollout
            fetch('data/price-history.json')
                .then(response => response.json())
                .then(payload2 => {
                    const observations = payload2.observations || payload2;   // tolerate both shapes
                    displayProductsTable(products, observations);
                    const count = Object.keys(products).length;
                    document.getElementById('product-count').textContent = count;
                    document.getElementById('history-count').textContent = observations.length;
                    displayRecentChanges(observations);
                })
                .catch(error => {
                    console.error('Error loading price history:', error);
                    document.getElementById('history-count').textContent = 'Error';
                });
        })
        .catch(error => {
            console.error('Error loading products:', error);
            document.getElementById('product-count').textContent = 'Error';
        });

    const now = new Date();
    document.getElementById('last-updated').textContent =
        `Last updated: ${now.toLocaleString()}`;
}

function escapeHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;').replace(/'/g, '&#39;');
}

function displayProductsTable(products, observations) {
    const container = document.getElementById('products-container');
    
    // Build map: partNumber -> retailerSlug -> {productName, productUrl, latestObsTime, verifiedStats}
    const stats = {};
    
    // First, initialize from products data
    for (const [partNumber, product] of Object.entries(products)) {
        stats[partNumber] = {};
        for (const [retailerSlug, listing] of Object.entries(product.retailers || {})) {
            stats[partNumber][retailerSlug] = {
                productName: product.product || product.model || 'Unknown Product',
                productUrl: listing.product_url || '',
                latestObsTime: null, // will update from observations
                verifiedStats: {
                    current: null,
                    lowest: null,
                    highest: null,
                    lastChecked: null
                }
            };
        }
    }
    
    // Process observations to fill latestObsTime and verified stats
    for (const obs of observations) {
        const partNumber = obs.manufacturer_part_number;
        const retailerSlug = obs.retailer_slug;
        if (!stats[partNumber] || !stats[partNumber][retailerSlug]) {
            // unknown product/retailer, skip
            continue;
        }
        const obsDate = new Date(obs.observed_at || obs.timestamp);
        const item = stats[partNumber][retailerSlug];
        // Update latest observation time (any status)
        if (!item.latestObsTime || obsDate > item.latestObsTime) {
            item.latestObsTime = obsDate;
        }
        // If verified and price present, update verified stats
        if (obs.verification_status === 'VERIFIED' && obs.price !== null && obs.price !== undefined) {
            const price = parseFloat(obs.price);
            if (!isNaN(price)) {
                const vs = item.verifiedStats;
                if (vs.current === null || obsDate > new Date(vs.lastChecked || 0)) {
                    vs.current = price;
                    vs.lastChecked = obs.observed_at || obs.timestamp;
                }
                if (vs.lowest === null || price < vs.lowest) {
                    vs.lowest = price;
                }
                if (vs.highest === null || price > vs.highest) {
                    vs.highest = price;
                }
            }
        }
    }
    
    // Build table HTML
    let html = '<table class="price-table"><thead><tr>';
    html += '<th>Laptop</th><th>Store</th><th>Today\'s Price</th><th>Lowest Price</th><th>Highest Price</th><th>Store Link</th><th>Last Checked</th>';
    html += '</tr></thead><tbody>';
    
    for (const [partNumber, retailers] of Object.entries(stats)) {
        // A laptop must appear even when it has no store rows yet.
        // A product flagged placeholder_id must not be shown as a genuine identifier.
        const entries = Object.entries(retailers);
        if (entries.length === 0) {
            const product = products[partNumber];
            const name = product.product || product.model || product.marketing_title || 'Unknown Product';
            html += `<tr>`;
            html += `<td>${escapeHtml(name)}${placeholderBadge(product)}</td>`;
            html += `<td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>`;
            html += `</tr>`;
            continue;
        }
        for (const [retailerSlug, data] of entries) {
            const product = products[partNumber];
            const vs = data.verifiedStats;
            const priceToday = vs.current !== null ? `£${vs.current.toFixed(2)}` : '-';
            const lowest = vs.lowest !== null ? `£${vs.lowest.toFixed(2)}` : '-';
            const highest = vs.highest !== null ? `£${vs.highest.toFixed(2)}` : '-';
            const lastChecked = vs.lastChecked ? new Date(vs.lastChecked).toLocaleString() : '-';
            const link = data.productUrl ? `<a href="${escapeHtml(data.productUrl)}" target="_blank" rel="noopener">link</a>` : '-';
            html += `<tr>`;
            html += `<td>${escapeHtml(data.productName)}${placeholderBadge(product)}</td>`;
            html += `<td>${escapeHtml(retailerSlug)}</td>`;
            html += `<td>${priceToday}</td>`;
            html += `<td>${lowest}</td>`;
            html += `<td>${highest}</td>`;
            html += `<td>${link}</td>`;
            html += `<td>${lastChecked}</td>`;
            html += `</tr>`;
        }
    }
    
    html += '</tbody></table>';
    
    if (Object.keys(stats).length === 0) {
        html = '<p>No product-store data available.</p>';
    }
    
    container.innerHTML = html;
}

// Placeholder part numbers are not real identifiers. Flag them visibly.
function placeholderBadge(product) {
    if (!product || !product.placeholder_id) return '';
    return ` <span class="placeholder-flag">[PLACEHOLDER ID - not verified]</span>`;
}

// Keep existing displayRecentChanges for sidebar
function displayRecentChanges(observations) {
    const changesList = document.getElementById('changes-list');
    if (!observations || observations.length === 0) {
        changesList.textContent = 'No price history yet';
        return;
    }
    const recent = observations.slice(-5).reverse();
    let html = '';
    for (const entry of recent) {
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
