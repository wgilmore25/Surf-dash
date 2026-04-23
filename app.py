"""
Surf Dash — Command Center
Run with: streamlit run app.py
"""

import streamlit as st
import streamlit_authenticator as stauth
import psycopg2, psycopg2.extras, json, os
from datetime import date, datetime

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Surf Dash",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --rb-navy: #0f172a;
    --rb-navy-2: #16213e;
    --rb-red: #db0835;
    --rb-red-dark: #b0062a;
    --rb-silver: #e5e7eb;
    --rb-slate: #64748b;
    --rb-surface: #f8fafc;
    --rb-border: #dbe3ee;
    --rb-gold: #d4a017;
    --rb-green: #15803d;
    --rb-amber: #b45309;
}

.stApp {
    background: linear-gradient(180deg, #f6f8fb 0%, #eef3f8 100%);
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--rb-navy) 0%, #121d34 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    color: #edf2f7 !important;
}

h1, h2, h3 {
    color: var(--rb-navy);
    letter-spacing: -0.02em;
}

.section-title {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--rb-slate);
    margin: 0 0 0.4rem 0;
}

.overview-shell {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(219, 227, 238, 0.9);
    border-radius: 18px;
    padding: 1rem 1.1rem 1.15rem 1.1rem;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
    backdrop-filter: blur(8px);
    margin-bottom: 1rem;
}

.athlete-header {
    background:
        linear-gradient(110deg, rgba(219, 8, 53, 0.18), rgba(219, 8, 53, 0.02) 35%),
        linear-gradient(135deg, var(--rb-navy) 0%, var(--rb-navy-2) 100%);
    color: white;
    padding: 24px 26px;
    border-radius: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 16px 34px rgba(15, 23, 42, 0.24);
}
.athlete-header h2 {
    color: white;
    margin: 0;
    font-weight: 800;
    letter-spacing: -0.03em;
}
.athlete-header p {
    color: #cbd5e1;
    margin: 8px 0 0 0;
    font-size: 0.96em;
}

.rb-badge {
    display: inline-block;
    background: linear-gradient(180deg, var(--rb-red) 0%, var(--rb-red-dark) 100%);
    color: white !important;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-left: 10px;
    vertical-align: middle;
    box-shadow: 0 6px 18px rgba(219, 8, 53, 0.28);
}

.metric-card {
    background: rgba(255,255,255,0.8);
    border: 1px solid var(--rb-border);
    border-radius: 16px;
    padding: 12px 16px;
    border-left: 4px solid var(--rb-red);
    margin-bottom: 8px;
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.86);
    border: 1px solid var(--rb-border);
    border-radius: 16px;
    padding: 14px 16px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}
[data-testid="metric-container"] label {
    color: var(--rb-slate) !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 0.7rem !important;
}
/* Metric values — target every possible inner element */
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: var(--rb-navy) !important;
}
/* Keep delta green/red */
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    color: inherit !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--rb-border);
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.55);
    border-radius: 12px 12px 0 0;
    padding: 10px 14px;
    border: 1px solid transparent;
}
/* All tab labels: readable slate */
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div {
    color: var(--rb-slate) !important;
    font-weight: 600;
}
/* Selected tab: bold navy */
.stTabs [aria-selected="true"] {
    background: white !important;
    border-color: var(--rb-border) !important;
    border-bottom-color: white !important;
    font-weight: 700;
}
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div {
    color: var(--rb-navy) !important;
    font-weight: 700 !important;
}

/* Main area buttons */
.stButton > button, .stDownloadButton > button {
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid var(--rb-border);
    box-shadow: none;
}
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
    background: linear-gradient(180deg, var(--rb-red) 0%, var(--rb-red-dark) 100%);
    color: white !important;
    border-color: transparent;
}
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.76);
    color: var(--rb-navy) !important;
}

/* Sidebar buttons: dark background theme so text must be light */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: #edf2f7 !important;
    border-color: rgba(255,255,255,0.12) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(180deg, var(--rb-red) 0%, var(--rb-red-dark) 100%) !important;
    color: white !important;
    border-color: transparent !important;
}
[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] .stButton > button span,
[data-testid="stSidebar"] .stButton > button div {
    color: inherit !important;
}

[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid var(--rb-border) !important;
    border-radius: 12px !important;
}

/* Expander header row — always white bg, dark text */
[data-testid="stExpander"] > details > summary {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
}

[data-testid="stExpander"] > details[open] > summary {
    border-radius: 12px 12px 0 0 !important;
    border-bottom: 1px solid var(--rb-border) !important;
}

/* All text inside expanders — force dark */
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] details * {
    color: var(--rb-navy) !important;
    background-color: transparent !important;
}

/* Form inputs inside expanders */
[data-testid="stExpander"] input,
[data-testid="stExpander"] textarea,
[data-testid="stExpander"] select,
[data-testid="stExpander"] [data-baseweb="input"] input,
[data-testid="stExpander"] [data-baseweb="select"] div {
    background: #f8fafc !important;
    color: var(--rb-navy) !important;
    border: 1px solid #cbd5e1 !important;
}

/* Placeholder text readable */
[data-testid="stExpander"] input::placeholder,
[data-testid="stExpander"] textarea::placeholder {
    color: #94a3b8 !important;
}

/* Labels above inputs */
[data-testid="stExpander"] label,
[data-testid="stExpander"] .stTextInput label,
[data-testid="stExpander"] .stSelectbox label,
[data-testid="stExpander"] .stDateInput label,
[data-testid="stExpander"] .stNumberInput label {
    color: var(--rb-navy) !important;
    font-weight: 600 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--rb-border);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

table thead th {
    background: var(--rb-navy) !important;
    color: white !important;
}

div[data-baseweb="select"] > div,
.stTextInput input,
.stTextArea textarea,
.stDateInput input,
.stNumberInput input {
    border-radius: 12px !important;
    border: 1px solid var(--rb-border) !important;
    background: rgba(255,255,255,0.9) !important;
}

small.kicker {
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-weight: 700;
}

/* ── Force dark text in main content (prevents washed-out text) ─────────── */
section[data-testid="stMain"] label,
section[data-testid="stMain"] li,
section[data-testid="stMain"] .stMarkdown:not(.athlete-header):not(.athlete-header *),
.stText > div,
div[data-testid="stText"] {
    color: var(--rb-navy) !important;
}

/* Metric values stay navy, deltas keep their green/red */
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--rb-navy) !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    /* keep default streamlit green/red for delta */
}

/* Tab labels */
.stTabs [data-baseweb="tab"] span {
    color: var(--rb-navy) !important;
}

/* Dataframe text */
[data-testid="stDataFrame"] * {
    color: var(--rb-navy) !important;
}
[data-testid="stDataFrame"] thead th {
    color: white !important;
}

/* Write / st.write text */
.stText > div,
div[data-testid="stText"] {
    color: var(--rb-navy) !important;
}


.status-good  { color: var(--rb-green); font-weight: 700; }
.status-watch { color: var(--rb-red);   font-weight: 700; }
.status-stable{ color: var(--rb-amber); font-weight: 700; }

.command-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin: 0 0 1rem 0;
}
.command-card {
    background: rgba(255,255,255,0.88);
    border: 1px solid var(--rb-border);
    border-radius: 16px;
    padding: 14px 16px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}
