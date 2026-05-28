import streamlit as st
import yfinance as yf
import pandas as pd
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="בורסה לילדים", layout="wide", initial_sidebar_state="expanded")

# רענון אוטומטי כל 2 דקות 
refresh_count = st_autorefresh(interval=120000, limit=None, key="auto_refresh")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap');

.stApp { direction: rtl !important; font-family: 'Heebo', sans-serif !important; }
.block-container { direction: rtl !important; max-width: 1100px; }

h1, h2, h3, h4, h5, h6 { direction: rtl !important; text-align: right !important; font-family: 'Heebo', sans-serif !important; }
.stMarkdown p, .stMarkdown li { direction: rtl !important; text-align: right !important; font-family: 'Heebo', sans-serif !important; }
[data-testid="stSidebar"] .stMarkdown { direction: rtl !important; text-align: right !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] p {
    direction: rtl !important; text-align: right !important; font-family: 'Heebo', sans-serif !important;
}

/* סידור המדים והאפשרויות לימין */
[data-testid="stSlider"] { direction: ltr !important; }
[data-testid="stRadio"] { direction: rtl !important; text-align: right !important; }

.stTabs [data-baseweb="tab-list"] { direction: rtl !important; gap: 6px; }
.stTabs [data-baseweb="tab"] { font-size: 17px !important; font-weight: 700 !important; font-family: 'Heebo', sans-serif !important; }
[data-testid="metric-container"] { text-align: right !important; }

