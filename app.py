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

h1, h2, h3, h4, h5, h6 {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}
.stMarkdown p, .stMarkdown li {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}
[data-testid="stSidebar"] .stMarkdown { direction: rtl !important; text-align: right !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] p {
    direction: rtl !important; text-align: right !important; font-family: 'Heebo', sans-serif !important;
}
[data-testid="stSlider"] { direction: ltr !important; }
.stTabs [data-baseweb="tab-list"] { direction: rtl !important; gap: 6px; }
.stTabs [data-baseweb="tab"] { font-size: 17px !important; font-weight: 700 !important; font-family: 'Heebo', sans-serif !important; }
[data-testid="metric-container"] { text-align: right !important; }

/* עיצוב לדמות של שוקי הינשוף */
.mascot-card {
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    border-radius: 20px; padding: 20px 30px;
    display: flex; align-items: center; gap: 25px;
    margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    border: 3px solid #7dd3fc;
}
.mascot-emoji { font-size: 80px; line-height: 1; }
.mascot-text h2 { margin: 0 0 10px 0; color: #0369a1; font-size: 28px; }
.mascot-text p { margin: 0; color: #0c4a6e; font-size: 18px; line-height: 1.5; font-weight: 600; }

.explain-card {
    background: white; border-radius: 16px; padding: 24px 28px;
    margin-bottom: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    direction: rtl; text-align: right; font-family: 'Heebo', sans-serif;
    border-right: 6px solid #4f46e5;
}
.explain-card h3 { margin: 0 0 10px 0; font-size: 22px; }
.explain-card p  { margin: 0; font-size: 16px; line-height: 1.8; color: #374151; }
.explain-card .emoji-big { font-size: 48px; margin-bottom: 10px; display: block; }

.quiz-card {
    background: #fefce8; border-radius: 16px; padding: 20px 24px;
    margin-bottom: 16px; border: 2px dashed #fbbf24;
    direction: rtl; text-align: right; font-family: 'Heebo', sans-serif;
}
.quiz-card h4 { color: #92400e; margin: 0 0 8px 0; font-size: 17px; }

.refresh-bar {
    background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px;
    padding: 8px 16px; margin-bottom: 16px; direction: rtl;
    font-family: 'Heebo', sans-serif; font-size: 13px; color: #166534;
    display: flex; justify-content: space-between; align-items: center;
}

.kids-table {
    width: 100%; border-collapse: collapse; direction: rtl;
    font-family: 'Heebo', sans-serif; font-size: 15px;
    margin-top: 10px; border-radius: 12px; overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.kids-table thead tr { background: #4f46e5; color: white; }
.kids-table th { padding: 12px 16px; text-align: right !important; font-weight: 700; font-size: 14px; }
.kids-table tbody tr { background: white; }
.kids-table tbody tr:nth-child(even) { background: #f8f8ff; }
.kids-table tbody tr:hover { background: #ede9fe; }
.kids-table td { padding: 11px 16px; text-align: right !important; border-bottom: 1px solid #e5e7eb; vertical-align: middle; }
.risk-badge { display: inline-block; padding: 3px 10px; border-radius: 99px; font-weight: 700; font-size: 13px; color: white; }
.positive { color: #16a34a; font-weight: 700; }
.negative { color: #dc2626; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# דמות המלווה - שוקי הינשוף
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

# סרגל רענון
now_str = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
<div class="refresh-bar">
  <span>🔄 הנתונים מתעדכנים אוטומטית מהבורסה</span>
  <span>⏰ עדכון אחרון: {now_str}</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🚀 המשחק והחברות", "📚 הבורסה של שוקי"])

# =================== מאגר שאלות ===================
ALL_QUESTIONS = [
    {"q": "קנית מניה ב-100 ₪, עכשיו היא שווה 130 ₪. כמה הרווחת?", "options": ["10 ₪", "30 ₪", "130 ₪", "כלום"], "answer": "30 ₪", "ok": "🎉 נכון! 130 - 100 = 30 ₪ רווח!", "bad": "❌ 130 פחות 100 שווה 30 ₪ — זה הרווח!"},
    {"q": "מה זה דיבידנד?", "options": ["סוג של מניה", "כסף שחברה מחלקת למשקיעים", "שם של חברה", "הלוואה מהבנק"], "answer": "כסף שחברה מחלקת למשקיעים", "ok": "🎉 מעולה! דיבידנד = דמי כיס מהחברה!", "bad": "❌ דיבידנד הוא כסף שחברה רווחית מחלקת לבעלי המניות."},
    {"q": "מה בדרך כלל יותר בטוח?", "options": ["לקנות מניה של חברה אחת", "לקנות קרן סל עם 500 חברות"], "answer": "לקנות קרן סל עם 500 חברות", "ok": "🎉 נכון! פיזור בין הרבה חברות = פחות סיכון!", "bad": "❌ קרן סל מפזרת בין הרבה חברות — הרבה יותר בטוח!"},
    {"q": "חברה ותיקה כמו קוקה-קולה נחשבת...", "options": ["מסוכנת מאוד", "יציבה ובטוחה יחסית", "לא כדאית להשקעה", "גדלה מהר מאוד"], "answer": "יציבה ובטוחה יחסית", "ok": "🎉 נכון! חברות ותיקות בדרך כלל יציבות יותר.", "bad": "❌ חברות ותיקות כמו קוקה-קולה נחשבות יציבות."}
]

# =================== טאב הסבר ===================
with tab2:
    st.markdown("""
    <div dir="rtl" style="text-align:right; font-family:'Heebo',sans-serif;">
    <h2 style="font-size:26px;">📖 המדריך של שוקי הינשוף לבורסה</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="explain-card" style="border-color:#6366f1;">
      <span class="emoji-big">🍕</span>
      <h3>שלב 1 — איך מתחילה חברה?</h3>
      <p>דמיינו שפתחתם <strong>פיצרייה</strong>. קניתם תנור, קמח ועגבניות, והתחלתם למכור פיצות.<br><br>
      אם הרבה אנשים באים לקנות — הפיצרייה שלכם מרוויחה כסף ומצליחה! 🎉<br>
      אם קשה לכם למכור — הפיצרייה עלולה להפסיד. בעולם האמיתי, חברות כמו מקדונלד'ס או דיסני פועלות בדיוק ככה, רק בגדול!</p>
    </div>

    <div class="explain-card" style="border-color:#10b981;">
      <span class="emoji-big">🧩</span>
      <h3>שלב 2 — מה זו בעצם מניה?</h3>
      <p>נניח שהפיצה שלכם כל כך טעימה, שאתם רוצים לפתוח <strong>עוד 10 סניפים!</strong> אבל... אין לכם מספיק כסף כדי לבנות אותם.<br><br>
      מה עושים? אתם מציעים לאנשים: <strong>"תנו לי קצת כסף כדי שאפתח עוד סניפים, ובתמורה אתן לכם חתיכה קטנה מהחברה שלי!"</strong><br><br>
      כל חתיכה כזאת נקראת <strong>מניה</strong>. כשאתם קונים מניה של 'אפל', אתם הופכים ל<strong>שותפים</strong> קטנטנים בחברה שמייצרת את האייפון!</p>
    </div>

    <div class="explain-card" style="border-color:#f59e0b;">
      <span class="emoji-big">💰</span>
      <h3>שלב 3 — איך המשקיעים מרוויחים?</h3>
      <p>מי שקנה מכם מניה יכול להרוויח בשתי דרכים:<br><br>
      <strong>1️⃣ המניה נהיית שווה יותר (צמיחה):</strong> אם החברה מצליחה מאוד, כולם ירצו לקנות את ה"חתיכות" שלה. המחיר שלהן יעלה, ותוכלו למכור את המניה שלכם בהרבה יותר ממה שקניתם אותה! 🤑<br><br>
      <strong>2️⃣ דמי כיס (דיבידנד):</strong> לפעמים, כשחברה מרוויחה המון כסף, היא אומרת "תודה" לשותפים שלה ומחלקת להם חלק מהרווחים במזומן ישר לחשבון. אנחנו קוראים לזה דיבידנד! 💌</p>
    </div>
    """, unsafe_allow_html=True)

    # === שאלות מתחלפות ===
    st.markdown(f"""
    <div dir="rtl" style="font-family:'Heebo',sans-serif; margin: 24px 0 12px 0;">
      <h3 style="margin-bottom:4px;">🧠 החידון של שוקי הינשוף!</h3>
      <p style="color:#6b7280; font-size:14px; margin:0;">בואו נבדוק מה למדנו עד עכשיו:</p>
    </div>
    """, unsafe_allow_html=True)

    rng = random.Random(refresh_count)
    shown_qs = rng.sample(ALL_QUESTIONS, k=2)

    for i, item in enumerate(shown_qs):
        st.markdown(f"""
        <div class="quiz-card">
          <h4>❓ שאלה {i+1}: {item['q']}</h4>
        </div>
        """, unsafe_allow_html=True)

        choice = st.radio(
            item["q"],
            item["options"],
            index=None,
            key=f"quiz_{refresh_count}_{i}",
            label_visibility="collapsed"
        )
        if choice == item["answer"]:
            st.success(item["ok"])
        elif choice is not None:
            st.error(item["bad"])
        st.write("")

# =================== טאב המשחק ===================
with tab1:

    KIDS_COMPANIES = {
        "RBLX": {
            "name": "רובלוקס 🎮", 
            "desc": "פלטפורמה ענקית שבה ילדים יכולים לבנות משחקים בעצמם ולשחק עם חברים מכל העולם.",
            "products": "עולמות וירטואליים, כסף משחק (Robux) ופריטים לדמויות.",
            "fun_fact": "בכל יום נכנסים לרובלוקס מעל 60 מיליון שחקנים — יותר מכל האנשים שגרים באיטליה!",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Roblox_player_icon_black.svg/120px-Roblox_player_icon_black.svg.png",
            "risk": 9
        },
        "DIS": {
            "name": "דיסני 🎢", 
            "desc": "חברת הבידור הגדולה בעולם שיוצרת חוויות קסומות לילדים ולמשפחות.",
            "products": "סרטים (מארוול, פיקסאר, מלחמת הכוכבים), פארקי שעשועים, ובובות.",
            "fun_fact": "הדמות הראשונה שוולט דיסני צייר לא הייתה מיקי מאוס, אלא ארנב בשם אוסוולד!",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Disney_wordmark.svg/200px-Disney_wordmark.svg.png",
            "risk": 5
        },
        "MCD": {
            "name": "מקדונלד'ס 🍔", 
            "desc": "רשת המסעדות הגדולה והמוכרת ביותר בעולם.",
            "products": "המבורגרים, צ'יפס, גלידות וארוחות ילדים (Happy Meal).",
            "fun_fact": "מקדונלד'ס היא למעשה חברת הצעצועים הגדולה בעולם, בזכות ההפתעות שהיא מחלקת בארוחות הילדים!",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png",
            "risk": 3
        },
        "NKE": {
            "name": "נייקי 👟", 
            "desc": "יצרנית בגדי ונעלי הספורט הגדולה בעולם, שמלבישה את הספורטאים המפורסמים ביותר.",
            "products": "נעלי כדורסל (כמו ג'ורדן), בגדי ספורט וכדורים.",
            "fun_fact": "הסמל המפורסם של נייקי (ה'סווש') עוצב על ידי סטודנטית שהרוויחה עליו רק 35 דולר!",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Logo_NIKE.svg/200px-Logo_NIKE.svg.png",
            "risk": 6
        },
        "KO": {
            "name": "קוקה-קולה 🥤", 
            "desc": "המשקה המתוק המפורסם והנמכר ביותר בהיסטוריה.",
            "products": "קוקה קולה, פאנטה, ספרייט, מים מינרלים ומיצים.",
            "fun_fact": "המתכון הסודי של קוקה-קולה שמור בתוך כספת מיוחדת וענקית באטלנטה, ארה\"ב!",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Coca-Cola_logo.svg/200px-Coca-Cola_logo.svg.png",
            "risk": 2
        },
        "AAPL": {
            "name": "אפל 📱", 
            "desc": "ענקית הטכנולוגיה שממציאה את רוב המכשירים החכמים שאנחנו אוהבים.",
            "products": "אייפון, אייפד, שעוני אפל, אוזניות ואפליקציות.",
            "fun_fact": "בשעות הראשונות של אפל, המייסדים שלה (סטיב ג'ובס וסטיב ווזניאק) נאלצו למכור את המכונית והמחשבון שלהם כדי שיהיה להם כסף להתחיל!",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/100px-Apple_logo_black.svg.png",
            "risk": 7
        },
    }

    REAL_BACKUP_DATA = {
        "RBLX": {"div": 0.0, "growth": 35.2},
        "DIS":  {"div": 0.0, "growth": -9.8},
        "MCD":  {"div": 2.4, "growth": 11.5},
        "NKE":  {"div": 1.6, "growth": -17.4},
        "KO":   {"div": 3.0, "growth": 6.2},
        "AAPL": {"div": 0.5, "growth": 26.8}
    }

    @st.cache_data(ttl=120)
    def fetch_kids_data():
        rows = []
        for ticker, d in KIDS_COMPANIES.items():
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
            for ticker, d in KIDS_COMPANIES.items():
                rows.append({
                    "ticker": ticker, 
                    "name": d["name"], 
                    "desc": d["desc"],
                    "products": d["products"],
                    "fun_fact": d["fun_fact"],
                    "image": d["image"],
                    "risk": d["risk"], 
                    "div": REAL_BACKUP_DATA[ticker]["div"], 
                    "growth": REAL_BACKUP_DATA[ticker]["growth"],
                    "is_dummy": True 
                })
        return pd.DataFrame(rows)

    with st.spinner("🔄 שוקי הינשוף אוסף נתונים מהבורסה..."):
        df = fetch_kids_data()
        
    if df.empty:
        st.error("תקלה לא צפויה בטעינת הנתונים.")
        st.stop()
        
    if "is_dummy" in df.columns:
        st.info("💡 המערכת של הבורסה קצת עמוסה כרגע. כדי שנוכל להמשיך לשחק, נטענו נתוני אמת קפואים מהעדכון האחרון!")

    # SIDEBAR
    st.sidebar.markdown("""
    <div dir="rtl" style="text-align:right; font-family:'Heebo',sans-serif; padding-bottom:8px;">
      <h3 style="margin:0 0 4px 0;">🕹️ איזה משקיע אתה?</h3>
      <p style="font-size:13px; color:#6b7280; margin:0;">הזז את המדים כדי להתאים את הציונים אליך!</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">🚀 כמה חשובה לי צמיחה מהירה?</div>', unsafe_allow_html=True)
    w_growth = st.sidebar.slider(" ", 0, 10, 5, key="growth_slider")
    st.sidebar.markdown('<div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;margin-bottom:16px;font-family:Heebo,sans-serif;">0 = לא אכפת לי &nbsp;|&nbsp; 10 = הכי חשוב לי בעולם!</div>', unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">💰 כמה חשוב לי לקבל דמי כיס?</div>', unsafe_allow_html=True)
    w_dividend = st.sidebar.slider("  ", 0, 10, 5, key="div_slider")
    st.sidebar.markdown('<div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;margin-bottom:16px;font-family:Heebo,sans-serif;">0 = לא אכפת לי &nbsp;|&nbsp; 10 = הכי חשוב לי בעולם!</div>', unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">🎢 כמה סיכון אני מוכן לקחת?</div>', unsafe_allow_html=True)
    w_risk = st.sidebar.slider("   ", 1, 10, 5, key="risk_slider")
    risk_color_label = "#16a34a" if w_risk <= 3 else "#d97706" if w_risk <= 6 else "#dc2626"
    risk_text_label  = "🟢 בטוח ורגוע" if w_risk <= 3 else "🟡 קצת מכל דבר" if w_risk <= 6 else "🔴 אני אוהב רכבות הרים!"
    st.sidebar.markdown(f"""
    <div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;font-family:Heebo,sans-serif;">1 = רק דברים בטוחים &nbsp;|&nbsp; 10 = אוהב להסתכן!</div>
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

    st.subheader("🏆 טבלת החברות הגדולות")
    st.markdown(f"""
    <table class="kids-table">
      <thead><tr>
        <th>🏢 שם החברה</th><th>🎢 רמת סיכון</th><th>💰 דמי כיס (ב-%)</th><th>📈 צמיחה השנה</th><th>⭐ ציון התאמה</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔍 תעודת זהות לחברה")
    name_to_ticker = {row["name"]: row["ticker"] for _, row in df.iterrows()}
    selected_name  = st.selectbox("בחרו חברה כדי ללמוד עליה דברים מגניבים:", list(name_to_ticker.keys()))
    sel = df[df["name"] == selected_name].iloc[0]

    # יצירת מד סיכון ויזואלי (נקודות צבעוניות)
    risk_dots = ("🔴" * sel['risk']) + ("⚪" * (10 - sel['risk']))

    st.markdown(f"""
    <div dir="rtl" style="background:white; border: 2px solid #e5e7eb; border-radius:15px; padding:25px; margin-top: 15px; font-family:'Heebo',sans-serif; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px dashed #e5e7eb; padding-bottom: 15px;">
            <div>
                <h2 style="margin:0 0 5px 0; color:#111827; font-size: 32px;">{sel['name']} ({sel['ticker']})</h2>
                <span style="background-color: #f3f4f6; padding: 5px 12px; border-radius: 20px; font-weight: 600; color: #4b5563; font-size: 14px;">מדד התאמה אישי: {calc_stars(sel)}</span>
            </div>
            <img src="{sel['image']}" style="height: 60px; object-fit: contain;">
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
            <div style="background: #f8fafc; padding: 15px; border-radius: 10px;">
                <h4 style="margin:0 0 10px 0; color:#3b82f6;">🏢 מה החברה הזו עושה?</h4>
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
            <div style="flex: 1; background: #f3f4f6; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; color: #6b7280; margin-bottom: 5px; font-weight: 700;">מד סיכון</div>
                <div style="font-size: 18px; margin-bottom: 5px;">{sel['risk']} / 10</div>
                <div style="font-size: 12px;">{risk_dots}</div>
            </div>
            <div style="flex: 1; background: #f3f4f6; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; color: #6b7280; margin-bottom: 5px; font-weight: 700;">דמי כיס (דיבידנד)</div>
                <div style="font-size: 24px; font-weight: 700; color: #111827;">{sel['div']}%</div>
                <div style="font-size: 12px; color: #4b5563;">כסף שמקבלים לחשבון</div>
            </div>
            <div style="flex: 1; background: {'#dcfce7' if sel['growth'] >= 0 else '#fee2e2'}; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; color: #6b7280; margin-bottom: 5px; font-weight: 700;">בכמה המניה צמחה השנה?</div>
                <div style="font-size: 24px; font-weight: 700; color: {'#166534' if sel['growth'] >= 0 else '#991b1b'};">
                    {'+' if sel['growth']>=0 else ''}{sel['growth']}%
                </div>
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
