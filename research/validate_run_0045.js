// Post-run validation for the 2026-10-03T00:45Z price-radar test run.
// Read-only: validates committed-to-be data files, writes nothing.
const fs = require('fs');
const path = require('path');
const root = 'C:/Users/Administrator/hermes-price-radar';
const R = f => JSON.parse(fs.readFileSync(path.join(root, f), 'utf8'));

let pass = 0, fail = 0;
const ok = (c, m) => { if (c) { pass++; console.log('  PASS  ' + m); } else { fail++; console.log('  FAIL  ' + m); } };

let cfg, prod, hist;
console.log('=== 1. JSON validity ===');
for (const [f, k] of [['config/products.json', 'cfg'], ['data/products.json', 'prod'], ['data/price-history.json', 'hist']]) {
  try {
    const d = R(f);
    if (k === 'cfg') cfg = d; else if (k === 'prod') prod = d; else hist = d;
    ok(true, f + ' parses');
  } catch (e) { ok(false, f + ': ' + e.message); }
}

const P = prod.products || prod;
const obs = hist.observations || hist;
const RUN = '2026-10-03T00:45:00Z';

console.log('\n=== 2. No accidental product additions ===');
ok(Object.keys(P).length === 2, 'exactly 2 products (got ' + Object.keys(P).length + ')');
ok(cfg.tracked_part_numbers.length === 2, 'exactly 2 tracked_part_numbers');
ok(P['90NB15F1-M00A60'] && P['90NB10R2-M01820'], 'both expected part numbers present');
const allPNs = Object.keys(P);
ok(allPNs.every(p => /^90NB/.test(p)), 'all product keys are manufacturer part numbers');
ok(cfg.tracked_part_numbers.every(p => P[p.manufacturer_part_number]), 'every configured part number resolves to a product');
ok(!('unresolved_products' in prod) || (prod.unresolved_products || []).length === 0, 'no unresolved products added');

console.log('\n=== 3. Exact part-number matching on new listings ===');
const box = P['90NB15F1-M00A60'].retailers.box;
ok(!!box, 'Blue has box retailer');
// Box's URL slug is lowercased by the retailer, so match case-insensitively.
ok(/90NB15F1-M00A60/i.test(box.product_url), 'Box URL contains the Blue part number');
ok(/90NB15F1-M00A60/.test(box.evidence), 'Box evidence cites exact MPN');
ok(box.retailer_product_id === 'M1607KA-MB148W', 'Box sku matches Blue model number');
const tw = P['90NB15F1-M00A60'].retailers.technoworld;
ok(!!tw, 'Blue has technoworld retailer');
ok(tw.retailer_product_id === 'M1607KA-MB148W', 'Technoworld SKU matches Blue model');
const wmit = P['90NB10R2-M01820'].retailers['wmit-solutions'];
ok(!!wmit, 'Silver has wmit-solutions retailer');
ok(/m1605ya-mb601w/i.test(wmit.product_url), 'WMIT URL contains Silver SKU');
ok(wmit.retailer_product_id === 'M1605YA-MB601W', 'WMIT retailer_product_id is the Silver SKU');
ok(/SKU: M1605YA-MB601W/.test(wmit.evidence), 'WMIT evidence cites exact SKU');

console.log('\n=== 4. New records have required status values ===');
ok(box.verification_status === 'VERIFIED', 'Box VERIFIED');
ok(box.availability === 'out_of_stock', 'Box out_of_stock');
ok(box.price === 619.99, 'Box price 619.99 (got ' + box.price + ')');
ok(box.verification_method === 'structured_data', 'Box structured_data (JSON-LD)');
ok(/OutOfStock/.test(box.evidence), 'Box evidence cites JSON-LD OutOfStock');
ok(wmit.verification_status === 'VERIFIED', 'WMIT VERIFIED');
ok(wmit.availability === 'preorder', 'WMIT preorder');
ok(wmit.price === 613.27, 'WMIT price 613.27 (got ' + wmit.price + ')');
ok(/back-order/.test(wmit.evidence), 'WMIT evidence cites back-order');

