// Plotline view counter. No cookies, no login, nothing stored about a visitor.
// POST /hit  {p: plot id, r: referrer host}  -> increments views for (day, plot, referrer); counts a daily unique
//            from a salted hash of IP + user agent + day that is never stored in raw form.
// GET  /stats?key=...  -> totals and the last 90 days per plot, plus referrers (private; needs the key).
const ORIGINS = ['https://luyenchou1.github.io'];
const cors = (req) => { const o = req.headers.get('Origin') || ''; return { 'Access-Control-Allow-Origin': ORIGINS.includes(o) ? o : ORIGINS[0], 'Access-Control-Allow-Methods': 'POST, GET, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' }; };
async function sha(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].slice(0, 16).map(x => x.toString(16).padStart(2, '0')).join(''); }

export default {
  async fetch(req, env) {
    const url = new URL(req.url); const h = cors(req);
    if (req.method === 'OPTIONS') return new Response(null, { headers: h });
    const id = env.COUNTER.idFromName('plotline'); const stub = env.COUNTER.get(id);
    if (req.method === 'POST' && url.pathname === '/hit') {
      let body = {}; try { body = await req.json(); } catch (e) {}
      const plot = String(body.p || '').replace(/[^a-z0-9-]/g, '').slice(0, 40); if (!plot) return new Response('no', { status: 400, headers: h });
      const ref = String(body.r || '').replace(/[^a-z0-9.-]/g, '').slice(0, 80) || 'direct';
      const day = new Date().toISOString().slice(0, 10);
      const ip = req.headers.get('CF-Connecting-IP') || ''; const ua = req.headers.get('User-Agent') || '';
      const salt = env.STATS_KEY || 'plotline'; const vh = await sha(`${salt}|${day}|${ip}|${ua}`);
      const country = req.headers.get('CF-IPCountry') || '';
      await stub.fetch('https://do/hit', { method: 'POST', body: JSON.stringify({ day, plot, ref, vh, country }) });
      return new Response('ok', { headers: h });
    }
    if (req.method === 'GET' && url.pathname === '/stats') {
      if (!env.STATS_KEY || url.searchParams.get('key') !== env.STATS_KEY) return new Response('forbidden', { status: 403 });
      const r = await stub.fetch('https://do/stats'); return new Response(await r.text(), { headers: { 'Content-Type': 'application/json' } });
    }
    return new Response('plotline counter', { headers: h });
  }
};

export class Counter {
  constructor(state) { this.sql = state.storage.sql;
    this.sql.exec(`CREATE TABLE IF NOT EXISTS hits (day TEXT, plot TEXT, ref TEXT, views INTEGER, PRIMARY KEY (day, plot, ref));
      CREATE TABLE IF NOT EXISTS uniq (day TEXT, plot TEXT, vh TEXT, PRIMARY KEY (day, plot, vh));
      CREATE TABLE IF NOT EXISTS countries (day TEXT, plot TEXT, country TEXT, views INTEGER, PRIMARY KEY (day, plot, country));`); }
  async fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === '/hit') {
      const { day, plot, ref, vh, country } = await req.json();
      this.sql.exec(`INSERT INTO hits (day, plot, ref, views) VALUES (?, ?, ?, 1) ON CONFLICT(day, plot, ref) DO UPDATE SET views = views + 1`, day, plot, ref);
      this.sql.exec(`INSERT OR IGNORE INTO uniq (day, plot, vh) VALUES (?, ?, ?)`, day, plot, vh);
      if (country) this.sql.exec(`INSERT INTO countries (day, plot, country, views) VALUES (?, ?, ?, 1) ON CONFLICT(day, plot, country) DO UPDATE SET views = views + 1`, day, plot, country);
      // uniques older than 90 days are not needed once the daily count is settled; keep the table small
      this.sql.exec(`DELETE FROM uniq WHERE day < date('now', '-90 days')`);
      return new Response('ok');
    }
    if (url.pathname === '/stats') {
      const totals = this.sql.exec(`SELECT plot, SUM(views) AS views FROM hits GROUP BY plot ORDER BY views DESC`).toArray();
      const daily = this.sql.exec(`SELECT h.day, h.plot, SUM(h.views) AS views, (SELECT COUNT(*) FROM uniq u WHERE u.day = h.day AND u.plot = h.plot) AS visitors FROM hits h WHERE h.day >= date('now', '-90 days') GROUP BY h.day, h.plot ORDER BY h.day DESC, views DESC`).toArray();
      const refs = this.sql.exec(`SELECT plot, ref, SUM(views) AS views FROM hits GROUP BY plot, ref ORDER BY views DESC LIMIT 100`).toArray();
      const countries = this.sql.exec(`SELECT plot, country, SUM(views) AS views FROM countries GROUP BY plot, country ORDER BY views DESC LIMIT 100`).toArray();
      return new Response(JSON.stringify({ generated: new Date().toISOString(), totals, daily, referrers: refs, countries }, null, 1), { headers: { 'Content-Type': 'application/json' } });
    }
    return new Response('?', { status: 404 });
  }
}
