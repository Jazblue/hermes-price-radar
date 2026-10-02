// Final pre-commit validation for schema v2 migration.
const fs = require('fs');
const path = require('path');
const root = 'C:/Users/Administrator/hermes-price-radar';

let pass = 0, fail = 0;
const ok = (c, m) => { if (c) { pass++; console.log('  PASS  ' + m); } else { fail++; console.log('  FAIL  ' + m); } };

console.log('=== 1. Valid JSON for all three data/config files ===');
let cfg, prod, hist;
try { cfg = JSON.parse(fs.readFileSync(path.join(root, 'config/products.json'), 'utf8')); ok(true, 'config/products.json parses'); } catch (e) { ok(false, 'config/products.json: ' + e.message); }
try { prod = JSON.parse(fs.readFileSync(path.join(root, 'data/products.json'), 'utf8')); ok(true, 'data/products.json parses'); } catch (e) { ok(false, 'data/products.json: ' + e.message); }
try { hist = JSON.parse(fs.readFileSync(path.join(root, 'data/price-history.json'), 'utf8')); ok(true, 'data/price-history.json parses'); } catch (e) { ok(false, 'data/price-history.json: ' + e.message); }

console.log('\n=== 2. app.js syntax ===');
const appSrc = fs.readFileSync(path.join(root, 'app.js'), 'utf8');
try { new Function(appSrc); ok(true, 'app.js parses as valid JS'); } catch (e) { ok(false, 'app.js syntax: ' + e.message); }
ok(appSrc.includes('payload.observations || payload'), 'app.js unwraps price-history object');
ok(appSrc.includes('payload.products || payload'), 'app.js unwraps products object');
ok(appSrc.includes('No verified price'), 'app.js has no-verified-price fallback');

console.log('\n=== 3. Both ASUS products present ===');
const P = prod.products || prod;
ok(!!P['90NB15F1-M00A60'], 'Blue product present');
ok(!!P['90NB10R2-M01820'], 'Silver product present');
ok(Object.keys(P).length === 2, 'exactly 2 products tracked (got ' + Object.keys(P).length + ')');

console.log('\n=== 4. Correct manufacturer part numbers ===');
ok(P['90NB15F1-M00A60'].manufacturer_part_number === '90NB15F1-M00A60', 'Blue part number matches key');
ok(P['90NB15F1-M00A60'].model_number === 'M1607KA-MB148W', 'Blue model M1607KA-MB148W');
ok(P['90NB10R2-M01820'].manufacturer_part_number === '90NB10R2-M01820', 'Silver part number matches key');
ok(P['90NB10R2-M01820'].model_number === 'M1605YA-MB601W', 'Silver model M1605YA-MB601W');

console.log('\n=== 5/6. ASUS UK VERIFIED + in stock prices ===');
const blue = P['90NB15F1-M00A60'].retailers['asus-uk-store'];
const silver = P['90NB10R2-M01820'].retailers['asus-uk-store'];
ok(blue.price === 549.99, 'Blue ASUS UK price 549.99 (got ' + blue.price + ')');
ok(blue.verification_status === 'VERIFIED', 'Blue ASUS UK VERIFIED');
ok(blue.availability === 'in_stock', 'Blue ASUS UK in_stock');
ok(silver.price === 499.99, 'Silver ASUS UK price 499.99 (got ' + silver.price + ')');
ok(silver.verification_status === 'VERIFIED', 'Silver ASUS UK VERIFIED');
ok(silver.availability === 'in_stock', 'Silver ASUS UK in_stock');
ok(!!blue.evidence && !!silver.evidence, 'both carry evidence strings');