console.log('\n=== 5. Technoworld: UNVERIFIED, price null, ambiguity retained ===');
ok(tw.verification_status === 'UNVERIFIED', 'Technoworld UNVERIFIED');
ok(tw.price === null, 'Technoworld price is null');
ok(tw.availability === 'in_stock', 'Technoworld availability in_stock (stock verified)');
ok(tw.last_verified === null, 'Technoworld last_verified null');
ok(Array.isArray(tw.ambiguous_prices_seen) && tw.ambiguous_prices_seen.length === 2, 'both ambiguous prices retained');
ok(tw.ambiguous_prices_seen.includes(503.46) && tw.ambiguous_prices_seen.includes(604.15), '503.46 and 604.15 both present');
ok(/INFERRED/.test(tw.ambiguity_note), 'ambiguity note says VAT interpretation is INFERRED');
ok(/NOT confirmed from any page label/.test(tw.ambiguity_note), 'ambiguity note says not confirmed from label');
ok(/340/.test(tw.spec_conflict_observed) && /330/.test(tw.spec_conflict_observed), 'conflicting CPU evidence retained (340 H1 / 330 body)');
ok('503.46' !== String(tw.price), '503.46 NOT adopted as price');
ok('604.15' !== String(tw.price), '604.15 NOT adopted as price');

console.log('\n=== 6. lowest_verified values unchanged ===');
ok(P['90NB15F1-M00A60'].lowest_verified.price === 549.99, 'Blue lowest_verified 549.99');
ok(P['90NB15F1-M00A60'].lowest_verified.retailer_slug === 'asus-uk-store', 'Blue lowest_verified from ASUS UK');
ok(P['90NB10R2-M01820'].lowest_verified.price === 499.99, 'Silver lowest_verified 499.99');
ok(P['90NB10R2-M01820'].lowest_verified.retailer_slug === 'asus-uk-store', 'Silver lowest_verified from ASUS UK');

console.log('\n=== 7. lowest_verified independently recomputed ===');
function recompute(rec) {
  const c = Object.values(rec.retailers).filter(l =>
    l.verification_status === 'VERIFIED' && l.availability === 'in_stock' &&
    l.price_type === 'standard' && l.price !== null && l.price !== undefined);
  if (!c.length) return null;
  return { price: Math.min(...c.map(x => x.price)), slug: c.sort((a,b)=>a.price-b.price)[0].retailer_slug };
}
for (const pn of allPNs) {
  const r = recompute(P[pn]);
  ok(r && r.price === P[pn].lowest_verified.price,
     pn + ' recompute ' + (r ? r.price : 'null') + ' == stored ' + P[pn].lowest_verified.price);
  ok(r && r.slug === P[pn].lowest_verified.retailer_slug, pn + ' recompute retailer matches');
}

console.log('\n=== 8. Ineligible prices cannot become lowest_verified ===');
const boxPrice = P['90NB15F1-M00A60'].lowest_verified.price;
ok(boxPrice !== box.price, 'Blue lowest_verified is not the out-of-stock Box price');
ok(boxPrice !== P['90NB15F1-M00A60'].retailers.laptopoutlet.price, 'Blue lowest_verified is not the out-of-stock LaptopOutlet price');
const silverLv = P['90NB10R2-M01820'].lowest_verified.price;
ok(silverLv !== wmit.price, 'Silver lowest_verified is not the preorder WMIT price');
const badStatuses = ['UNVERIFIED', 'BLOCKED', 'PARTIALLY_VERIFIED', 'STALE'];
for (const pn of allPNs) {
  for (const [slug, l] of Object.entries(P[pn].retailers)) {
    if (badStatuses.includes(l.verification_status) && l.price !== null)
      ok(P[pn].lowest_verified.price !== l.price, pn + '/' + slug + ' ineligible price not selected');
  }
}
for (const pn of allPNs) {
  for (const [slug, l] of Object.entries(P[pn].retailers)) {
    if (['out_of_stock', 'preorder', 'discontinued'].includes(l.availability) && l.price !== null)
      ok(P[pn].lowest_verified.price !== l.price, pn + '/' + slug + ' non-in_stock price not selected');
  }
}

