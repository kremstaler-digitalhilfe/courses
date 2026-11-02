#!/usr/bin/env node
/**
 * Scan docs/**/*.html with Playwright + axe-core (WCAG 2.2 AA + AAA tags).
 * Usage: node scripts/a11y-audit.mjs [--json] [glob…]
 */
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import { readdir, writeFile } from 'node:fs/promises';
import { join, relative, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const ROOT = resolve(import.meta.dirname, '..');
const DOCS = join(ROOT, 'docs');
const wantJson = process.argv.includes('--json');
const filters = process.argv.slice(2).filter((a) => a !== '--json');

async function listHtml(dir, out = []) {
  for (const ent of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, ent.name);
    if (ent.isDirectory()) {
      if (ent.name === 'powerpoint' || ent.name === 'node_modules') continue;
      await listHtml(p, out);
    } else if (ent.name.endsWith('.html')) {
      out.push(p);
    }
  }
  return out;
}

function severityRank(impact) {
  return { critical: 0, serious: 1, moderate: 2, minor: 3 }[impact] ?? 9;
}

const browser = await chromium.launch();
const context = await browser.newContext();
const page = await context.newPage();

const all = await listHtml(DOCS);
const files = filters.length
  ? all.filter((f) => filters.some((g) => relative(DOCS, f).includes(g)))
  : all;

const summary = [];
let failPages = 0;

for (const file of files) {
  const rel = relative(DOCS, file);
  const url = pathToFileURL(file).href;
  await page.goto(url, { waitUntil: 'domcontentloaded' });

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'wcag2aaa', 'best-practice'])
    .analyze();

  const violations = results.violations
    .map((v) => ({
      id: v.id,
      impact: v.impact,
      help: v.help,
      nodes: v.nodes.length,
      tags: v.tags.filter((t) => t.startsWith('wcag')),
    }))
    .sort((a, b) => severityRank(a.impact) - severityRank(b.impact));

  const critical = violations.filter((v) => v.impact === 'critical' || v.impact === 'serious');
  if (critical.length) failPages += 1;

  summary.push({ file: rel, violations, passes: results.passes.length, incomplete: results.incomplete.length });

  const mark = critical.length ? 'FAIL' : violations.length ? 'WARN' : 'OK  ';
  console.log(`${mark}  ${rel}  (${violations.length} viol., ${results.passes.length} pass)`);
  for (const v of violations.slice(0, 12)) {
    console.log(`      [${v.impact}] ${v.id}: ${v.help} (${v.nodes})`);
  }
}

await browser.close();

if (wantJson) {
  const out = join(ROOT, 'a11y-report.json');
  await writeFile(out, JSON.stringify({ generatedAt: new Date().toISOString(), pages: summary }, null, 2));
  console.log(`\nWrote ${out}`);
}

console.log(`\n${files.length} pages · ${failPages} with critical/serious`);
process.exit(failPages ? 1 : 0);
