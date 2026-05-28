import streamlit as st
import yfinance as yf
import pandas as pd
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="בורסה לילדים", layout="wide", initial_sidebar_state="collapsed")

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
[data-testid="stSlider"] { direction: ltr !important; }
[data-testid="stRadio"] { direction: rtl !important; text-align: right !important; }

/* ====== תיקון סיידבר לנייד ====== */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        width: 80vw !important;
        max-width: 320px !important;
        min-width: unset !important;
        position: fixed !important;
        z-index: 999 !important;
        height: 100vh !important;
        top: 0 !important;
    }
    [data-testid="stSidebar"][aria-expanded="true"] {
        box-shadow: 4px 0 24px rgba(0,0,0,0.35) !important;
    }
    .main .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        max-width: 100vw !important;
    }
}
/* ================================= */

.stTabs [data-baseweb="tab-list"] { direction: rtl !important; gap: 6px; }
.stTabs [data-baseweb="tab"] { font-size: 17px !important; font-weight: 700 !important; font-family: 'Heebo', sans-serif !important; }

div.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white; border-radius: 12px; border: none; padding: 12px;
    font-size: 18px; font-weight: 700; width: 100%; margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(245, 158, 11, 0.3);
}
div.stButton > button:hover { background: linear-gradient(135deg, #d97706 0%, #b45309 100%); color: white; border: none; }

.table-wrapper { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; direction: rtl; margin-bottom: 20px;}
.kids-table {
    width: 100%; border-collapse: collapse; min-width: 650px; font-size: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-radius: 10px; overflow: hidden;
}
.kids-table th { background: #4f46e5; color: white; padding: 12px; text-align: right !important; font-weight: 700; white-space: nowrap; }
.kids-table td { padding: 12px; text-align: right !important; border-bottom: 1px solid #eee; background: white; vertical-align: middle; white-space: nowrap; }
.kids-table tr:nth-child(even) td { background: #f8fafc; }
.risk-badge { padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white; }

.info-box { background: #f8fafc; padding: 15px; border-radius: 12px; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.metric-box { padding: 15px; border-radius: 12px; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;}
</style>
""", unsafe_allow_html=True)

# =================== מאגר חברות ===================
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
    "MAT": {"name": "מאטל 🏎️", "desc": "יצרנית הצעצועים הענקית.", "products": "ברבי, מכוניות הוט-ווילס (Hot Wheels) ומשחק הקלפים טאקי/אונו.", "fun_fact": "בובת הברבי הראשונה בעולם עלתה רק 3 דולר!", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Mattel_logo.svg/200px-Mattel_logo.svg.png", "risk": 7}
}

FULL_BACKUP_DATA = {k: {"div": random.uniform(0, 4), "growth": random.uniform(-20, 50)} for k in FULL_KIDS_COMPANIES.keys()}

if "active_tickers" not in st.session_state:
    st.session_state.active_tickers = random.sample(list(FULL_KIDS_COMPANIES.keys()), 6)

# =================== Header ===================
st.info("🦉 **היי חברים! אני שוקי הינשוף!** \n\n אני כאן כדי לעזור לכם להבין איך הבורסה עובדת. מוכנים לצאת להרפתקה ולגלות איך החברות הכי גדולות בעולם עושות כסף?")

now_str = datetime.now().strftime("%H:%M:%S")
st.success(f"🔄 **הנתונים מתעדכנים אוטומטית מהבורסה** | ⏰ עדכון אחרון: {now_str}")

if st.button("🎲 שוקי, תביא חברות חדשות!", use_container_width=True):
    st.session_state.active_tickers = random.sample(list(FULL_KIDS_COMPANIES.keys()), 6)

tab1, tab2 = st.tabs(["🚀 המשחק והחברות", "📚 הבורסה של שוקי"])

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

        if len(rows) == 0:
            for ticker in tickers:
                d = FULL_KIDS_COMPANIES[ticker]
                rows.append({
                    "ticker": ticker, "name": d["name"], "desc": d["desc"],
                    "products": d["products"], "fun_fact": d["fun_fact"], "image": d["image"],
                    "risk": d["risk"], "div": round(FULL_BACKUP_DATA[ticker]["div"], 2),
                    "growth": round(FULL_BACKUP_DATA[ticker]["growth"], 2), "is_dummy": True
                })
        return pd.DataFrame(rows)

    with st.spinner("🔄 שוקי אוסף נתונים..."):
        df = fetch_kids_data(tuple(st.session_state.active_tickers))

    if "is_dummy" in df.columns:
        st.warning("💡 המערכת עמוסה. נטענו נתוני גיבוי כדי שלא נפסיק לשחק!")

    # =================== סיידבר ===================
    st.sidebar.markdown("""
    <div dir="rtl" style="text-align:right; font-family:'Heebo',sans-serif; padding-top:10px;">
    <h3 style="margin:10px 0 4px 0;">🕹️ איזה משקיע אתה?</h3>
    <p style="font-size:13px; color:#6b7280; margin:0 0 15px 0;">הזז את המדים כדי להתאים את הציונים אליך!</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">🚀 כמה חשובה לי צמיחה מהירה?</div>', unsafe_allow_html=True)
    w_growth = st.sidebar.slider(" ", 0, 10, 5, key="growth_slider")

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;margin-top:10px;">💰 כמה חשוב לי לקבל דמי כיס?</div>', unsafe_allow_html=True)
    w_dividend = st.sidebar.slider("  ", 0, 10, 5, key="div_slider")

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;margin-top:10px;">🎢 כמה סיכון אני מוכן לקחת?</div>', unsafe_allow_html=True)
    w_risk = st.sidebar.slider("   ", 1, 10, 5, key="risk_slider")

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
        <td><strong>{row['name']}</strong></td>
        <td><span class="risk-badge" style="background:{risk_color(row['risk'])};">{risk_label(row['risk'])} ({row['risk']}/10)</span></td>
        <td>{row['div']}%</td>
        <td class="{g_cls}">{g_sign}{row['growth']}%</td>
        <td style="font-size:16px;">{stars}</td>
        </tr>"""

    st.subheader("🏆 טבלת החברות להשקעה")
    st.markdown(f"""
    <div class="table-wrapper">
        <table class="kids-table">
            <thead><tr><th>🏢 שם החברה</th><th>🎢 רמת סיכון</th><th>💰 דמי כיס (%)</th><th>📈 צמיחה השנה</th><th>⭐ התאמה</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔍 תעודת זהות לחברה")
    name_to_ticker = {row["name"]: row["ticker"] for _, row in df.iterrows()}
    selected_name = st.selectbox("בחרו חברה כדי ללמוד עליה ולחשב רווחים:", list(name_to_ticker.keys()))
    sel = df[df["name"] == selected_name].iloc[0]

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(sel['image'], width=80)
    with col2:
        st.markdown(f"## {sel['name']}")
        st.caption(f"התאמה אישית אליך: {calc_stars(sel)}")

    st.write("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='info-box'><h4 style='color:#3b82f6; margin-top:0;'>🏢 מה החברה עושה?</h4>{sel['desc']}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='info-box'><h4 style='color:#d97706; margin-top:0;'>🛒 מה מוכרים שם?</h4>{sel['products']}</div>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#f0fdfa; padding:15px; border-radius:12px; margin-bottom:20px;'><h4 style='color:#0d9488; margin-top:0;'>💡 הידעת?</h4>{sel['fun_fact']}</div>", unsafe_allow_html=True)

    risk_dots = ("🔴" * sel['risk']) + ("⚪" * (10 - sel['risk']))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-box' style='background:#f3f4f6;'><b>מד סיכון</b><br><span style='font-size:24px;'>{sel['risk']}/10</span><br><span style='font-size:12px;'>{risk_dots}</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box' style='background:#f3f4f6;'><b>דמי כיס (דיבידנד)</b><br><span style='font-size:24px;'>{sel['div']}%</span><br><span style='font-size:12px;'>לשנה</span></div>", unsafe_allow_html=True)
    with col3:
        bg_col = "#dcfce7" if sel['growth'] >= 0 else "#fee2e2"
        text_col = "#166534" if sel['growth'] >= 0 else "#991b1b"
        st.markdown(f"<div class='metric-box' style='background:{bg_col};'><b>צמיחה אחרונה</b><br><span style='font-size:24px; color:{text_col}; font-weight:bold;'>{'+' if sel['growth']>=0 else ''}{sel['growth']}%</span></div>", unsafe_allow_html=True)

    # =================== מחשבון ===================
    st.markdown("---")
    st.subheader(f"🧮 מחשבון השקעות — כמה יהיה לנו בעתיד?")

    calc_type = st.radio("איך נרצה להשקיע?", ["השקעה פעם אחת היום", "חסכון קבוע (לשים קצת כל חודש)"], horizontal=True)
    amount = st.number_input("סכום בשקלים:", min_value=10, max_value=10000, value=100, step=10)

    if "פעם אחת" in calc_type:
        total_invested = amount
        total_profit = amount * (sel['growth'] / 100)
    else:
        total_invested = amount * 12
        total_profit = total_invested * (sel['growth'] / 100) / 2

    final_amount = total_invested + total_profit
    profit_text = "הרווח הצפוי" if total_profit >= 0 else "ההפסד הצפוי"
    profit_color = "#16a34a" if total_profit >= 0 else "#dc2626"

    st.write(f"נניח שנשקיע לפי התכנית שלנו, והחברה תגדל בשנה הקרובה בדיוק כמו שהיא גדלה בשנה שעברה. הנה התוצאה:")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-box' style='border:1px solid #e2e8f0;'><b>הכנסנו לקופה:</b><br><span style='font-size:26px;'>{total_invested:,.0f} ₪</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-box' style='border:1px solid #e2e8f0; border-bottom: 4px solid {profit_color};'><b>{profit_text}:</b><br><span style='font-size:26px; color:{profit_color};'>{abs(total_profit):,.0f} ₪</span></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-box' style='background:#1e293b; color:white;'><b>בעוד שנה יהיה לנו:</b><br><span style='font-size:26px;'>{final_amount:,.0f} ₪</span></div>", unsafe_allow_html=True)

    # =================== מכונת הזמן ===================
    st.markdown("---")
    st.subheader(f"🕰️ מכונת הזמן של {sel['name']}")
    st.write("במקום להסתכל על גרף מסובך, בואו נראה מה קרה למחיר של החברה בשנה האחרונה:")

    try:
        hist = yf.Ticker(sel["ticker"]).history(period="1y")
        if not hist.empty:
            min_price = hist["Close"].min()
            max_price = hist["Close"].max()
            curr_price = hist["Close"].iloc[-1]

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='metric-box' style='background:#eff6ff; border:2px dashed #bfdbfe;'>📉<br><b>הכי זול שהיה</b><br><span style='font-size:22px; color:#2563eb;'>${min_price:.0f}</span></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='metric-box' style='background:#fdf4ff; border:2px dashed #fbcfe8;'>⛰️<br><b>הכי יקר שהיה</b><br><span style='font-size:22px; color:#db2777;'>${max_price:.0f}</span></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='metric-box' style='background:#f0fdf4; border:2px dashed #bbf7d0;'>🚩<br><b>המחיר היום</b><br><span style='font-size:22px; color:#16a34a;'>${curr_price:.0f}</span></div>", unsafe_allow_html=True)

            if curr_price >= max_price * 0.9:
                verdict = "וואו! החברה נמצאת ממש קרוב לשיא שלה. כולם רוצים לקנות אותה עכשיו!"
            elif curr_price <= min_price * 1.1:
                verdict = "החברה עברה שנה לא קלה, והמחיר שלה עכשיו נמוך מאוד. משקיעים חכמים אולי יחשבו שזו 'מכירת חיסול'!"
            else:
                verdict = "החברה נמצאת איפשהו באמצע הדרך, עם עליות וירידות נורמליות."

            st.info(f"🦉 **השורה התחתונה של שוקי:** {verdict}")
    except Exception:
        st.warning("שוקי לא הצליח להפעיל את מכונת הזמן כרגע.")

# =================== טאב הסבר וחידון ===================
with tab2:
    st.header("📖 המדריך של שוקי הינשוף לבורסה")

    st.info("### 🍋 שלב 1 — מה זו בכלל חברה?\nתחשבו שפתחתם בקיץ **דוכן לימונדה** שכונתי. אם הרבה אנשים קונים מכם — הדוכן מרוויח כסף ומצליח! 🎉 חברות ענקיות כמו אפל עובדות בדיוק ככה, רק בגדול.")
    st.video("https://www.youtube.com/watch?v=Kz6pG1Y4L1s")

    st.success("### 🧩 שלב 2 — מה זו בעצם מניה?\nרוצים לפתוח **עוד 10 דוכנים** אבל אין כסף? אתם אומרים לחברים: 'תנו לי קצת כסף, ובתמורה אתן לכם חתיכה מהדוכן שלי!'. כל חתיכה כזאת נקראת **מניה**.")
    st.video("https://www.youtube.com/watch?v=R9_W7z1RpsU")

    st.warning("### 💰 שלב 3 — איך מרוויחים מזה כסף?\n**1️⃣ צמיחה:** אם החברה מצליחה, כולם רוצים את ה'חתיכות' שלה. המחיר עולה ותוכלו למכור ברווח! 🤑\n**2️⃣ דיבידנד:** כשהחברה מרוויחה המון, היא מחלקת לשותפים מזומן ישר לחשבון! 💌")
    st.video("https://www.youtube.com/watch?v=e_K0XqQz7-s")

    st.markdown("---")
    st.subheader("🧠 החידון של שוקי הינשוף! (אינסוף שאלות)")
    st.write("בואו נבדוק מה למדנו! השאלות מתחלפות בכל פעם שהטיימר מגיע לאפס:")

    def get_infinite_questions_pool():
        pool = [
            {"q": "מה זה דיבידנד?", "options": ["סוג של מניה", "כסף שחברה מחלקת למשקיעים", "שם של חברה", "הלוואה מהבנק"], "answer": "כסף שחברה מחלקת למשקיעים", "ok": "🎉 מעולה! דיבידנד הוא כמו דמי כיס שהחברה מחלקת!", "bad": "❌ דיבידנד הוא כסף מזומן שחברה רווחית מחלקת למי שקנה את המניות שלה."},
            {"q": "מה בדרך כלל יותר בטוח?", "options": ["לקנות מניה של חברה אחת בלבד", "לקנות קרן סל שכוללת המון חברות"], "answer": "לקנות קרן סל שכוללת המון חברות", "ok": "🎉 נכון! פיזור בין הרבה חברות = פחות סיכון!", "bad": "❌ כשקונים הרבה חברות יחד (קרן סל) הסיכון יורד כי אנחנו לא תלויים רק בחברה אחת."},
            {"q": "למה מומלץ לפזר את הכסף בין כמה חברות שונות?", "options": ["כי ככה זה נראה יותר יפה", "כי זה החוק בישראל", "כדי שאם חברה אחת תפסיד, האחרות יוכלו לאזן אותה", "אי אפשר לפזר את הכסף"], "answer": "כדי שאם חברה אחת תפסיד, האחרות יוכלו לאזן אותה", "ok": "🎉 נכון! זה נקרא 'פיזור סיכונים'. לא שמים את כל הביצים בסל אחד!", "bad": "❌ אנחנו מפזרים כדי לא להיות תלויים רק בהצלחה של חברה אחת. זה מקטין סיכון!"},
            {"q": "מה עלול לקרות אם נקנה מניה והחברה תתחיל להפסיד הרבה כסף?", "options": ["ערך המניה עלול לרדת", "נצטרך לשלם להם קנס", "המניה תהפוך למטבע זהב", "לא קורה כלום"], "answer": "ערך המניה עלול לרדת", "ok": "🎉 נכון. כשהחברה מפסידה, פחות אנשים רוצים אותה והמחיר שלה יורד.", "bad": "❌ במצב כזה, אנשים ירצו למכור את המניה שלהם, וערך המניה ירד."},
            {"q": "האם בורסה היא כמו קסם שמתעשרים ממנו ביום אחד?", "options": ["כן, תמיד מרוויחים בתוך יום!", "לא, זה דורש סבלנות, למידה והשקעה לאורך שנים", "כן, מספיק ללחוץ על כפתור", "לא, אי אפשר להרוויח בבורסה בכלל"], "answer": "לא, זה דורש סבלנות, למידה והשקעה לאורך שנים", "ok": "🎉 בדיוק! השקעה נכונה בבורסה היא כמו לשתול עץ - לוקח לו זמן לצמוח, אבל בסוף קוטפים פירות!", "bad": "❌ הבורסה היא לא קסם. כדי להרוויח בה באמת, צריך להשקיע בחברות טובות ולחכות בסבלנות הרבה זמן."}
        ]

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

    if "quiz_questions" not in st.session_state or st.session_state.get("last_refresh") != refresh_count:
        st.session_state.quiz_questions = random.sample(get_infinite_questions_pool(), k=5)
        st.session_state.last_refresh = refresh_count

    for i, item in enumerate(st.session_state.quiz_questions):
        st.markdown(f"#### ❓ שאלה {i+1}: {item['q']}")
        choice = st.radio("בחר תשובה:", item["options"], index=None, key=f"quiz_{st.session_state.last_refresh}_{i}", label_visibility="collapsed")

        if choice == item["answer"]:
            st.success(item["ok"])
        elif choice is not None:
            st.error(item["bad"])
        st.write("<br>", unsafe_allow_html=True)