console.log('\n=== 9. lowest_verified counts consistent ===');
const bl = P['90NB15F1-M00A60'];
ok(bl.lowest_verified.retailers_checked === Object.keys(bl.retailers).length, 'Blue retailers_checked matches actual (' + Object.keys(bl.retailers).length + ')');
ok(bl.lowest_verified.retailers_verified === Object.values(bl.retailers).filter(l => l.verification_status === 'VERIFIED').length, 'Blue retailers_verified matches');
const sl = P['90NB10R2-M01820'];
ok(sl.lowest_verified.retailers_checked === Object.keys(sl.retailers).length, 'Silver retailers_checked matches actual (' + Object.keys(sl.retailers).length + ')');
ok(sl.lowest_verified.retailers_verified === Object.values(sl.retailers).filter(l => l.verification_status === 'VERIFIED').length, 'Silver retailers_verified matches');

console.log('\n=== 10. Argos remains BLOCKED, no comparison to 549 ===');
for (const [pn, label] of [['90NB15F1-M00A60', 'Blue'], ['90NB10R2-M01820', 'Silver']]) {
  const a = P[pn].retailers.argos;
  ok(a.verification_status === 'BLOCKED', label + ' Argos BLOCKED');
  ok(a.price === null, label + ' Argos price null');
  ok(a.availability === 'unknown', label + ' Argos availability unknown');
  ok(a.last_known_price_unverified === 549.0, label + ' Argos unverified 549.0 retained as history');
  ok(P[pn].lowest_verified.price !== 549.0 || P[pn].lowest_verified.retailer_slug !== 'argos', label + ' lowest_verified never sourced from Argos');
}
const newObs = obs.filter(o => o.observed_at === RUN);
ok(newObs.every(o => !(o.retailer_slug === 'argos' && o.price !== null)), 'no new Argos observation carries a price');
ok(newObs.every(o => !/drop|dropped|fall|decrease/i.test(o.change_note || '')), 'no new observation claims a price drop');

console.log('\n=== 11. Observation count and structure ===');
ok(obs.length === 15, '15 observations total (7 baseline + 8 new), got ' + obs.length);
ok(newObs.length === 8, '8 new observations, got ' + newObs.length);
ok(obs.every(o => 'observed_at' in o && 'manufacturer_part_number' in o && 'verification_status' in o), 'every observation has required keys');
ok(obs.every(o => !('timestamp' in o)), 'no legacy timestamp field in observations');
ok(newObs.every(o => 'counts_toward_lowest_verified' in o), 'all 8 NEW observations have counts_toward_lowest_verified');
// Pre-existing baseline note: 2 of the 7 earlier observations (the original ASUS UK records
// written during the v2 migration) predate this field. Not introduced or altered by this run.
const missingCt = obs.filter(o => !('counts_toward_lowest_verified' in o));
ok(missingCt.every(o => o.observed_at !== RUN), 'no NEW observation omits counts_toward_lowest_verified');
if (missingCt.length) console.log('  NOTE  pre-existing records lacking the field: ' + missingCt.length +
   ' (' + missingCt.map(o => o.observation_id).join(', ') + ') - unchanged by this run');
ok(newObs.filter(o => o.counts_toward_lowest_verified === true).length === 2, 'exactly 2 new observations count toward lowest_verified');
ok(!('rejected_matches' in hist), 'rejected_matches still absent from price-history.json');
ok(hist.migrated_legacy_records.records.length === 2, '2 legacy records still preserved');
ok(hist.migrated_legacy_records.records.every(r => r.is_current_price === false && r.can_support_lowest_verified === false), 'legacy records still flagged non-current');

