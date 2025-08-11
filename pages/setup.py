import os
import streamlit as st
import psycopg2
import psycopg2.extras
from pathlib import Path

# --- UI Styles ---
st.set_page_config(page_title="Loreweave • Setup", layout="centered")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');
.stApp { background: #000; color: #fff; font-family: 'Lora', serif !important; }
h1, h2, h3 { font-family: 'Cinzel', serif !important; text-transform: uppercase; }
label { color:#fff !important; font-weight:bold; }
div.stButton > button { background:#333 !important; color:#fff !important; border:none !important; }
.step { background: rgba(255,255,255,0.06); padding: 1rem; border-radius: 12px; margin: .75rem 0; }
.tip  { font-size: 13px; opacity: 0.9; }
hr { border: none; border-top: 1px solid rgba(255,255,255,.15); margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;'>
  <img src='https://i.imgur.com/YBozTrh.png' width='180' />
  <h1 style='margin-top:.25rem;'>Setup Wizard</h1>
  <p class='tip'>This will connect your app to a Neon Postgres database, initialize the schema, and create your first admin user.</p>
</div>
<hr/>
""", unsafe_allow_html=True)

# --- DB helpers (local, non-invasive to repo) ---
def _conn(url: str):
    return psycopg2.connect(url, sslmode="require")

def _table_exists(url: str, table: str) -> bool:
    with _conn(url) as cn, cn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as c:
        c.execute("""
          SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema='public' AND table_name=%s
          ) AS ok
        """, (table,))
        return bool(c.fetchone()["ok"])

def _run_sql_file(url: str, path: str):
    p = Path(path)
    if not p.exists():
        return
    sql_text = p.read_text(encoding="utf-8")
    with _conn(url) as cn, cn.cursor() as c:
        c.execute(sql_text)
        cn.commit()

def _ensure_schema(url: str):
    if not _table_exists(url, "users"):
        _run_sql_file(url, "sql/init_db.sql")
        if Path("sql/seed_calendar.sql").exists():
            _run_sql_file(url, "sql/seed_calendar.sql")

def _count_users(url: str) -> int:
    if not _table_exists(url, "users"):
        return 0
    with _conn(url) as cn, cn.cursor() as c:
        c.execute("SELECT COUNT(*) FROM users")
        return int(c.fetchone()[0])

# --- Step 1: Get / verify DATABASE_URL ---
st.subheader("Step 1 — Connect to Neon")

env_url = os.getenv("DATABASE_URL", "")
mask = ""
if env_url:
    try:
        host = env_url.split("@")[-1].split("?")[0]
    except Exception:
        host = "(unknown)"
    mask = f"`{host}`"

st.markdown("<div class='step'>", unsafe_allow_html=True)
st.markdown("**Your current connection**")
if env_url:
    st.success(f"Found `DATABASE_URL` → {mask}")
else:
    st.warning("No `DATABASE_URL` detected in the environment.")

manual_url = st.text_input(
    "Paste your Neon connection string (postgresql://user:pass@host/db?sslmode=require)",
    value=env_url if env_url else "",
    type="password",
    help="Get this from Neon → Project → Connection Details → Connection string"
)

colA, colB = st.columns([1,1])
with colA:
    test_clicked = st.button("Test Connection")
with colB:
    use_clicked = st.button("Use This Connection")

if test_clicked:
    try:
        with _conn(manual_url) as cn:
            with cn.cursor() as c:
                c.execute("SELECT 1")
        st.success("Connection successful.")
    except Exception as e:
        st.error(f"Connection failed: {e}")

if use_clicked and manual_url:
    st.session_state["SETUP_DB_URL"] = manual_url
    st.success("Connection saved for this setup session.")

active_url = st.session_state.get("SETUP_DB_URL") or manual_url or env_url

st.markdown("</div>", unsafe_allow_html=True)

# --- Step 2: Initialize schema ---
st.subheader("Step 2 — Initialize Database Schema")

st.markdown("<div class='step'>", unsafe_allow_html=True)
if not active_url:
    st.info("Paste your Neon connection string above to continue.")
else:
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Initialize Schema"):
            try:
                _ensure_schema(active_url)
                st.success("Schema initialized (idempotent).")
            except Exception as e:
                st.error(f"Initialization error: {e}")

    with col2:
        if st.button("Check Schema Status"):
            try:
                users_ok = _table_exists(active_url, "users")
                events_ok = _table_exists(active_url, "campaignevents")
                st.write(f"- users table: **{'OK' if users_ok else 'Missing'}**")
                st.write(f"- campaignevents table: **{'OK' if events_ok else 'Missing'}**")
            except Exception as e:
                st.error(f"Check failed: {e}")
st.markdown("</div>", unsafe_allow_html=True)

# --- Step 3: Create first admin ---
st.subheader("Step 3 — Create First Admin")

st.markdown("<div class='step'>", unsafe_allow_html=True)
if not active_url:
    st.info("Connect to the database first.")
else:
    import bcrypt
    with st.form("create_admin"):
        uname = st.text_input("Admin Username")
        pwd = st.text_input("Admin Password", type="password")
        submitted = st.form_submit_button("Create Admin User")
        if submitted:
            if not uname or not pwd:
                st.error("Please provide a username and password.")
            else:
                try:
                    _ensure_schema(active_url)
                    pw_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    with _conn(active_url) as cn, cn.cursor() as c:
                        c.execute(
                            "INSERT INTO users (username, password_hash, is_admin) VALUES (%s,%s,true) ON CONFLICT (username) DO NOTHING",
                            (uname, pw_hash)
                        )
                        cn.commit()
                    count = _count_users(active_url)
                    st.success(f"Admin created. Total users: {count}.")
                except Exception as e:
                    st.error(f"Failed to create admin: {e}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)
st.caption("Tip: On Render, set the `DATABASE_URL` environment variable in the service settings so it persists across restarts.")