console.log('\n=== 7. Argos listings BLOCKED ===');
for (const [pn, label] of [['90NB15F1-M00A60', 'Blue'], ['90NB10R2-M01820', 'Silver']]) {
  const a = P[pn].retailers['argos'];
  ok(!!a, label + ' has Argos listing');
  ok(a.verification_status === 'BLOCKED', label + ' Argos BLOCKED');
  ok(a.price === null, label + ' Argos price is null (not a current price)');
  ok(!!a.block_reason, label + ' Argos has block_reason');
  ok(a.retailer_product_id === (label === 'Blue' ? '7741159' : '7761225'), label + ' Argos product id retained: ' + a.retailer_product_id);
}

console.log('\n=== 8. Laptop Outlet Blue excluded (out of stock) ===');
const lo = P['90NB15F1-M00A60'].retailers['laptopoutlet'];
ok(lo.price === 619.99, 'Laptop Outlet price 619.99 retained');
ok(lo.verification_status === 'VERIFIED', 'Laptop Outlet VERIFIED');
ok(lo.availability === 'out_of_stock', 'Laptop Outlet out_of_stock');
ok(!!lo.excluded_from_lowest_verified_reason, 'Laptop Outlet carries exclusion reason');
ok(P['90NB15F1-M00A60'].lowest_verified.price !== 619.99, 'lowest_verified is NOT the out-of-stock price');

console.log('\n=== 9. lowest_verified values correct ===');
ok(P['90NB15F1-M00A60'].lowest_verified.price === 549.99, 'Blue lowest_verified 549.99');
ok(P['90NB15F1-M00A60'].lowest_verified.retailer_slug === 'asus-uk-store', 'Blue lowest_verified from ASUS UK');
ok(P['90NB10R2-M01820'].lowest_verified.price === 499.99, 'Silver lowest_verified 499.99');
ok(P['90NB10R2-M01820'].lowest_verified.retailer_slug === 'asus-uk-store', 'Silver lowest_verified from ASUS UK');

console.log('\n=== 10. No unverified price used as lowest_verified (recompute independently) ===');
function recompute(rec) {
  const cands = Object.values(rec.retailers).filter(l =>
    l.verification_status === 'VERIFIED' && l.availability === 'in_stock' &&
    l.price_type === 'standard' && l.price !== null && l.price !== undefined);
  if (!cands.length) return null;
  return Math.min(...cands.map(c => c.price));
}
for (const pn of ['90NB15F1-M00A60', '90NB10R2-M01820']) {
  const expect = recompute(P[pn]);
  ok(expect === P[pn].lowest_verified.price,
     pn + ' lowest_verified matches independent recompute (' + expect + ')');
  const anyUnverified = Object.values(P[pn].retailers).some(l =>
    ['UNVERIFIED','BLOCKED','PARTIALLY_VERIFIED','STALE'].includes(l.verification_status) &&
    P[pn].lowest_verified.price === l.price);
  ok(!anyUnverified, pn + ' lowest_verified does not match any unverified/blocked price');
}

console.log('\n=== 11. History: structure + no rejected_matches + legacy preserved ===');
ok(Array.isArray(hist.observations), 'observations is an array');
ok(!('rejected_matches' in hist), 'rejected_matches NOT in price-history.json');
ok(typeof hist.migrated_legacy_records === 'object', 'migrated_legacy_records present');
const legacy = hist.migrated_legacy_records.records;
ok(legacy.length === 2, '2 legacy Argos records preserved');
ok(legacy.every(r => r.is_current_price === false), 'legacy marked is_current_price false');
ok(legacy.every(r => r.can_support_lowest_verified === false), 'legacy cannot support lowest_verified');
ok(legacy.every(r => r.price === 549.0), 'legacy price 549.00 preserved verbatim');
ok(legacy.every(r => r.verification_status === 'UNVERIFIED'), 'legacy records UNVERIFIED');
ok(hist.observations.every(o => 'observed_at' in o), 'all observations use observed_at');
const blockedObs = hist.observations.filter(o => o.verification_status === 'BLOCKED');
ok(blockedObs.length === 2, '2 BLOCKED observations recorded (got ' + blockedObs.length + ')');
ok(blockedObs.every(o => o.price === null), 'BLOCKED observations carry price null');
const diag = hist.diagnostics;
ok(diag.some(d => d.retailer === 'Argos' && d.http_status_via_jina === 200 && d.body_contained_block_marker === true),
   'diagnostics record the Jina 200 + Access Denied trap');