console.log('\n=== 12. New observations mirror product records ===');
const bySlug = {};
for (const o of newObs) bySlug[o.retailer_slug] = o;
ok(bySlug.box && bySlug.box.price === box.price && bySlug.box.availability === box.availability, 'box observation matches product record');
ok(bySlug.technoworld && bySlug.technoworld.price === null && bySlug.technoworld.availability === 'in_stock', 'technoworld observation matches');
ok(bySlug['wmit-solutions'] && bySlug['wmit-solutions'].price === wmit.price && bySlug['wmit-solutions'].availability === 'preorder', 'wmit observation matches');
ok(bySlug['wmit-solutions'].first_observation_for_product === true, 'wmit marked first observation (baseline, not a change)');
ok(bySlug.box.first_observation_for_product === true, 'box marked first observation (baseline, not a change)');
ok(bySlug.technoworld.first_observation_for_product === true, 'technoworld marked first observation');
const blueRepeat = newObs.find(o => o.retailer_slug === 'asus-uk-store' && o.manufacturer_part_number === '90NB15F1-M00A60');
ok(blueRepeat.first_observation_for_product === false, 'ASUS UK repeat observation not flagged as first');
ok(/Unchanged/.test(blueRepeat.change_note), 'ASUS UK repeat marked unchanged');

console.log('\n=== 13. All retailer URLs valid and direct ===');
const bad = [];
const NON_URL_SOURCE = /^(web_search|search|aggregator|manual)/i;
function chk(u, where) {
  if (!u) return;
  let host;
  try { host = new URL(u).host; } catch (e) { bad.push(where + ' unparseable: ' + u); return; }
  if (!/^https:/.test(u)) bad.push(where + ' not https: ' + u);
  if (/\/(search|browse|sd|category)\b/i.test(u)) bad.push(where + ' looks like listing page: ' + u);
}
for (const pn of allPNs) {
  for (const [slug, l] of Object.entries(P[pn].retailers)) {
    chk(l.product_url, pn + '/' + slug);
    // verification_source is a URL only for fetch-based methods; search_snippet /
    // aggregator_reported legitimately record the tool name instead.
    if (['direct_page_fetch', 'structured_data', 'blocked'].includes(l.verification_method)) {
      chk(l.verification_source, pn + '/' + slug + ' source');
    }
  }
  chk(P[pn].lowest_verified.product_url, pn + ' lowest_verified');
}
ok(bad.length === 0, 'all URLs https + direct product pages' + (bad.length ? ' -> ' + bad.join('; ') : ''));
const newURLs = [box.product_url, tw.product_url, wmit.product_url];
ok(newURLs.every(u => /^https:\/\//.test(u)), '3 new retailer URLs are https');

console.log('\n=== 14. Blue CPU conflict still unresolved ===');
const conf = P['90NB15F1-M00A60'].spec_conflicts;
ok(conf.length >= 1 && conf[0].field === 'cpu', 'cpu spec_conflict present');
ok(conf[0].resolved === false, 'still resolved=false (not guessed)');

console.log('\n=== 15. No schema change ===');
ok(hist._schema_version === '2.0', 'history _schema_version still 2.0');
ok(prod._schema_version === '2.0', 'products _schema_version still 2.0');
ok(cfg._schema_version === '2.0', 'config _schema_version still 2.0');
ok(!('rejected_matches' in hist), 'no new top-level keys added to history');
ok(Object.keys(hist).sort().join(',') === '_file_role,_note_on_migration,_schema_version,diagnostics,migrated_legacy_records,observations', 'history top-level keys unchanged');

console.log('\n========================================');
console.log('RESULT: ' + pass + ' passed, ' + fail + ' failed');
console.log('========================================');
process.exit(fail === 0 ? 0 : 1);