.command-label {
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--rb-slate);
    margin-bottom: 6px;
}
.command-value {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--rb-navy);
}
.command-sub {
    font-size: 0.82rem;
    color: var(--rb-slate);
    margin-top: 4px;
}
.group-shell {
    margin: 1rem 0 1.2rem 0;
}
.command-header-row {
    display: grid;
    grid-template-columns: 2.2fr 0.9fr 0.9fr 1fr 1fr 1fr;
    gap: 12px;
    padding: 0 14px 8px 14px;
    color: var(--rb-slate);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.command-row {
    display: grid;
    grid-template-columns: 2.2fr 0.9fr 0.9fr 1fr 1fr 1fr;
    gap: 12px;
    align-items: center;
    background: rgba(255,255,255,0.86);
    border: 1px solid var(--rb-border);
    border-radius: 14px;
    padding: 12px 14px;
    margin-bottom: 10px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}
.command-name {
    font-weight: 800;
    color: var(--rb-navy);
    margin-bottom: 2px;
}
.command-subtext {
    font-size: 0.82rem;
    color: var(--rb-slate);
}
.status-pill {
    display: inline-block;
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: 1px solid currentColor;
}
.overview-button button {
    width: 100%;
    min-height: 56px;
}

</style>
""", unsafe_allow_html=True)

# ── Database ──────────────────────────────────────────────────────────────────
class _DbWrapper:
    """Thin wrapper so psycopg2 behaves like sqlite3 (con.execute returns cursor)."""
    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, params=None):
        cur = self._conn.cursor()
        cur.execute(sql, params or ())
        return cur

    def cursor(self):
        return self._conn.cursor()

    def executemany(self, sql, seq):
        cur = self._conn.cursor()
        cur.executemany(sql, seq)
        return cur

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()

def get_db():
    """Return a wrapped psycopg2 connection."""
    url = st.secrets["database_url"]
    # Supabase requires SSL and a connect timeout
    if "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url += f"{sep}sslmode=require"
    try:
        conn = psycopg2.connect(url, connect_timeout=15)
        return _DbWrapper(conn)
    except Exception as e:
        host = url.split("@")[1].split("/")[0] if "@" in url else "unknown"
        st.error(f"**Database connection error:** `{e}`\n\n**Host attempted:** `{host}`")
        raise

def init_db():
    """Ensure all tables exist (safe to run on every startup)."""
    con = get_db()
    cur = con.cursor()
    statements = [
        """CREATE TABLE IF NOT EXISTS athletes (
            id SERIAL PRIMARY KEY,
            sheet_key TEXT UNIQUE,
            name TEXT, country TEXT, discipline TEXT, tour TEXT,
            ranking_season TEXT, current_ranking TEXT,
            stance TEXT, home_break TEXT, known_for TEXT, notes TEXT,
            photo_url TEXT DEFAULT '', gender TEXT DEFAULT 'Men'
        )""",
        """CREATE TABLE IF NOT EXISTS sponsors (
            id SERIAL PRIMARY KEY,
            athlete_id INTEGER REFERENCES athletes(id),
            name TEXT, type TEXT, since TEXT, notes TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS injuries (
            id SERIAL PRIMARY KEY,
            athlete_id INTEGER REFERENCES athletes(id),
            inj_date TEXT, type TEXT, body_part TEXT, severity TEXT,
            return_date TEXT, notes TEXT, active INTEGER DEFAULT 1,
            logged_by TEXT DEFAULT '', logged_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS comp_results (
            id SERIAL PRIMARY KEY,
            athlete_id INTEGER REFERENCES athletes(id),
            season TEXT, event TEXT, tour TEXT, event_date TEXT,
            location TEXT, round TEXT, place INTEGER, points REAL,
            heat_score TEXT, notes TEXT, source_url TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS ranking_history (
            id SERIAL PRIMARY KEY,
            athlete_id INTEGER REFERENCES athletes(id),
            season TEXT, tour TEXT, as_of TEXT,
            ranking INTEGER, points REAL, notes TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS physical_testing (
            id SERIAL PRIMARY KEY,
            athlete_id INTEGER REFERENCES athletes(id),
            test_date TEXT, test_type TEXT, metric TEXT,
            value TEXT, unit TEXT, notes TEXT,
            logged_by TEXT DEFAULT '', logged_at TIMESTAMP DEFAULT NOW()
        )""",
    ]
    for stmt in statements:
        cur.execute(stmt)
    con.commit()
    con.close()

def seed_from_json():
    """No-op: data lives in Supabase."""
    return

def _seed_legacy():
    """Legacy seeder — kept for reference only, not called."""
    con = get_db()
    cur = con.cursor()
    if cur.execute("SELECT COUNT(*) FROM athletes").fetchone()[0] > 0:
        con.close()
        return
    con.close()
    return
    with open("athlete_data.json") as f:
        data = json.load(f)
    for sheet, d in data.items():
        cur.execute("""INSERT INTO athletes
            (sheet_key,name,country,discipline,tour,ranking_season,
             current_ranking,stance,home_break,known_for,notes)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (sheet_key) DO NOTHING""",
            (sheet, d["name"], d.get("country",""), d.get("discipline",""),
             d.get("tour",""), d.get("ranking_season",""),
             d.get("current_ranking",""), d.get("stance",""),
             d.get("home_break",""), d.get("known_for",""), d.get("notes","")))
        aid = cur.execute("SELECT id FROM athletes WHERE sheet_key=%s", (sheet,)).fetchone()[0]
        for s in d.get("sponsors", []):
            cur.execute("INSERT INTO sponsors (athlete_id,name,type,since,notes) VALUES (%s,%s,%s,%s,%s)",
                (aid, s["name"], s["type"], s["since"], s["notes"]))
        for inj in d.get("injuries", []):
            cur.execute("INSERT INTO injuries (athlete_id,inj_date,type,body_part,severity,return_date,notes) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (aid, inj["date"], inj["type"], inj["body_part"], inj["severity"], inj["return_date"], inj["notes"]))
        for r in d.get("comp_results", []):
            place = r["place"]
            try: place = int(place)
            except: pass
            points = r["points"]
            try: points = float(points)
            except: points = None
            cur.execute("INSERT INTO comp_results (athlete_id,season,event,tour,event_date,location,round,place,points,notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (aid, r["season"], r["event"], r["tour"], r["date"], r["location"], r["round"], place, points, r["notes"]))
        for rh in d.get("ranking_history", []):
            rank = rh["rank"]
            try: rank = int(rank)
            except: rank = None
            pts = rh["points"]
            try: pts = float(pts)
            except: pts = None
            cur.execute("INSERT INTO ranking_history (athlete_id,season,tour,as_of,ranking,points,notes) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (aid, rh["season"], rh["tour"], rh["as_of"], rank, pts, rh["notes"]))
    con.commit()
    con.close()

# ── Helpers ───────────────────────────────────────────────────────────────────
def tour_color(tour: str) -> str:
    t = tour.upper()
    if "CT" in t:   return "#e8003d"
    if "CS" in t or "CHALLENGER" in t: return "#0077b6"
    if "BIG" in t:  return "#2d6a4f"
    return "#7209b7"

def status_tier(rank_delta_num=None, recent_avg=None, has_injury=False):
    if has_injury:
        return "WATCH", "status-watch"
    if rank_delta_num is not None and rank_delta_num >= 2 and (recent_avg is None or recent_avg <= 8):
        return "RISING", "status-good"
    if rank_delta_num is not None and rank_delta_num <= -2 and (recent_avg is None or recent_avg >= 12):
        return "WATCH", "status-watch"
    if recent_avg is not None and recent_avg <= 8:
        return "STRONG", "status-good"
    if recent_avg is not None and recent_avg >= 12:
        return "WATCH", "status-watch"
    return "STABLE", "status-stable"

def status_pill(label, css_class):
    return f'<span class="status-pill {css_class}">{label}</span>'

def get_athletes():
    con = get_db()
    rows = con.execute("""
        SELECT a.id, a.name, a.country, a.discipline, a.tour,
               a.current_ranking, a.stance, a.home_break,
               COALESCE(MAX(CASE WHEN i.active=1 THEN 1 ELSE 0 END),0) as has_injury,
               COUNT(DISTINCT cr.id) as num_results,
               MAX(rh.ranking) as latest_rank,
               MIN(rh.ranking) as best_rank,
               MAX(CASE WHEN rh.as_of = (SELECT MAX(as_of) FROM ranking_history rh2 WHERE rh2.athlete_id=a.id) THEN rh.ranking END) as current_rank
        FROM athletes a
        LEFT JOIN injuries i ON i.athlete_id=a.id
        LEFT JOIN comp_results cr ON cr.athlete_id=a.id
        LEFT JOIN ranking_history rh ON rh.athlete_id=a.id
        GROUP BY a.id ORDER BY
            CASE WHEN a.tour LIKE '%CT%' THEN 0 WHEN a.tour LIKE '%Challenger%' OR a.tour LIKE '%CS%' THEN 1 ELSE 2 END,
            a.name
    """).fetchall()
    con.close()
    return rows

def get_athlete(aid):
    con = get_db()
    row = con.execute("SELECT * FROM athletes WHERE id=%s", (aid,)).fetchone()
    con.close()
    return row

def get_sponsors(aid):
    con = get_db()
    rows = con.execute("SELECT * FROM sponsors WHERE athlete_id=%s ORDER BY type, since", (aid,)).fetchall()
    con.close()
    return rows

def get_injuries(aid):
    con = get_db()
    rows = con.execute("SELECT * FROM injuries WHERE athlete_id=%s ORDER BY inj_date DESC", (aid,)).fetchall()
    con.close()
    return rows

def get_results(aid):
    con = get_db()
    rows = con.execute("SELECT * FROM comp_results WHERE athlete_id=%s ORDER BY season DESC, event_date DESC", (aid,)).fetchall()
    con.close()
    return rows

def get_rankings(aid):
    con = get_db()
    rows = con.execute("SELECT * FROM ranking_history WHERE athlete_id=%s ORDER BY season DESC, as_of DESC", (aid,)).fetchall()
    con.close()
    return rows

def get_physical(aid):
    con = get_db()
    rows = con.execute("SELECT * FROM physical_testing WHERE athlete_id=%s ORDER BY test_date DESC", (aid,)).fetchall()
    con.close()
    return rows

# ── Pages ─────────────────────────────────────────────────────────────────────

def page_overview():
    import pandas as pd

    st.markdown("<small class='kicker'>High Performance Monitoring</small>", unsafe_allow_html=True)
    st.markdown("## Surf Dash Command Center")
    st.markdown("<div class='overview-shell'>Competition monitoring centered on rank, trajectory, and event outcomes across the full surf roster.</div>", unsafe_allow_html=True)

    athletes = get_athletes()
    if not athletes:
        st.info("No athletes loaded yet.")
        return

    ct_athletes  = [a for a in athletes if "CT" in (a[4] or "").upper()]
    cs_athletes  = [a for a in athletes if any(x in (a[4] or "").upper() for x in ["CHALLENGER", "CS"])]
    other        = [a for a in athletes if a not in ct_athletes and a not in cs_athletes]

    watch_count = 0
    ranks_available = 0
    events_logged = 0

    athlete_summaries = {}
    for a in athletes:
        aid, name, country, disc, tour, ranking, stance, home, has_injury, num_results, latest_rank, best_rank, current_rank = a
        results  = get_results(aid)
        rankings = get_rankings(aid)
        valid_rankings = [r for r in rankings if isinstance(r[5], int)]
        # Exclude place=0 (in-progress placeholder)
        valid_places = [r[8] for r in results if isinstance(r[8], int) and r[8] > 0]
        last_result  = f"P{valid_places[0]}" if valid_places else "—"
        season_best  = f"P{min(valid_places)}" if valid_places else "—"
        rank_delta = "—"
        rank_delta_num = None
        # Only use numerical rank — never fall back to text notes
        num_rank = current_rank if isinstance(current_rank, int) else None
        if not num_rank and valid_rankings:
            num_rank = valid_rankings[0][5]
        rank_display = f"#{num_rank}" if num_rank else "—"
        if valid_rankings:
            ranks_available += 1
            if len(valid_rankings) > 1:
                rank_delta_num = valid_rankings[1][5] - valid_rankings[0][5]
                rank_delta = f"{rank_delta_num:+d}"
        recent_places = valid_places[:3]
        recent_avg = sum(recent_places) / len(recent_places) if recent_places else None
        status_label, status_class = status_tier(rank_delta_num, recent_avg, bool(has_injury))
        if status_label == "WATCH":
            watch_count += 1
        events_logged += len(valid_places)
        athlete_summaries[aid] = {
            "current_rank": rank_display,
            "rank_delta":   rank_delta,
            "last_result":  last_result,
            "season_best":  season_best,
            "status_label": status_label,
            "status_class": status_class,
        }

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Athletes",  len(athletes),    help="Full roster loaded in the system")
    k2.metric("Ranks Available", ranks_available,  help="Athletes with 2026 ranking history")
    k3.metric("Results Logged",  events_logged,    help="Competition results on file")
    k4.metric("Watch List",      watch_count,      help="Athletes flagged for attention — injury, dropping rank, or poor recent results")

    # ── Watch List expandable ─────────────────────────────────────────────────
    watch_athletes = [(aid, s) for aid, s in athlete_summaries.items() if s["status_label"] == "WATCH"]
    if watch_athletes:
        with st.expander(f"⚠ Watch List — {watch_count} athlete{'s' if watch_count != 1 else ''} flagged", expanded=False):
            reason_map = {
                "injury":       "Active injury",
                "rank_drop":    "Rank dropping",
                "poor_results": "Poor recent results",
            }
            for aid_w, s_w in watch_athletes:
                a_match = next((a for a in athletes if a[0] == aid_w), None)
                if not a_match:
                    continue
                aname   = a_match[1]
                acountry= a_match[2]
                # Determine reason
                results_w  = get_results(aid_w)
                rankings_w = get_rankings(aid_w)
                valid_r    = [r for r in rankings_w if isinstance(r[5], int)]
                has_inj    = bool(a_match[8])
                rank_delta_w = None
                if len(valid_r) > 1:
                    rank_delta_w = valid_r[1][5] - valid_r[0][5]
                valid_pl_w = [r[8] for r in results_w if isinstance(r[8], int) and r[8] > 0]
                recent_avg_w = sum(valid_pl_w[:3]) / len(valid_pl_w[:3]) if valid_pl_w else None

                if has_inj:
                    reason = "Active injury"
                elif rank_delta_w is not None and rank_delta_w <= -2:
                    reason = f"Rank dropping ({rank_delta_w:+d} positions)"
                elif recent_avg_w is not None and recent_avg_w >= 12:
                    reason = f"Recent avg finish: P{recent_avg_w:.0f}"
                else:
                    reason = "Flagged for review"

                wc1, wc2, wc3, wc4 = st.columns([2, 1, 1.5, 2])
                wc1.markdown(f"**{aname}**")
                wc2.markdown(f"{acountry}")
                wc3.markdown(f"{s_w['current_rank']}")
                wc4.markdown(f"<span style='color:#db0835;font-size:0.85rem'>{reason}</span>", unsafe_allow_html=True)
            st.markdown("")

    # ── CT Season Standings: Men + Women separately ───────────────────────────
    con = get_db()
    ev_rows = con.execute("""
        SELECT DISTINCT event, MIN(event_date) as dt FROM comp_results
        WHERE season='2026' AND event != '' GROUP BY event ORDER BY dt
    """).fetchall()
    ev_labels = {}
    for ev, dt in ev_rows:
        short = (ev.replace("Rip Curl Pro ", "")
                   .replace("Western Australia ", "WA ")
                   .replace(" Presented By Bonsoy", ""))
        ev_labels[ev] = short

    def build_standings(gender_val, title):
        rows = con.execute("""
            SELECT a.id, a.name, a.country,
                   rh.ranking, rh.points,
                   STRING_AGG(cr.event || '::' || CAST(cr.points AS TEXT), '|||') as evt_pts
            FROM athletes a
            LEFT JOIN ranking_history rh ON rh.athlete_id=a.id AND rh.season='2026'
            LEFT JOIN comp_results cr ON cr.athlete_id=a.id AND cr.season='2026'
            WHERE a.tour LIKE '%CT%' AND a.gender=%s
            GROUP BY a.id
            ORDER BY rh.ranking ASC NULLS LAST, a.name ASC
        """, (gender_val,)).fetchall()
        if not rows:
            return
        st.markdown(f"<div class='section-title' style='color:#e8003d;margin-top:0.8rem'>{title}</div>", unsafe_allow_html=True)
        table_data = []
        for row in rows:
            _, aname, country, rank, total_pts, evt_pts_str = row
            entry = {
                "Rank":      f"#{rank}" if rank else "—",
                "Athlete":   aname,
                "Country":   country or "",
                "Total Pts": int(total_pts) if total_pts else "—",
            }
            seen_events = set()
            if evt_pts_str:
                for chunk in evt_pts_str.split("|||"):
                    parts = chunk.split("::")
                    if len(parts) == 2:
                        ev_name, pts = parts
                        short = ev_labels.get(ev_name, ev_name[:18])
                        if short not in seen_events:
                            seen_events.add(short)
                            entry[short] = int(float(pts)) if pts and pts not in ("None", "") else "—"
            # Fill missing event columns with "—"
            for ev_short in ev_labels.values():
                if ev_short not in entry:
                    entry[ev_short] = "—"
            table_data.append(entry)
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    build_standings("Men",   "2026 Men's CT Season Standings")
    build_standings("Women", "2026 Women's CT Season Standings")
    con.close()
    st.markdown("---")

    # ── Athlete Groups ────────────────────────────────────────────────────────
    def render_group(title, group, color):
        if not group:
            return
        st.markdown(
            f"<div class='group-shell'>"
            f"<div class='section-title' style='color:{color}'>{title}</div>"
            f"<div class='command-header-row'>"
            f"<div>Athlete</div><div>Rank</div><div>Δ Rank</div>"
            f"<div>Last Result</div><div>Season Best</div><div>Status</div>"
            f"</div></div>",
            unsafe_allow_html=True
        )
        for a in group:
            aid, name, country, disc, tour, ranking, stance, home, has_injury, num_results, latest_rank, best_rank, current_rank = a
            s = athlete_summaries[aid]
            col1, col2, col3, col4, col5, col6 = st.columns([2.2, 0.8, 0.8, 1, 1, 1.1])
            with col1:
                if st.button(name, key=f"ov_{aid}", use_container_width=True):
                    st.session_state.page = "athlete"
                    st.session_state.athlete_id = aid
                    st.rerun()
            col2.markdown(f"<div style='padding-top:8px;font-weight:700;color:#0f172a'>{s['current_rank']}</div>", unsafe_allow_html=True)
            col3.markdown(f"<div style='padding-top:8px;font-weight:600;color:#64748b'>{s['rank_delta']}</div>", unsafe_allow_html=True)
            col4.markdown(f"<div style='padding-top:8px;font-weight:600;color:#0f172a'>{s['last_result']}</div>", unsafe_allow_html=True)
            col5.markdown(f"<div style='padding-top:8px;font-weight:600;color:#0f172a'>{s['season_best']}</div>", unsafe_allow_html=True)
            col6.markdown(f"<div style='padding-top:6px'>{status_pill(s['status_label'], s['status_class'])}</div>", unsafe_allow_html=True)

    render_group("Championship Tour", ct_athletes, "#e8003d")
    render_group("Challenger Series", cs_athletes, "#0077b6")
    render_group("Big Wave and Free Surf", other, "#2d6a4f")


def page_athlete(aid):
    a = get_athlete(aid)
    if not a:
        st.error("Athlete not found.")
        return

    # columns: id,sheet_key,name,country,discipline,tour,ranking_season,current_ranking,stance,home_break,known_for,notes,photo_url[,gender]
    _, sheet, name, country, discipline, tour, ranking_season, current_ranking, stance, home_break, known_for, notes, photo_url = a[:13]

    tc = tour_color(tour or "")
    st.markdown(f"""
    <div class="athlete-header" style="color: white !important;">
        <h2 style="color: white !important; margin: 0; font-weight: 800; letter-spacing: -0.03em;">{name} <span style="display: inline-block; background: linear-gradient(180deg, #db0835 0%, #b0062a 100%); color: white !important; padding: 4px 10px; border-radius: 999px; font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-left: 10px; vertical-align: middle; box-shadow: 0 6px 18px rgba(219,8,53,0.28);">RED BULL</span></h2>
        <p style="color: #cbd5e1 !important; margin: 8px 0 0 0; font-size: 0.96em;">{country} &nbsp;·&nbsp; <span style="color:{tc} !important; font-weight:600;">{tour}</span> &nbsp;·&nbsp; <span style="color: #cbd5e1 !important;">{current_ranking}</span></p>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats row
    sponsors = get_sponsors(aid)
    injuries = get_injuries(aid)
    results  = get_results(aid)
    rankings = get_rankings(aid)
    physical = get_physical(aid)

    valid_rankings = [r for r in rankings if isinstance(r[5], int)]
    current_rank_num  = valid_rankings[0][5] if valid_rankings else None
    previous_rank_num = valid_rankings[1][5] if len(valid_rankings) > 1 else None
    rank_delta_num    = (previous_rank_num - current_rank_num) if current_rank_num is not None and previous_rank_num is not None else None

    valid_places   = [r[8] for r in results if isinstance(r[8], int)]
    last_place     = next((r[8] for r in results if isinstance(r[8], int)), None)
    season_best_pl = min(valid_places) if valid_places else None
    avg_finish     = round(sum(valid_places)/len(valid_places), 1) if valid_places else None

    recent_places = [r[8] for r in results[:3] if isinstance(r[8], int)]
    recent_avg    = sum(recent_places)/len(recent_places) if recent_places else None
    status_label, _ = status_tier(rank_delta_num, recent_avg, any(i[8]==1 for i in injuries))

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Country", country or "—")
    c2.metric("Current Rank", f"#{current_rank_num}" if current_rank_num is not None else (current_ranking or "—"),
              delta=f"{rank_delta_num:+d}" if rank_delta_num is not None else None)
    c3.metric("Last Result", f"P{last_place}" if last_place is not None else "—")
    c4.metric("Season Best", f"P{season_best_pl}" if season_best_pl is not None else "—")
    c5.metric("Avg Finish",  str(avg_finish) if avg_finish is not None else "—")
    c6.metric("Status", status_label)

    tab_profile, tab_results, tab_rankings, tab_injuries, tab_physical, tab_sponsors, tab_edit = st.tabs([
        "Profile", "Results", "Rankings", "Injuries",
        "Physical Testing", "Sponsors", "Edit Profile"
    ])

    # ── Profile ──────────────────────────────────────────────────────────────
    with tab_profile:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Country**")
            st.write(country or "—")
            st.markdown("**Home Break / Region**")
            st.write(home_break or "—")
            st.markdown("**Known For**")
            st.write(known_for or "—")
        with col2:
            st.markdown("**Tour / Discipline**")
            st.write(f"{tour or '—'} · {discipline or '—'}")
            st.markdown("**Scouting Notes**")
            st.write(notes or "—")
        if rankings:
            r = rankings[0]
            st.markdown("---")
            try:
                st.markdown(f"**Latest Ranking:** #{r[4]} on {r[2]} ({r[5]:,} pts)" if r[4] and r[5] else f"**Latest Ranking:** {current_ranking}")
            except Exception:
                st.markdown(f"**Latest Ranking:** {current_ranking}")

    # ── Competition Results ───────────────────────────────────────────────────
    with tab_results:
        if results:
            import pandas as pd
            df = pd.DataFrame(results, columns=["id","athlete_id","season","event","tour","date","location","round","place","points","heat_score","notes","source_url"])
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            # ── 2026 Season Event-by-Event Summary ────────────────────────────
            season_df = df[df["season"] == "2026"].copy()
            if not season_df.empty:
                st.markdown("<div class='section-title'>2026 Season — Event Points</div>", unsafe_allow_html=True)

                # Season rank & total from ranking_history
                season_rank = season_total = None
                if rankings:
                    rdf = pd.DataFrame(rankings, columns=["id","athlete_id","season","tour","as_of","rank","points","notes"])
                    rdf_2026 = rdf[rdf["season"] == "2026"].copy()
                    if not rdf_2026.empty:
                        latest = rdf_2026.sort_values("as_of", ascending=False).iloc[0]
                        season_rank  = int(latest["rank"])   if pd.notna(latest["rank"])   else None
                        season_total = int(latest["points"]) if pd.notna(latest["points"]) else None

                pivot_rows = []
                for _, row in season_df.sort_values("date").iterrows():
                    ev_label = (str(row["event"])
                                .replace("Rip Curl Pro ", "")
                                .replace("Western Australia ", "WA ")
                                .replace(" Presented By Bonsoy", ""))
                    place_val = row["place"]
                    try: place_val = int(place_val)
                    except: pass
                    pts_val = row["points"]
                    try: pts_val = int(float(pts_val))
                    except: pts_val = 0
                    pivot_rows.append({
                        "Event":         ev_label,
                        "Date":          row["date"].strftime("%Y-%m-%d") if pd.notna(row["date"]) else "",
                        "Location":      row["location"] or "",
                        "Round Reached": row["round"] or "",
                        "Place":         place_val,
                        "Points":        pts_val,
                    })

                pivot_df = pd.DataFrame(pivot_rows)
                col_cfg = {
                    "Points": st.column_config.NumberColumn("Points", format="%d"),
                    "Place":  st.column_config.NumberColumn("Place",  format="%d"),
                }
                st.dataframe(pivot_df, use_container_width=True, hide_index=True, column_config=col_cfg)

                total_pts = int(season_df["points"].fillna(0).sum())
                st.markdown("---")
                sm1, sm2, sm3 = st.columns(3)
                sm1.metric("Season Rank",       f"#{season_rank}"           if season_rank  else "—")
                sm2.metric("Total Points",      f"{season_total:,}"         if season_total else f"{total_pts:,}")
                sm3.metric("Events Completed",  len(season_df))
                st.markdown("---")

            # ── Competition Trend Chart ────────────────────────────────────────
            valid_places_df = df.dropna(subset=["place"]).copy()
            if not valid_places_df.empty:
                trend_df = valid_places_df.sort_values("date").copy()
                trend_df["place_display"] = trend_df["place"].astype(float)
                st.markdown("**Competition Trend (Place over Time)**")
                st.line_chart(trend_df.set_index("date")[["place_display"]], use_container_width=True)

                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Events", len(valid_places_df))
                s2.metric("Best Finish",    f"P{int(valid_places_df['place'].min())}")
                s3.metric("Average Finish", f"{valid_places_df['place'].mean():.1f}")
                latest_p = valid_places_df.sort_values("date", ascending=False).iloc[0]["place"]
                s4.metric("Most Recent",    f"P{int(latest_p)}")

            st.dataframe(df[["season","event","tour","date","location","round","place","points","notes"]].rename(columns={
                "season":"Season","event":"Event","tour":"Tour","date":"Date",
                "location":"Location","round":"Round","place":"Place","points":"Points","notes":"Notes"
            }), use_container_width=True, hide_index=True)
        else:
            st.info("No competition results logged yet.")

        with st.expander("Add Competition Result"):
            with st.form(f"add_result_{aid}"):
                rc1, rc2, rc3 = st.columns(3)
                season    = rc1.text_input("Season", value="2026")
                event     = rc2.text_input("Event Name", placeholder="Rip Curl Pro Bells Beach")
                tour_r    = rc3.text_input("Tour", value="Championship Tour")
                rc4, rc5 = st.columns(2)
                ev_date   = rc4.date_input("Event Date", value=date.today())
                location  = rc5.text_input("Location", placeholder="Bells Beach, Australia")
                rc6, rc7, rc8 = st.columns(3)
                round_r   = rc6.text_input("Round", placeholder="Final / Semifinal / etc.")
                place     = rc7.number_input("Place", min_value=1, max_value=50, value=1)
                points    = rc8.number_input("Points", min_value=0.0, value=0.0)
                notes_r   = st.text_input("Notes", placeholder="Optional notes")
                source    = st.text_input("Source URL", placeholder="https://www.worldsurfleague.com/...")
                if st.form_submit_button("Add Result", type="primary"):
                    con = get_db()
                    con.execute("""INSERT INTO comp_results
                        (athlete_id,season,event,tour,event_date,location,round,place,points,notes,source_url)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (sheet_key) DO NOTHING""",
                        (aid, season, event, tour_r, str(ev_date), location, round_r, int(place), float(points), notes_r, source))
                    con.commit(); con.close()
                    st.success("Result added!"); st.rerun()

    # ── Rankings ─────────────────────────────────────────────────────────────
    with tab_rankings:
        if rankings:
            import pandas as pd
            df = pd.DataFrame(rankings, columns=["id","athlete_id","season","tour","as_of","rank","points","notes"])
            df["as_of"] = pd.to_datetime(df["as_of"], errors="coerce")
            valid_rank_df = df.dropna(subset=["rank"]).copy()
            if not valid_rank_df.empty:
                trend_df = valid_rank_df.sort_values("as_of").copy()
                st.markdown("**Ranking Trend**")
                st.line_chart(trend_df.set_index("as_of")[["rank"]], use_container_width=True)

                current_rank_display = int(trend_df.iloc[-1]["rank"])
                best_rank_display    = int(trend_df["rank"].min())
                worst_rank_display   = int(trend_df["rank"].max())
                rank_change_display  = None
                if len(trend_df) > 1:
                    rank_change_display = int(trend_df.iloc[-2]["rank"] - trend_df.iloc[-1]["rank"])

                r1, r2, r3, r4 = st.columns(4)
                r1.metric("Current",   f"#{current_rank_display}", delta=f"{rank_change_display:+d}" if rank_change_display is not None else None)
                r2.metric("Best",      f"#{best_rank_display}")
                r3.metric("Worst",     f"#{worst_rank_display}")
                r4.metric("Snapshots", len(trend_df))

            st.dataframe(df[["season","tour","as_of","rank","points","notes"]].rename(columns={
                "season":"Season","tour":"Tour","as_of":"As Of","rank":"Rank","points":"Points","notes":"Notes"
            }), use_container_width=True, hide_index=True)
        else:
            st.info("No ranking history logged yet.")

        with st.expander("Add Ranking Snapshot"):
            with st.form(f"add_rank_{aid}"):
                r1, r2, r3 = st.columns(3)
                rk_season = r1.text_input("Season", value="2026")
                rk_tour   = r2.text_input("Tour", value="WSL CT")
                rk_asof   = r3.date_input("As Of Date", value=date.today())
                r4, r5    = st.columns(2)
                rk_rank   = r4.number_input("Ranking", min_value=1, max_value=100, value=1)
                rk_pts    = r5.number_input("Points", min_value=0.0, value=0.0)
                rk_notes  = st.text_input("Notes")
                if st.form_submit_button("Add Ranking", type="primary"):
                    con = get_db()
                    con.execute("""INSERT INTO ranking_history
                        (athlete_id,season,tour,as_of,ranking,points,notes)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                        (aid, rk_season, rk_tour, str(rk_asof), int(rk_rank), float(rk_pts), rk_notes))
                    con.commit(); con.close()
                    st.success("Ranking added!"); st.rerun()

    # ── Injuries ─────────────────────────────────────────────────────────────
    with tab_injuries:
        active_inj   = [i for i in injuries if i[8] == 1]
        resolved_inj = [i for i in injuries if i[8] == 0]

        SEV_COLOR = {"High": "#db0835", "Medium": "#b45309", "Low": "#15803d"}

        if active_inj:
            st.markdown("<div class='section-title' style='color:#db0835;margin-bottom:0.5rem'>Active Injuries</div>", unsafe_allow_html=True)
            for inj in active_inj:
                iid, _, inj_date, typ, body, severity, ret, inj_notes, _ = inj[:9]
                inj_logged_by = inj[9] if len(inj) > 9 else ""
                sev_color = SEV_COLOR.get(severity, "#64748b")
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #dbe3ee;border-left:4px solid {sev_color};
                            border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.6rem;">
                    <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
                        <span style="font-weight:700;color:#0f172a;font-size:1rem">{typ} — {body}</span>
                        <span style="background:{sev_color}22;color:{sev_color};font-size:0.75rem;
                                     font-weight:700;padding:2px 10px;border-radius:99px;text-transform:uppercase">{severity}</span>
                    </div>
                    <div style="margin-top:0.4rem;color:#64748b;font-size:0.88rem">
                        📅 <strong style="color:#0f172a">Injured:</strong> {inj_date}
                        &nbsp;·&nbsp; 🏄 <strong style="color:#0f172a">Est. Return:</strong> {ret or "TBD"}
                        {f'&nbsp;·&nbsp; 📝 {inj_notes}' if inj_notes else ''}
                        {f'&nbsp;·&nbsp; 🧑‍⚕️ Logged by {inj_logged_by}' if inj_logged_by else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                btn_c1, btn_c2, _ = st.columns([1.3, 1, 6])
                if btn_c1.button("✓ Resolved", key=f"resolve_{iid}", type="primary"):
                    con = get_db()
                    con.execute("UPDATE injuries SET active=0 WHERE id=%s", (iid,))
                    con.commit(); con.close(); st.rerun()
                if btn_c2.button("🗑 Delete", key=f"del_inj_{iid}"):
                    con = get_db()
                    con.execute("DELETE FROM injuries WHERE id=%s", (iid,))
                    con.commit(); con.close(); st.rerun()
        else:
            st.success("✓ No active injuries")

        if resolved_inj:
            with st.expander(f"View {len(resolved_inj)} resolved injur{'ies' if len(resolved_inj) != 1 else 'y'}"):
                for inj in resolved_inj:
                    iid, _, inj_date, typ, body, severity, ret, inj_notes, _ = inj
                    sev_color = SEV_COLOR.get(severity, "#64748b")
                    ri1, ri2 = st.columns([8, 1])
                    ri1.markdown(f"""
                    <div style="background:#f8fafc;border:1px solid #dbe3ee;border-left:4px solid #94a3b8;
                                border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.4rem;opacity:0.85">
                        <span style="font-weight:600;color:#334155">{typ} — {body}</span>
                        <span style="margin-left:0.8rem;background:{sev_color}22;color:{sev_color};font-size:0.72rem;
                                     font-weight:700;padding:1px 8px;border-radius:99px">{severity}</span>
                        <div style="color:#94a3b8;font-size:0.82rem;margin-top:0.2rem">
                            {inj_date} → {ret or "TBD"}{f'  ·  {inj_notes}' if inj_notes else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if ri2.button("🗑", key=f"del_res_inj_{iid}", help="Delete this record"):
                        con = get_db()
                        con.execute("DELETE FROM injuries WHERE id=%s", (iid,))
                        con.commit(); con.close(); st.rerun()

        st.markdown("---")
        with st.expander("➕ Log New Injury"):
            with st.form(f"add_injury_{aid}"):
                ij1, ij2 = st.columns(2)
                inj_date_inp = ij1.date_input("Date of Injury", value=date.today())
                inj_type     = ij2.selectbox("Type", ["Fracture","Sprain","Strain","Tear","Laceration","Concussion","Surgery","Other"])
                ij3, ij4 = st.columns(2)
                body_part    = ij3.text_input("Body Part", placeholder="Knee, Shoulder, Ankle...")
                severity     = ij4.selectbox("Severity", ["Low","Medium","High"])
                ij5, ij6 = st.columns(2)
                ret_date     = ij5.date_input("Expected Return", value=date.today())
                inj_notes_f  = ij6.text_input("Notes", placeholder="Details, surgery info...")
                if st.form_submit_button("Log Injury", type="primary"):
                    logged_by = st.session_state.get("fullname", st.session_state.get("username", "unknown"))
                    con = get_db()
                    cur = con.cursor()
                    cur.execute("""INSERT INTO injuries
                        (athlete_id,inj_date,type,body_part,severity,return_date,notes,active,logged_by,logged_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,1,%s,NOW())""",
                        (aid, str(inj_date_inp), inj_type, body_part, severity, str(ret_date), inj_notes_f, logged_by))
                    con.commit(); con.close()
                    st.success(f"Injury logged by {logged_by}!"); st.rerun()

    # ── Physical Testing ──────────────────────────────────────────────────────
    with tab_physical:
        import pandas as pd
        if physical:
            st.markdown("<div class='section-title' style='margin-bottom:0.5rem'>Test History</div>", unsafe_allow_html=True)
            for row in physical:
                pid, _, pt_date, pt_type, pt_metric, pt_val, pt_unit, pt_notes = row[:8]
                pt_logged_by = row[8] if len(row) > 8 else ""
                pc1, pc2 = st.columns([8, 1])
                pc1.markdown(f"""
                <div style="background:#fff;border:1px solid #dbe3ee;border-left:4px solid #0f172a;
                            border-radius:12px;padding:0.8rem 1.2rem;margin-bottom:0.5rem;">
                    <div style="display:flex;align-items:center;gap:0.8rem;flex-wrap:wrap;">
                        <span style="font-weight:700;color:#0f172a;font-size:0.95rem">{pt_metric}</span>
                        <span style="font-size:1.1rem;font-weight:800;color:#db0835">{pt_val} <span style="font-size:0.8rem;color:#64748b;font-weight:500">{pt_unit or ''}</span></span>
                        <span style="background:#f1f5f9;color:#334155;font-size:0.75rem;padding:2px 10px;border-radius:99px">{pt_type}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.82rem;margin-top:0.3rem">
                        📅 {pt_date}{f'  ·  {pt_notes}' if pt_notes else ''}{f'  ·  🧑‍⚕️ {pt_logged_by}' if pt_logged_by else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if pc2.button("🗑", key=f"del_pt_{pid}", help="Delete this record"):
                    con = get_db()
                    con.execute("DELETE FROM physical_testing WHERE id=%s", (pid,))
                    con.commit(); con.close(); st.rerun()
        else:
            st.info("No physical testing data logged yet.")

        st.markdown("---")
        with st.expander("➕ Log Physical Test"):
            with st.form(f"add_physical_{aid}"):
                pt1, pt2 = st.columns(2)
                pt_date  = pt1.date_input("Test Date", value=date.today())
                pt_type  = pt2.selectbox("Test Type", [
                    "Strength", "Power", "Endurance", "Flexibility", "Speed",
                    "Agility", "Balance", "Breath Hold", "VO2 Max", "Body Composition", "Other"
                ])
                pt3, pt4, pt5 = st.columns(3)
                pt_metric = pt3.text_input("Metric", placeholder="Bench Press, Sprint 40m...")
                pt_value  = pt4.text_input("Value", placeholder="135")
                pt_unit   = pt5.text_input("Unit", placeholder="kg, sec, %...")
                pt_notes  = st.text_input("Notes", placeholder="Conditions, comparison to last test...")
                if st.form_submit_button("Log Test", type="primary"):
                    logged_by = st.session_state.get("fullname", st.session_state.get("username", "unknown"))
                    con = get_db()
                    cur = con.cursor()
                    cur.execute("""INSERT INTO physical_testing
                        (athlete_id,test_date,test_type,metric,value,unit,notes,logged_by,logged_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())""",
                        (aid, str(pt_date), pt_type, pt_metric, pt_value, pt_unit, pt_notes, logged_by))
                    con.commit(); con.close()
                    st.success(f"Test logged by {logged_by}!"); st.rerun()

    # ── Sponsors ─────────────────────────────────────────────────────────────
    with tab_sponsors:
        if sponsors:
            import pandas as pd
            df = pd.DataFrame(sponsors, columns=["id","athlete_id","name","type","since","notes"])
            st.dataframe(df[["name","type","since","notes"]].rename(columns={
                "name":"Sponsor","type":"Type","since":"Since","notes":"Notes"
            }), use_container_width=True, hide_index=True)
        else:
            st.info("No sponsors logged.")

        with st.expander("Add Sponsor"):
            with st.form(f"add_sponsor_{aid}"):
                sp1, sp2, sp3 = st.columns(3)
                sp_name  = sp1.text_input("Sponsor Name")
                sp_type  = sp2.selectbox("Type", ["Title","Equipment","Apparel","Nutrition","Tech","Media","Other"])
                sp_since = sp3.text_input("Since (year)", placeholder="2022")
                sp_notes = st.text_input("Notes")
                if st.form_submit_button("Add Sponsor", type="primary"):
                    con = get_db()
                    con.execute("INSERT INTO sponsors (athlete_id,name,type,since,notes) VALUES (%s,%s,%s,%s,%s)",
                        (aid, sp_name, sp_type, sp_since, sp_notes))
                    con.commit(); con.close()
                    st.success("Sponsor added!"); st.rerun()

    # ── Edit Profile ──────────────────────────────────────────────────────────
    with tab_edit:
        with st.form(f"edit_profile_{aid}"):
            ep1, ep2 = st.columns(2)
            new_name     = ep1.text_input("Name", value=name)
            new_country  = ep2.text_input("Country", value=country or "")
            ep3, ep4 = st.columns(2)
            new_disc     = ep3.selectbox("Discipline", ["CT","Challenger","Big Wave","Free Surf","Junior","Other"],
                           index=["CT","Challenger","Big Wave","Free Surf","Junior","Other"].index(discipline) if discipline in ["CT","Challenger","Big Wave","Free Surf","Junior","Other"] else 0)
            new_tour     = ep4.text_input("Primary Tour", value=tour or "")
            ep5, ep6 = st.columns(2)
            new_stance   = ep5.selectbox("Stance", ["Regular","Goofy","—"],
                           index=["Regular","Goofy","—"].index(stance) if stance in ["Regular","Goofy","—"] else 2)
            new_ranking  = ep6.text_input("Current Ranking Note", value=current_ranking or "")
            new_home     = st.text_input("Home Break / Region", value=home_break or "")
            new_known    = st.text_area("Known For", value=known_for or "", height=80)
            new_notes    = st.text_area("Scouting Notes", value=notes or "", height=100)
            if st.form_submit_button("Save Profile", type="primary"):
                con = get_db()
                con.execute("""UPDATE athletes SET name=%s,country=%s,discipline=%s,tour=%s,stance=%s,
                    current_ranking=%s,home_break=%s,known_for=%s,notes=%s WHERE id=%s""",
                    (new_name, new_country, new_disc, new_tour, new_stance,
                     new_ranking, new_home, new_known, new_notes, aid))
                con.commit(); con.close()
                st.success("Profile saved!"); st.rerun()


# ── WSL Sync Page ─────────────────────────────────────────────────────────────
def page_sync():
    import pandas as pd

    st.markdown("<small class='kicker'>Data Management</small>", unsafe_allow_html=True)
    st.markdown("## Sync WSL Rankings")
    st.markdown("""<div class='overview-shell'>
    Paste data from <strong>worldsurfleague.com</strong> to update athlete standings and event results.
    Go to the WSL rankings page, copy the athlete rows, and paste below.
    </div>""", unsafe_allow_html=True)

    def match_athlete(name_val, all_athletes):
        """Fuzzy-match a WSL name to a DB athlete."""
        name_lower = name_val.lower().strip()
        # Exact match first
        for aid, aname in all_athletes:
            if aname.lower() == name_lower:
                return aid, aname
        # Partial match — WSL name contained in DB name or vice versa
        for aid, aname in all_athletes:
            if name_lower in aname.lower() or aname.lower() in name_lower:
                return aid, aname
        # First-name match
        first = name_lower.split()[0] if name_lower else ""
        for aid, aname in all_athletes:
            if first and aname.lower().startswith(first):
                return aid, aname
        return None, None

    tab_rank, tab_event = st.tabs(["Season Rankings", "Event Results"])

    # ── Tab 1: Season Rankings ────────────────────────────────────────────────
    with tab_rank:
        st.markdown("#### Update Season Rankings")
        st.markdown(
            "Go to [WSL Rankings](https://www.worldsurfleague.com/athletes/tour/mct?year=2026), "
            "copy the rows you want, and paste below in this format:"
        )
        st.code("Rank, Athlete Name, Total Points\n5, Caitlin Simmers, 6745\n9, Erin Brooks, 4000", language="text")

        rc1, rc2, rc3 = st.columns(3)
        tour_sel = rc1.selectbox("Tour", ["Men's CT", "Women's CT"])
        season   = rc2.text_input("Season", value="2026")
        as_of    = rc3.date_input("As Of Date", value=date.today())

        raw = st.text_area("Paste rankings here", height=220,
                           placeholder="5, Caitlin Simmers, 6745\n9, Erin Brooks, 4000\n10, Carissa Moore, 4000")

        if st.button("Parse & Preview", type="primary", key="parse_rank"):
            con = get_db()
            all_athletes = con.execute("SELECT id, name FROM athletes").fetchall()
            con.close()

            lines   = [l.strip() for l in raw.strip().split('\n') if l.strip()]
            parsed  = []
            skipped = []

            for line in lines:
                if line.lower().startswith('rank') or line.lower().startswith('#'):
                    continue
                # Support comma or tab separation
                parts = [p.strip().replace(',', '') for p in line.replace('\t', ',').split(',')]
                parts = [p for p in parts if p]
                if len(parts) < 3:
                    skipped.append(line)
                    continue
                try:
                    rank_val = int(parts[0])
                    name_val = parts[1].strip()
                    pts_val  = int(float(parts[2]))
                    aid_m, aname_m = match_athlete(name_val, all_athletes)
                    parsed.append({
                        'rank': rank_val, 'input_name': name_val,
                        'points': pts_val,
                        'matched_id': aid_m, 'matched_name': aname_m or '⚠ No match',
                    })
                except Exception:
                    skipped.append(line)

            if parsed:
                st.session_state['sync_rank_preview'] = {
                    'data': parsed, 'tour': tour_sel,
                    'season': season, 'as_of': str(as_of),
                }
                preview_df = pd.DataFrame([{
                    'Input Name':      p['input_name'],
                    'Matched Athlete': p['matched_name'],
                    'Rank':            p['rank'],
                    'Total Pts':       p['points'],
                    'Status':          '✓ Ready' if p['matched_id'] else '⚠ No match',
                } for p in parsed])
                st.dataframe(preview_df, use_container_width=True, hide_index=True)
                matched = sum(1 for p in parsed if p['matched_id'])
                st.info(f"{matched} of {len(parsed)} athletes matched to roster.")
                if skipped:
                    st.warning(f"Skipped {len(skipped)} unreadable lines.")
            else:
                st.warning("Could not parse any rows. Check the format.")

        if st.session_state.get('sync_rank_preview'):
            preview = st.session_state['sync_rank_preview']
            if st.button("✓ Import Rankings", type="primary", key="import_rank"):
                con = get_db()
                imported = 0
                for p in preview['data']:
                    if not p['matched_id']:
                        continue
                    con.execute(
                        "DELETE FROM ranking_history WHERE athlete_id=%s AND season=?",
                        (p['matched_id'], preview['season'])
                    )
                    con.execute(
                        """INSERT INTO ranking_history
                           (athlete_id,season,tour,as_of,ranking,points,notes)
                           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                        (p['matched_id'], preview['season'], preview['tour'],
                         preview['as_of'], p['rank'], p['points'],
                         f"Synced from WSL {preview['as_of']}")
                    )
                    imported += 1
                con.commit(); con.close()
                st.success(f"✓ Imported rankings for {imported} athletes.")
                st.session_state['sync_rank_preview'] = None
                st.rerun()

    # ── Tab 2: Event Results ──────────────────────────────────────────────────
    with tab_event:
        st.markdown("#### Add Event Results")
        st.markdown("Paste results for a single event — one athlete per line:")
        st.code("Athlete Name, Round Reached, Points\nCaitlin Simmers, Quarterfinal, 4745\nErin Brooks, Round 2, 2000",
                language="text")

        ec1, ec2 = st.columns(2)
        ev_name     = ec1.text_input("Event Name", placeholder="Western Australia Pro Margaret River")
        ev_date_inp = ec2.date_input("Event Date", value=date.today(), key="ev_date")
        ec3, ec4 = st.columns(2)
        ev_tour     = ec3.text_input("Tour", value="WSL CT")
        ev_location = ec4.text_input("Location", placeholder="Margaret River, WA, Australia")

        raw_ev = st.text_area("Paste event results here", height=200,
                              placeholder="Caitlin Simmers, Quarterfinal, 4745\nErin Brooks, Round 2, 2000")

        ROUND_PLACE = {
            'winner': 1, 'final': 1, 'runner-up': 2,
            'semifinal': 3, 'quarterfinal': 5,
            'round 3': 9, 'round 2': 17, 'round 1': 25,
        }

        if st.button("Parse & Preview Results", type="primary", key="parse_ev"):
            con = get_db()
            all_athletes = con.execute("SELECT id, name FROM athletes").fetchall()
            con.close()

            lines_ev = [l.strip() for l in raw_ev.strip().split('\n') if l.strip()]
            parsed_ev = []

            for line in lines_ev:
                if line.lower().startswith('athlete'):
                    continue
                parts = [p.strip() for p in line.replace('\t', ',').split(',')]
                parts = [p for p in parts if p]
                if len(parts) < 3:
                    continue
                try:
                    name_val  = parts[0].strip()
                    round_val = parts[1].strip()
                    pts_val   = int(parts[2].replace(',', ''))
                    place_val = next((v for k, v in ROUND_PLACE.items() if k in round_val.lower()), 0)
                    aid_m, aname_m = match_athlete(name_val, all_athletes)
                    parsed_ev.append({
                        'input_name': name_val, 'round': round_val,
                        'points': pts_val, 'place': place_val,
                        'matched_id': aid_m, 'matched_name': aname_m or '⚠ No match',
                    })
                except Exception:
                    pass

            if parsed_ev:
                st.session_state['sync_ev_preview'] = {
                    'data': parsed_ev, 'event': ev_name,
                    'date': str(ev_date_inp), 'tour': ev_tour, 'location': ev_location,
                }
                ev_df = pd.DataFrame([{
                    'Input Name': p['input_name'],
                    'Matched':    p['matched_name'],
                    'Round':      p['round'],
                    'Points':     p['points'],
                    'Status':     '✓ Ready' if p['matched_id'] else '⚠ No match',
                } for p in parsed_ev])
                st.dataframe(ev_df, use_container_width=True, hide_index=True)
                matched_ev = sum(1 for p in parsed_ev if p['matched_id'])
                st.info(f"{matched_ev} of {len(parsed_ev)} athletes matched to roster.")
            else:
                st.warning("Could not parse any rows. Check the format.")

        if st.session_state.get('sync_ev_preview'):
            prev_ev = st.session_state['sync_ev_preview']
            if st.button("✓ Import Event Results", type="primary", key="import_ev"):
                con = get_db()
                imported = 0
                for p in prev_ev['data']:
                    if not p['matched_id']:
                        continue
                    con.execute(
                        "DELETE FROM comp_results WHERE athlete_id=%s AND event=? AND season='2026'",
                        (p['matched_id'], prev_ev['event'])
                    )
                    con.execute(
                        """INSERT INTO comp_results
                           (athlete_id,season,event,tour,event_date,location,round,place,points)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (p['matched_id'], '2026', prev_ev['event'], prev_ev['tour'],
                         prev_ev['date'], prev_ev['location'],
                         p['round'], p['place'], p['points'])
                    )
                    imported += 1
                con.commit(); con.close()
                st.success(f"✓ Imported results for {imported} athletes.")
                st.session_state['sync_ev_preview'] = None
                st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("<small class='kicker'>Red Bull Performance</small>", unsafe_allow_html=True)
        st.markdown("## Surf Dash")
        st.markdown("---")

        if st.button("Overview", use_container_width=True,
                     type="primary" if st.session_state.get("page") == "overview" else "secondary"):
            st.session_state.page = "overview"
            st.rerun()

        st.markdown("---")
        st.markdown("**Athletes**")

        athletes = get_athletes()
        # Group by tour (index 4 = tour)
        ct_group = [a for a in athletes if "CT" in (a[4] or "").upper()]
        cs_group = [a for a in athletes if any(x in (a[4] or "").upper() for x in ["CHALLENGER","CS"])]
        ot_group = [a for a in athletes if a not in ct_group and a not in cs_group]

        for label, group in [("CT", ct_group), ("Challenger", cs_group), ("Other", ot_group)]:
            if not group: continue
            st.markdown(f"<small style='color:#aab;text-transform:uppercase;letter-spacing:1px'>{label}</small>", unsafe_allow_html=True)
            for a in group:
                aid, aname, *rest = a
                has_injury = rest[7]   # index 9 in full row, offset 7 after aid+name
                is_active  = st.session_state.get("athlete_id") == aid and st.session_state.get("page") == "athlete"
                btn_type   = "primary" if is_active else "secondary"
                if st.button(aname, key=f"sb_{aid}", use_container_width=True, type=btn_type):
                    st.session_state.page       = "athlete"
                    st.session_state.athlete_id = aid
                    st.rerun()

        st.markdown("---")
        if st.button("⟳ Sync WSL Data", use_container_width=True,
                     type="primary" if st.session_state.get("page") == "sync" else "secondary"):
            st.session_state.page = "sync"
            st.rerun()

        st.markdown("<small style='color:#94a3b8'>Surf Dash · 2026</small>", unsafe_allow_html=True)


# ── Auth ──────────────────────────────────────────────────────────────────────
def build_authenticator():
    credentials = {
        "usernames": {
            "will": {
                "email": "will.gilmore@redbull.com",
                "name": "Will Gilmore",
                "password": st.secrets["passwords"]["will"],
                "role": "admin",
            },
            "pt1": {
                "email": "pt1@redbull.com",
                "name": st.secrets.get("pt_names", {}).get("pt1", "PT User 1"),
                "password": st.secrets["passwords"]["pt1"],
                "role": "pt",
            },
            "pt2": {
                "email": "pt2@redbull.com",
                "name": st.secrets.get("pt_names", {}).get("pt2", "PT User 2"),
                "password": st.secrets["passwords"]["pt2"],
                "role": "pt",
            },
            "pt3": {
                "email": "pt3@redbull.com",
                "name": st.secrets.get("pt_names", {}).get("pt3", "PT User 3"),
                "password": st.secrets["passwords"]["pt3"],
                "role": "pt",
            },
            "viewer": {
                "email": "team@redbull.com",
                "name": "Team Viewer",
                "password": st.secrets["passwords"]["viewer"],
                "role": "viewer",
            },
        }
    }
    return stauth.Authenticate(
        credentials,
        cookie_name="surf_dash_auth",
        cookie_key=st.secrets["auth_cookie_key"],
        cookie_expiry_days=7,
    )

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    init_db()

    authenticator = build_authenticator()
    authenticator.login(location="main")

    auth_status = st.session_state.get("authentication_status")
    username    = st.session_state.get("username", "")
    name        = st.session_state.get("name", "")

    if auth_status is False:
        st.error("Incorrect username or password.")
        return
    if auth_status is None:
        st.markdown("""
        <div style='max-width:400px;margin:80px auto;text-align:center'>
            <h2 style='color:#0f172a'>🏄 Surf Dash</h2>
            <p style='color:#64748b'>Red Bull Surf Performance · Enter your credentials above</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Authenticated ──────────────────────────────────────────────────────
    # Determine role from credentials config
    role_map = {"will": "admin", "pt1": "pt", "pt2": "pt", "pt3": "pt", "viewer": "viewer"}
    role = role_map.get(username, "viewer")
    st.session_state.role     = role
    st.session_state.username = username
    st.session_state.fullname = name

    if "page" not in st.session_state:
        st.session_state.page = "overview"

    # Logout button in sidebar
    with st.sidebar:
        st.markdown(f"<small style='color:#94a3b8'>Signed in as <strong style='color:#edf2f7'>{name}</strong></small>", unsafe_allow_html=True)
        role_label = {"admin": "Admin", "pt": "PT Staff", "viewer": "Team Viewer"}.get(role, role)
        st.markdown(f"<small style='color:#64748b'>{role_label}</small>", unsafe_allow_html=True)
        authenticator.logout("Sign Out", location="sidebar")

    sidebar()

    if st.session_state.page == "overview":
        page_overview()
    elif st.session_state.page == "athlete":
        aid = st.session_state.get("athlete_id")
        if aid:
            page_athlete(aid)
        else:
            page_overview()
    elif st.session_state.page == "sync":
        if role in ("admin", "pt"):
            page_sync()
        else:
            st.warning("You need PT or Admin access to sync data.")


if __name__ == "__main__":
    main()