console.log('\n=== 12. Silver baseline is not framed as a price drop ===');
const silverObs = hist.observations.find(o => o.manufacturer_part_number === '90NB10R2-M01820' && o.retailer_slug === 'asus-uk-store');
ok(silverObs.first_observation_for_product === true, 'Silver ASUS UK marked first_observation_for_product');
ok(/NEW RETAILER DISCOVERED, NOT A PRICE MOVE/.test(silverObs.interpretation_note || ''), 'Silver carries NOT-A-PRICE-MOVE note');

console.log('\n=== 13. Blue CPU conflict unresolved ===');
const conf = P['90NB15F1-M00A60'].spec_conflicts;
ok(conf.length === 1 && conf[0].field === 'cpu', 'Blue has one cpu spec conflict');
ok(conf[0].resolved === false, 'Blue CPU conflict resolved=false');
ok(conf[0].values.length === 3, 'conflict records all 3 readings (got ' + conf[0].values.length + ')');
ok(P['90NB10R2-M01820'].spec_conflicts.length === 0, 'Silver has no conflicts');

console.log('\n=== 14. Evasion disabled ===');
ok(cfg.global_settings.evasion_attempts_allowed === false, 'evasion_attempts_allowed false');
ok(cfg.global_settings.verify_body_not_just_status === true, 'verify_body_not_just_status true');
ok(Array.isArray(cfg.global_settings.block_markers) && cfg.global_settings.block_markers.includes('Access Denied'), 'Access Denied in block_markers');
ok(cfg.global_settings.never_substitute_unverified_price === true, 'never_substitute_unverified_price true');
ok(!('products' in cfg), 'config/products.json holds no product/pricing state');
ok(!JSON.stringify(cfg).includes('current_price'), 'config contains no prices');

console.log('\n=== 15. Website links are direct retailer URLs ===');
const allowed = ['uk.store.asus.com', 'www.laptopoutlet.co.uk', 'www.argos.co.uk', 'ao.com', 'www.amazon.co.uk'];
const bad = [];
function checkUrl(u, where) {
  if (!u) return;
  let host;
  try { host = new URL(u).host; } catch (e) { bad.push(where + ' unparseable: ' + u); return; }
  if (!allowed.includes(host)) bad.push(where + ' unexpected host: ' + host);
  if (/\/(search|browse|sd|category)/i.test(u)) bad.push(where + ' looks like a listing/category page: ' + u);
}
for (const pn of Object.keys(P)) {
  checkUrl(P[pn].lowest_verified && P[pn].lowest_verified.product_url, pn + ' lowest_verified');
  for (const [slug, l] of Object.entries(P[pn].retailers)) checkUrl(l.product_url, pn + '/' + slug);
}
ok(bad.length === 0, 'all product URLs are direct retailer product pages' + (bad.length ? ' -> ' + bad.join('; ') : ''));
ok(P['90NB15F1-M00A60'].lowest_verified.product_url.includes('uk.store.asus.com'), 'lowest_verified link points at ASUS UK');

console.log('\n=== 16. Discovery config sanity ===');
const cat = cfg.categories[0];
ok(cat.retailers.includes('uk.store.asus.com'), 'ASUS UK store in retailer list');
ok(cat.retailers.includes('argos.co.uk'), 'Argos still listed (recorded BLOCKED, not dropped)');
ok(!!cat.retailer_notes && !!cat.retailer_notes['argos.co.uk'], 'Argos retailer note documents the block');
ok(cfg.tracked_part_numbers.length === 2, '2 part numbers tracked');

console.log('\n========================================');
console.log('RESULT: ' + pass + ' passed, ' + fail + ' failed');
console.log('========================================');
process.exit(fail === 0 ? 0 : 1);