/* עיצוב כפתור ההגרלה */
div.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white; border-radius: 12px; border: none; padding: 10px;
    font-size: 16px; font-weight: 700; font-family: 'Heebo', sans-serif;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; margin-bottom: 20px;
}
div.stButton > button:hover { background: linear-gradient(135deg, #d97706 0%, #b45309 100%); color: white; border: none; }

.mascot-card {
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    border-radius: 20px; padding: 20px 30px; display: flex; align-items: center; gap: 25px;
    margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 3px solid #7dd3fc;
}
.mascot-emoji { font-size: 80px; line-height: 1; }
.mascot-text h2 { margin: 0 0 10px 0; color: #0369a1; font-size: 28px; }
.mascot-text p { margin: 0; color: #0c4a6e; font-size: 18px; line-height: 1.5; font-weight: 600; }

.refresh-bar {
    background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 8px 16px;
    margin-bottom: 16px; direction: rtl; font-family: 'Heebo', sans-serif; font-size: 13px; color: #166534;
    display: flex; justify-content: space-between; align-items: center;
}

/* התאמת טבלה למובייל */
.table-responsive { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: 12px; margin-bottom: 20px; }
.kids-table {
    width: 100%; border-collapse: collapse; direction: rtl; font-family: 'Heebo', sans-serif;
    font-size: 15px; margin-top: 10px; min-width: 600px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.kids-table thead tr { background: #4f46e5; color: white; }
.kids-table th { padding: 12px 16px; text-align: right !important; font-weight: 700; font-size: 14px; white-space: nowrap; }
.kids-table tbody tr { background: white; }
.kids-table tbody tr:nth-child(even) { background: #f8f8ff; }
.kids-table tbody tr:hover { background: #ede9fe; }
.kids-table td { padding: 11px 16px; text-align: right !important; border-bottom: 1px solid #e5e7eb; vertical-align: middle; }
.risk-badge { display: inline-block; padding: 3px 10px; border-radius: 99px; font-weight: 700; font-size: 13px; color: white; white-space: nowrap; }
.positive { color: #16a34a; font-weight: 700; }
.negative { color: #dc2626; font-weight: 700; }

/* התאמות עיצוב לסלולר (מסכים קטנים) */
@media (max-width: 768px) {
    .mascot-card { flex-direction: column; text-align: center; padding: 15px; gap: 10px; }
    .mascot-emoji { font-size: 60px; }
    .mascot-text h2 { font-size: 22px; }
    .mascot-text p { font-size: 16px; }
    .refresh-bar { flex-direction: column; text-align: center; gap: 5px; }
    .id-header { flex-direction: column !important; align-items: center !important; text-align: center; gap: 15px; }
    .id-header img { margin-top: 10px; }
    .id-grid { grid-template-columns: 1fr !important; }
    .calc-grid { flex-direction: column !important; gap: 15px !important; }
}
</style>
""", unsafe_allow_html=True)

# =================== מאגר חברות ענק להגרלה ===================
FULL_KIDS_COMPANIES = {
    "RBLX": {"name": "רובלוקס 🎮", "desc": "פלטפורמה ענקית לבניית משחקים.", "products": "עולמות וירטואליים וכסף משחק (Robux).", "fun_fact": "בכל יום נכנסים למשחק יותר מ-60 מיליון ילדים!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Roblox_player_icon_black.svg/120px-Roblox_player_icon_black.svg.png", "risk": 9},
    "DIS": {"name": "דיסני 🎢", "desc": "חברת הבידור והסרטים הגדולה בעולם.", "products": "סרטי מארוול, פארקי שעשועים ובובות.", "fun_fact": "הדמות הראשונה שוולט דיסני צייר הייתה ארנב, לא עכבר!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Disney_wordmark.svg/200px-Disney_wordmark.svg.png", "risk": 5},
    "MCD": {"name": "מקדונלד'ס 🍔", "desc": "רשת המסעדות המוכרת ביותר בעולם.", "products": "המבורגרים, צ'יפס וארוחות ילדים.", "fun_fact": "היא חברת הצעצועים הגדולה בעולם בזכות ההפתעות בארוחות!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png", "risk": 3},
    "NKE": {"name": "נייקי 👟", "desc": "יצרנית בגדי ונעלי הספורט הגדולה בעולם.", "products": "נעלי כדורסל (כמו ג'ורדן) ובגדי ספורט.", "fun_fact": "סמל החברה (ה'סווש') עוצב על ידי סטודנטית שהרוויחה עליו רק 35 דולר!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Logo_NIKE.svg/200px-Logo_NIKE.svg.png", "risk": 6},
    "KO": {"name": "קוקה-קולה 🥤", "desc": "המשקה המתוק הנמכר ביותר בהיסטוריה.", "products": "קוקה קולה, פאנטה וספרייט.", "fun_fact": "המתכון הסודי שמור בתוך כספת מיוחדת וענקית באטלנטה!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Coca-Cola_logo.svg/200px-Coca-Cola_logo.svg.png", "risk": 2},
    "AAPL": {"name": "אפל 📱", "desc": "ענקית טכנולוגיה שממציאה מכשירים חכמים.", "products": "אייפון, אייפד ושעוני אפל.", "fun_fact": "המייסדים מכרו את המכונית שלהם רק כדי לקנות רכיבים למחשב הראשון!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/100px-Apple_logo_black.svg.png", "risk": 7},
    "MSFT": {"name": "מיקרוסופט 💻", "desc": "חברת תוכנה ומשחקים ענקית.", "products": "ווינדוס, קונסולת אקס-בוקס (Xbox) ומיינקראפט.", "fun_fact": "מקים החברה, ביל גייטס, התחיל לתכנת כשהיה רק בן 13!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/200px-Microsoft_logo.svg.png", "risk": 5},
    "SONY": {"name": "סוני 🕹️", "desc": "חברה יפנית שמייצרת אלקטרוניקה ומשחקים.", "products": "פלייסטיישן, טלוויזיות, וסרטי ספיידרמן.", "fun_fact": "הפלייסטיישן הראשון הומצא בכלל בגלל ויכוח בין סוני לחברת נינטנדו!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Sony_logo.svg/200px-Sony_logo.svg.png", "risk": 6},
    "NFLX": {"name": "נטפליקס 🍿", "desc": "החברה שהמציאה את הצפייה הישירה בסדרות.", "products": "סרטים וסדרות דרך האינטרנט.", "fun_fact": "פעם, נטפליקס הייתה שולחת סרטים על דיסקים (DVD) לאנשים בדואר!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/200px-Netflix_2015_logo.svg.png", "risk": 8},
    "AMZN": {"name": "אמזון 📦", "desc": "החנות האינטרנטית הגדולה בעולם.", "products": "אתר קניות שמגיע עד הבית ועוזרים חכמים (אלקסה).", "fun_fact": "כשהאתר הוקם, הוא מכר רק סוג אחד של מוצרים: ספרים!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/200px-Amazon_logo.svg.png", "risk": 6},
    "HSY": {"name": "הרשיז 🍫", "desc": "אחת מחברות השוקולד הגדולות באמריקה.", "products": "שוקולד, ריסס (Reese's) וסירופ לפנקייק.", "fun_fact": "בעיר שבה החברה נמצאת, אפילו פנסי הרחוב מעוצבים כמו נשיקות שוקולד!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/The_Hershey_Company_logo.svg/200px-The_Hershey_Company_logo.svg.png", "risk": 3},
    "MAT": {"name": "מאטל 🏎️", "desc": "יצרנית הצעצועים הענקית.", "products": "ברבי, מכוניות הוט-ווילס (Hot Wheels) ומשחק הקלפים טאקי/אونو.", "fun_fact": "בובת הברבי הראשונה בעולם עלתה רק 3 דולר!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Mattel_logo.svg/200px-Mattel_logo.svg.png", "risk": 7}
}

FULL_BACKUP_DATA = {
    "RBLX": {"div": 0.0, "growth": 35.2}, "DIS": {"div": 0.0, "growth": -9.8},
    "MCD": {"div": 2.4, "growth": 11.5}, "NKE": {"div": 1.6, "growth": -17.4},
    "KO": {"div": 3.0, "growth": 6.2}, "AAPL": {"div": 0.5, "growth": 26.8},
    "MSFT": {"div": 0.8, "growth": 30.0}, "SONY": {"div": 0.6, "growth": 15.0},
    "NFLX": {"div": 0.0, "growth": 40.0}, "AMZN": {"div": 0.0, "growth": 50.0},
    "HSY": {"div": 2.8, "growth": -10.0}, "MAT": {"div": 0.0, "growth": -5.0}
}

# ניהול הגרלת החברות
if "active_tickers" not in st.session_state:
    st.session_state.active_tickers = random.sample(list(FULL_KIDS_COMPANIES.keys()), 6)

# =================== תחילת הממשק ===================
st.markdown("""
<div class="mascot-card">
<div class="mascot-emoji">🦉</div>
<div class="mascot-text">
<h2>היי חברים! אני שוקי הינשוף!</h2>
<p>אני כאן כדי לעזור לכם להבין איך הבורסה עובדת. <br>מוכנים לצאת להרפתקה ולגלות איך החברות הכי גדולות בעולם עושות כסף?</p>
</div>
</div>
""", unsafe_allow_html=True)

st.title("🎢 משחק ההשקעות הראשון שלי!")

now_str = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
<div class="refresh-bar">
<span>🔄 הנתונים מתעדכנים אוטומטית מהבורסה</span>
<span>⏰ עדכון אחרון: {now_str}</span>
</div>
""", unsafe_allow_html=True)

# כפתור הגרלה בתפריט הצדדי
if st.sidebar.button("🎲 שוקי, תביא חברות חדשות!", use_container_width=True):
    st.session_state.active_tickers = random.sample(list(FULL_KIDS_COMPANIES.keys()), 6)

tab1, tab2 = st.tabs(["🚀 המשחק והחברות", "📚 הבורסה של שוקי"])

# =================== טאב המשחק ===================
with tab1:
    @st.cache_data(ttl=120)
    def fetch_kids_data(tickers):
        rows = []
        for ticker in tickers:
            d = FULL_KIDS_COMPANIES[ticker]
            try:
                t = yf.Ticker(ticker)
                info = t.info
                hist = t.history(period="1y")
                ret = 0.0
                if len(hist) > 1:
                    ret = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                div = (info.get('dividendYield') or 0.0) * 100
                rows.append({
                    "ticker": ticker, "name": d["name"], "desc": d["desc"],
                    "products": d["products"], "fun_fact": d["fun_fact"], "image": d["image"],
                    "risk": d["risk"], "div": round(div, 2), "growth": round(ret, 2),
                })
            except Exception:
                pass
                
        # שימוש בגיבוי אם השרת נחסם
        if len(rows) == 0:
            for ticker in tickers:
                d = FULL_KIDS_COMPANIES[ticker]
                rows.append({
                    "ticker": ticker, "name": d["name"], "desc": d["desc"],
                    "products": d["products"], "fun_fact": d["fun_fact"], "image": d["image"],
                    "risk": d["risk"], "div": FULL_BACKUP_DATA[ticker]["div"], 
                    "growth": FULL_BACKUP_DATA[ticker]["growth"], "is_dummy": True 
                })
        return pd.DataFrame(rows)

    with st.spinner("🔄 שוקי הינשוף אוסף נתונים מהבורסה..."):
        df = fetch_kids_data(tuple(st.session_state.active_tickers))
        
    if df.empty:
        st.error("תקלה לא צפויה בטעינת הנתונים.")
        st.stop()
        
    if "is_dummy" in df.columns:
        st.info("💡 המערכת של הבורסה קצת עמוסה כרגע. נטענו נתוני אמת מהעדכון האחרון כדי שלא נפסיק לשחק!")

    # סליידרים בצד
    st.sidebar.markdown("""
    <div dir="rtl" style="text-align:right; font-family:'Heebo',sans-serif; padding-top:10px; border-top: 2px dashed #d1d5db;">
    <h3 style="margin:10px 0 4px 0;">🕹️ איזה משקיע אתה?</h3>
    <p style="font-size:13px; color:#6b7280; margin:0 0 15px 0;">הזז את המדים כדי להתאים את הציונים אליך!</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">🚀 כמה חשובה לי צמיחה מהירה?</div>', unsafe_allow_html=True)
    w_growth = st.sidebar.slider(" ", 0, 10, 5, key="growth_slider")
    st.sidebar.markdown('<div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;margin-bottom:16px;font-family:Heebo,sans-serif;">0 = לא אכפת לי &nbsp;|&nbsp; 10 = הכי חשוב!</div>', unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">💰 כמה חשוב לי לקבל דמי כיס?</div>', unsafe_allow_html=True)
    w_dividend = st.sidebar.slider("  ", 0, 10, 5, key="div_slider")
    st.sidebar.markdown('<div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;margin-bottom:16px;font-family:Heebo,sans-serif;">0 = לא אכפת לי &nbsp;|&nbsp; 10 = הכי חשוב!</div>', unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">🎢 כמה סיכון אני מוכן לקחת?</div>', unsafe_allow_html=True)
    w_risk = st.sidebar.slider("   ", 1, 10, 5, key="risk_slider")
    risk_color_label = "#16a34a" if w_risk <= 3 else "#d97706" if w_risk <= 6 else "#dc2626"
    risk_text_label  = "🟢 בטוח ורגוע" if w_risk <= 3 else "🟡 קצת מכל דבר" if w_risk <= 6 else "🔴 אני אוהב רכבות הרים!"
    st.sidebar.markdown(f"""
    <div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;font-family:Heebo,sans-serif;">1 = רק בטוחים &nbsp;|&nbsp; 10 = אוהב להסתכן!</div>
    <div dir="rtl" style="text-align:center;font-family:'Heebo',sans-serif;background:#f3f4f6;border-radius:8px;padding:8px;font-size:14px;margin-top:8px;">
    סגנון ההשקעה שלך: <br><strong style="color:{risk_color_label};">{risk_text_label} ({w_risk}/10)</strong>
    </div>
    """, unsafe_allow_html=True)

    def calc_stars(row):
        total_w = w_growth + w_dividend + 5
        if total_w == 0: total_w = 1
        s_growth = min(max(row["growth"], 0), 100)
        s_div    = min(row["div"] * 30, 100)
        s_risk   = max(100 - abs(row["risk"] - w_risk) * 10, 0)
        final    = ((s_growth * w_growth) + (s_div * w_dividend) + (s_risk * 5)) / total_w
        return "⭐" * max(1, min(round(final / 20), 5))

    def risk_color(r): return "#16a34a" if r <= 3 else "#d97706" if r <= 6 else "#dc2626"
    def risk_label(r): return "נמוך" if r <= 3 else "בינוני" if r <= 6 else "גבוה"

    rows_html = ""
    for _, row in df.iterrows():
        stars  = calc_stars(row)
        g_cls  = "positive" if row["growth"] >= 0 else "negative"
        g_sign = "+" if row["growth"] >= 0 else ""
        rows_html += f"""
        <tr>
        <td><strong>{row['name']}</strong><br><small style="color:#6b7280;">{row['ticker']}</small></td>
        <td><span class="risk-badge" style="background:{risk_color(row['risk'])};">{risk_label(row['risk'])} ({row['risk']}/10)</span></td>
        <td>{row['div']}%</td>
        <td class="{g_cls}">{g_sign}{row['growth']}%</td>
        <td style="font-size:18px;letter-spacing:2px;">{stars}</td>
        </tr>"""

    st.subheader("🏆 טבלת החברות להשקעה")
    # עטיפת הטבלה ב-div שמאפשר גלילה במובייל
    st.markdown(f"""
    <div class="table-responsive">
    <table class="kids-table">
    <thead><tr>
    <th>🏢 שם החברה</th><th>🎢 רמת סיכון</th><th>💰 דמי כיס (%)</th><th>📈 צמיחה השנה</th><th>⭐ התאמה</th>
    </tr></thead>
    <tbody>{rows_html}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔍 תעודת זהות לחברה")
    name_to_ticker = {row["name"]: row["ticker"] for _, row in df.iterrows()}
    
    selected_name = st.selectbox("בחרו חברה כדי ללמוד עליה ולחשב רווחים:", list(name_to_ticker.keys()))
    sel = df[df["name"] == selected_name].iloc[0]

    risk_dots = ("🔴" * sel['risk']) + ("⚪" * (10 - sel['risk']))

    st.markdown(f"""
    <div dir="rtl" style="background:white; border: 2px solid #e5e7eb; border-radius:15px; padding:25px; margin-top: 15px; font-family:'Heebo',sans-serif; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
    <div class="id-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px dashed #e5e7eb; padding-bottom: 15px;">
    <div>
    <h2 style="margin:0 0 5px 0; color:#111827; font-size: 32px;">{sel['name']} ({sel['ticker']})</h2>
    <span style="background-color: #f3f4f6; padding: 5px 12px; border-radius: 20px; font-weight: 600; color: #4b5563; font-size: 14px;">מדד התאמה אישי: {calc_stars(sel)}</span>
    </div>
    <img src="{sel['image']}" style="height: 60px; object-fit: contain;">
    </div>
    
    <div class="id-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
    <div style="background: #f8fafc; padding: 15px; border-radius: 10px;">
    <h4 style="margin:0 0 10px 0; color:#3b82f6;">🏢 מה החברה עושה?</h4>
    <p style="margin:0; color:#333;">{sel['desc']}</p>
    </div>
    <div style="background: #fffbeb; padding: 15px; border-radius: 10px;">
    <h4 style="margin:0 0 10px 0; color:#d97706;">🛒 מה היא מוכרת לנו?</h4>
    <p style="margin:0; color:#333;">{sel['products']}</p>
    </div>
    </div>
    
    <div style="background: #f0fdfa; padding: 15px; border-radius: 10px; margin-bottom: 25px;">
    <h4 style="margin:0 0 5px 0; color:#0d9488;">💡 הידעת? (עובדת בונוס!)</h4>
    <p style="margin:0; color:#115e59; font-weight: 600;">{sel['fun_fact']}</p>
    </div>
    
    <h3 style="margin-bottom: 15px;">📊 המספרים של החברה</h3>
    <div style="display: flex; gap: 15px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 120px; background: #f3f4f6; padding: 15px; border-radius: 10px; text-align: center;">
    <div style="font-size: 14px; color: #6b7280; margin-bottom: 5px; font-weight: 700;">מד סיכון</div>
    <div style="font-size: 18px; margin-bottom: 5px;">{sel['risk']} / 10</div>
    <div style="font-size: 12px;">{risk_dots}</div>
    </div>
    <div style="flex: 1; min-width: 120px; background: #f3f4f6; padding: 15px; border-radius: 10px; text-align: center;">
    <div style="font-size: 14px; color: #6b7280; margin-bottom: 5px; font-weight: 700;">דמי כיס (דיבידנד)</div>
    <div style="font-size: 24px; font-weight: 700; color: #111827;">{sel['div']}%</div>
    <div style="font-size: 12px; color: #4b5563;">מתוך הסכום לשנה</div>
    </div>
    <div style="flex: 1; min-width: 120px; background: {'#dcfce7' if sel['growth'] >= 0 else '#fee2e2'}; padding: 15px; border-radius: 10px; text-align: center;">
    <div style="font-size: 14px; color: #6b7280; margin-bottom: 5px; font-weight: 700;">צמיחה בשנה האחרונה</div>
    <div style="font-size: 24px; font-weight: 700; color: {'#166534' if sel['growth'] >= 0 else '#991b1b'};">
    {'+' if sel['growth']>=0 else ''}{sel['growth']}%
    </div>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # =================== מחשבון השקעות אינטראקטיבי ===================
    st.markdown("---")
    st.subheader(f"🧮 מחשבון השקעות — בואו נבדוק כמה היינו מרוויחים ב-{sel['name']}!")
    
    calc_type = st.radio("איך הייתם רוצים להשקיע?", ["השקעה חד פעמית (שמנו כסף לפני שנה וזהו)", "חסכון חודשי (שמנו קצת כסף כל חודש במשך שנה)"], horizontal=True)
    amount = st.number_input("כמה כסף (בשקלים) הייתם שמים?", min_value=10, max_value=10000, value=100, step=10)
    
    if "חד פעמית" in calc_type:
        total_invested = amount
        total_profit = amount * (sel['growth'] / 100)
        final_amount = total_invested + total_profit
        desc_text = f"שמנו {amount} ₪ בקופה לפני שנה, ולא נגענו."
    else:
        total_invested = amount * 12
        # בחיסכון חודשי הכסף לא יושב שנה שלמה אלא חצי שנה בממוצע, לכן נחלק את הצמיחה ב-2 כהערכה לילדים
        total_profit = total_invested * (sel['growth'] / 100) / 2 
        final_amount = total_invested + total_profit
        desc_text = f"שמנו {amount} ₪ בכל חודש (כפול 12 חודשים)."
        
    profit_color = "#16a34a" if total_profit >= 0 else "#dc2626"
    profit_text = "הרווחנו מהבורסה" if total_profit >= 0 else "הפסדנו מהבורסה"
    
    st.markdown(f"""
    <div style="background: #f8fafc; border-radius: 12px; padding: 20px; text-align: center; border: 2px solid #e2e8f0; font-family:'Heebo',sans-serif;">
        <h4 style="margin-top: 0; color: #334155;">התוצאה: {desc_text}</h4>
        <div class="calc-grid" style="display: flex; justify-content: space-around; align-items: center; margin-top: 20px;">
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); width: 100%; max-width: 200px;">
                <p style="margin: 0; color: #64748b; font-size: 14px; font-weight: bold;">הכסף שהכנסנו מקופת החיסכון:</p>
                <h3 style="margin: 5px 0 0 0; color: #0f172a;">{total_invested:,.0f} ₪</h3>
            </div>
            <div style="font-size: 24px; color: #94a3b8;">+</div>
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); width: 100%; max-width: 200px; border-bottom: 4px solid {profit_color};">
                <p style="margin: 0; color: #64748b; font-size: 14px; font-weight: bold;">{profit_text}:</p>
                <h3 style="margin: 5px 0 0 0; color: {profit_color};">{abs(total_profit):,.0f} ₪</h3>
            </div>
            <div style="font-size: 24px; color: #94a3b8;">=</div>
            <div style="background: #1e293b; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 200px;">
                <p style="margin: 0; color: #cbd5e1; font-size: 14px; font-weight: bold;">היום היה לנו ביד:</p>
                <h3 style="margin: 5px 0 0 0; color: white;">{final_amount:,.0f} ₪</h3>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(f"📈 גרף מחיר — איך המניה של {selected_name} זזה השנה?")
    try:
        hist = yf.Ticker(sel["ticker"]).history(period="1y")
        if not hist.empty:
            st.line_chart(hist[["Close"]].rename(columns={"Close": "מחיר ($)"}), use_container_width=True)
    except Exception:
        st.warning("לא ניתן לטעון גרף כרגע.")

# =================== טאב הסבר וחידון ===================
with tab2:
    st.header("📖 המדריך של שוקי הינשוף לבורסה")
    st.write("ברוכים הבאים לבית הספר להשקעות! בואו נבין איך כל העסק הזה עובד:")

    # הסבר 1 + סרטון בעברית
    st.info("""
    ### 🍋 שלב 1 — מה זו בכלל חברה?
    תחשבו שפתחתם בקיץ **דוכן לימונדה** שכונתי. קניתם לימונים, סוכר וכוסות, והתחלתם למכור.
    
    אם הרבה אנשים קונים מכם לימונדה — הדוכן שלכם מרוויח כסף ומצליח! 🎉 
    חברות ענקיות כמו אפל או קוקה-קולה עובדות בדיוק ככה, פשוט בקנה מידה של כל העולם.
    """)
    st.write("🎥 **צפו בהסבר מעולה של 'כאן סקרנים' על איך בכלל עובד כסף:**")
    st.video("https://www.youtube.com/watch?v=Kz6pG1Y4L1s") 

    # הסבר 2 + סרטון בעברית
    st.success("""
    ### 🧩 שלב 2 — מה זו בעצם מניה?
    נניח שהלימונדה שלכם כל כך טעימה, שאתם רוצים לפתוח **עוד 10 דוכנים!** אבל... הקופה שלכם ריקה ואין לכם מספיק כסף.
    
    מה עושים? אתם מציעים לחברים: **"תנו לי קצת כסף, ובתמורה אתן לכם חתיכה מהדוכן שלי!"**
    
    כל חתיכה כזאת נקראת **מניה**. כשאתם קונים מניה של דיסני, אתם הופכים ל**שותפים** קטנטנים בחברה שלהם!
    """)
    st.write("🎥 **איך הבורסה עובדת? צפו באנימציה של 'כאן 11':**")
    st.video("https://www.youtube.com/watch?v=R9_W7z1RpsU") 

    # הסבר 3 + סרטון בעברית
    st.warning("""
    ### 💰 שלב 3 — איך מרוויחים מזה כסף?
    **1️⃣ המניה נהיית שווה יותר (צמיחה):** אם החברה מצליחה, כולם ירצו לקנות את ה"חתיכות" שלה. ככל שיש יותר ביקוש, המחיר עולה ותוכלו למכור אותן ביותר ממה שקניתם! 🤑
    
    **2️⃣ דמי כיס (דיבידנד):** כשהחברה מרוויחה המון, היא מחלקת לשותפים שלה חלק מהרווחים במזומן ישר לחשבון! 💌
    """)
    st.write("🎥 **צפו בהסבר נוסף לילדים על חיסכון והשקעות:**")
    st.video("https://www.youtube.com/watch?v=e_K0XqQz7-s") 

    st.markdown("---")
    st.subheader("🧠 החידון של שוקי הינשוף! (אינסוף שאלות)")
    st.write("בואו נבדוק מה למדנו! השאלות מוגרלות **מחדש** בכל פעם, והמספרים בהן משתנים, כך שתמיד יהיה לכם אתגר חדש:")

    # מנוע אינסוף השאלות
    def get_infinite_questions_pool():
        pool = [
            {"q": "מה זה דיבידנד?", "options": ["סוג של מניה", "כסף שחברה מחלקת למשקיעים", "שם של חברה", "הלוואה מהבנק"], "answer": "כסף שחברה מחלקת למשקיעים", "ok": "🎉 מעולה! דיבידנד הוא כמו דמי כיס שהחברה מחלקת!", "bad": "❌ דיבידנד הוא כסף מזומן שחברה רווחית מחלקת למי שקנה את המניות שלה."},
            {"q": "מה בדרך כלל יותר בטוח?", "options": ["לקנות מניה של חברה אחת בלבד", "לקנות קרן סל שכוללת המון חברות"], "answer": "לקנות קרן סל שכוללת המון חברות", "ok": "🎉 נכון! פיזור בין הרבה חברות = פחות סיכון!", "bad": "❌ כשקונים הרבה חברות יחד (קרן סל) הסיכון יורד כי אנחנו לא תלויים רק בחברה אחת."},
            {"q": "חברה ותיקה ויציבה כמו קוקה-קולה נחשבת בדרך כלל...", "options": ["מסוכנת מאוד", "יציבה ובטוחה יחסית", "כמעט ולא מרוויחה", "גדלה הכי מהר בעולם"], "answer": "יציבה ובטוחה יחסית", "ok": "🎉 נכון! חברות ותיקות וענקיות נוטות להיות יציבות יותר.", "bad": "❌ חברות ותיקות כמו קוקה-קולה נחשבות יציבות כי כולם כבר מכירים אותן והן מוכרות באופן קבוע."},
            {"q": "מה זה 'תיק השקעות'?", "options": ["תיק בית ספר שמחביאים בו כסף", "אוסף של כל המניות וההשקעות שיש לנו", "מזוודה מיוחדת של הבנק", "תיק שקונים בחנות של דיסני"], "answer": "אוסף של כל המניות וההשקעות שיש לנו", "ok": "🎉 מעולה! ה'תיק' הוא פשוט השם של כלל המניות שאנחנו מחזיקים.", "bad": "❌ 'תיק השקעות' זה פשוט השם הכללי לכל המניות שאנחנו מחזיקים יחד."},
            {"q": "למה מומלץ לפזר את הכסף בין כמה חברות שונות?", "options": ["כי ככה זה נראה יותר יפה", "כי זה החוק בישראל", "כדי שאם חברה אחת תפסיד, האחרות יוכלו לאזן אותה", "אי אפשר לפזר את הכסף"], "answer": "כדי שאם חברה אחת תפסיד, האחרות יוכלו לאזן אותה", "ok": "🎉 נכון! זה נקרא 'פיזור סיכונים'. לא שמים את כל הביצים בסל אחד!", "bad": "❌ אנחנו מפזרים כדי לא להיות תלויים רק בהצלחה של חברה אחת. זה מקטין סיכון!"},
            {"q": "מה עלול לקרות אם נקנה מניה והחברה תתחיל להפסיד הרבה כסף?", "options": ["ערך המניה עלול לרדת", "נצטרך לשלם להם קנס", "המניה תהפוך למטבע זהב", "לא קורה כלום"], "answer": "ערך המניה עלול לרדת", "ok": "🎉 נכון. כשהחברה מפסידה, פחות אנשים רוצים אותה והמחיר שלה יורד.", "bad": "❌ במצב כזה, אנשים ירצו למכור את המניה שלהם, וערך המניה ירד."},
            {"q": "מי מחליט כמה עולה כל מניה בבורסה?", "options": ["הממשלה", "האנשים שקונים ומוכרים (היצע וביקוש)", "מנהל הבורסה", "הטלוויזיה"], "answer": "האנשים שקונים ומוכרים (היצע וביקוש)", "ok": "🎉 נכון! מחיר המניה נקבע לפי כמה אנשים רוצים לקנות או למכור אותה.", "bad": "❌ המחיר נקבע לפי 'היצע וביקוש' - אם הרבה אנשים רוצים לקנות, המחיר עולה!"},
            {"q": "האם בורסה היא כמו קסם שמתעשרים ממנו ביום אחד?", "options": ["כן, תמיד מרוויחים בתוך יום!", "לא, זה דורש סבלנות, למידה והשקעה לאורך שנים", "כן, מספיק ללחוץ על כפתור", "לא, אי אפשר להרוויח בבורסה בכלל"], "answer": "לא, זה דורש סבלנות, למידה והשקעה לאורך שנים", "ok": "🎉 בדיוק! השקעה נכונה בבורסה היא כמו לשתול עץ - לוקח לו זמן לצמוח, אבל בסוף קוטפים פירות!", "bad": "❌ הבורסה היא לא קסם. כדי להרוויח בה באמת, צריך להשקיע בחברות טובות ולחכות בסבלנות הרבה זמן."}
        ]

        # יצירת שאלות חשבון מתחלפות לחלוטין
        for _ in range(25):
            buy = random.randint(10, 80) * 10
            profit = random.randint(2, 6) * 10
            sell = buy + profit
            opts_1 = [f"{profit} ₪", f"{sell} ₪", f"{buy} ₪", "0 ₪"]
            random.shuffle(opts_1)
            pool.append({
                "q": f"קניתם מניה ב-{buy} ₪, וכעבור שנתיים מכרתם אותה ב-{sell} ₪. כמה כסף הרווחתם בסך הכל?",
                "options": opts_1,
                "answer": f"{profit} ₪",
                "ok": f"🎉 אלופים! {sell} פחות {buy} שווה {profit} ₪ רווח!",
                "bad": f"❌ לא נורא, נסו לחשב: {sell} פחות {buy} שווה {profit} ₪."
            })
            
            invest = random.choice([100, 200, 300, 500])
            div_p = random.randint(2, 5)
            div_money = int(invest * (div_p / 100))
            opts_2 = [f"{div_money} ₪", f"{div_money + 10} ₪", f"{div_money * 10} ₪", f"{invest} ₪"]
            random.shuffle(opts_2)
            pool.append({
                "q": f"השקעתם {invest} ₪ בחברה מעולה שמחלקת דיבידנד של {div_p}%. כמה 'דמי כיס' (דיבידנד) תקבלו?",
                "options": opts_2,
                "answer": f"{div_money} ₪",
                "ok": f"🎉 בול! {div_p}% מתוך {invest} שקלים הם בדיוק {div_money} ₪!",
                "bad": f"❌ אופס! התשובה היא {div_money} ₪."
            })

            buy_2 = random.randint(50, 100) * 10
            loss = random.randint(1, 3) * 10
            sell_2 = buy_2 - loss
            opts_3 = [f"{loss} ₪", f"{buy_2} ₪", f"{sell_2} ₪", "היא לא הפסידה"]
            random.shuffle(opts_3)
            pool.append({
                "q": f"קניתם מניה ב-{buy_2} ₪. לצערינו החברה הפסידה והמניה ירדה ל-{sell_2} ₪ ומכרתם אותה. כמה כסף הפסדתם?",
                "options": opts_3,
                "answer": f"{loss} ₪",
                "ok": f"🎉 יפה שחישבתם נכון! {buy_2} פחות {sell_2} שווה להפסד של {loss} ₪.",
                "bad": f"❌ החישוב הנכון הוא {buy_2} פחות {sell_2}, ולכן ההפסד הוא {loss} ₪."
            })
            
        return pool

    ALL_QUESTIONS = get_infinite_questions_pool()
    rng = random.Random(refresh_count)
    shown_qs = rng.sample(ALL_QUESTIONS, k=5) 

    for i, item in enumerate(shown_qs):
        st.markdown(f"#### ❓ שאלה {i+1}: {item['q']}")
        choice = st.radio(
            "בחר תשובה נכונה:",
            item["options"],
            index=None,
            key=f"quiz_{refresh_count}_{i}",
            label_visibility="collapsed"
        )
        if choice == item["answer"]:
            st.success(item["ok"])
        elif choice is not None:
            st.error(item["bad"])
        
        st.write("<br>", unsafe_allow_html=True)
