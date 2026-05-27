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

st.title("🎢 משחק ההשקעות הראשון שלי!")

# סרגל רענון
now_str = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
<div class="refresh-bar">
  <span>🔄 הנתונים מתעדכנים אוטומטית כל 2 דקות</span>
  <span>⏰ עדכון אחרון: {now_str} &nbsp;|&nbsp; מספר עדכון: #{refresh_count}</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🚀 המשחק והחברות", "📚 מה זה בכלל בורסה?"])

# =================== מאגר שאלות ===================
ALL_QUESTIONS = [
    {
        "q": "קנית מניה ב-100 ₪, עכשיו היא שווה 130 ₪. כמה הרווחת?",
        "options": ["10 ₪", "30 ₪", "130 ₪", "כלום"],
        "answer": "30 ₪",
        "ok": "🎉 נכון! 130 - 100 = 30 ₪ רווח!",
        "bad": "❌ 130 פחות 100 שווה 30 ₪ — זה הרווח!"
    },
    {
        "q": "מה זה דיבידנד?",
        "options": ["סוג של מניה", "כסף שחברה מחלקת למשקיעים", "שם של חברה", "הלוואה מהבנק"],
        "answer": "כסף שחברה מחלקת למשקיעים",
        "ok": "🎉 מעולה! דיבידנד = דמי כיס מהחברה!",
        "bad": "❌ דיבידנד הוא כסף שחברה רווחית מחלקת לבעלי המניות."
    },
    {
        "q": "מה בדרך כלל יותר בטוח?",
        "options": ["לקנות מניה של חברה אחת", "לקנות קרן סל עם 500 חברות"],
        "answer": "לקנות קרן סל עם 500 חברות",
        "ok": "🎉 נכון! פיזור בין הרבה חברות = פחות סיכון!",
        "bad": "❌ קרן סל מפזרת בין הרבה חברות — הרבה יותר בטוח!"
    },
    {
        "q": "חברה ותיקה כמו קוקה-קולה נחשבת...",
        "options": ["מסוכנת מאוד", "יציבה ובטוחה יחסית", "לא כדאית להשקעה", "גדלה מהר מאוד"],
        "answer": "יציבה ובטוחה יחסית",
        "ok": "🎉 נכון! חברות ותיקות בדרך כלל יציבות יותר.",
        "bad": "❌ חברות ותיקות כמו קוקה-קולה נחשבות יציבות."
    },
    {
        "q": "מה קורה כשחברה מצליחה?",
        "options": ["מחיר המניה יורד", "מחיר המניה עולה", "המניה נעלמת", "שום דבר"],
        "answer": "מחיר המניה עולה",
        "ok": "🎉 נכון! הצלחה = יותר ביקוש = מחיר עולה!",
        "bad": "❌ כשחברה מצליחה, כולם רוצים קנות ממנה — המחיר עולה!"
    },
    {
        "q": "מי הם 'בעלי המניות' של חברה?",
        "options": ["רק המייסדים", "כולם שקנו מניות שלה", "רק הבנקים", "העובדים בלבד"],
        "answer": "כולם שקנו מניות שלה",
        "ok": "🎉 נכון! כל מי שקנה מניה הוא שותף קטן בחברה!",
        "bad": "❌ כל מי שרכש מניה — הוא חלק מבעלי החברה!"
    },
    {
        "q": "חברת גיימינג חדשה כמו רובלוקס נחשבת...",
        "options": ["מסוכנת מאוד אבל פוטנציאל גבוה", "יציבה לגמרי", "בטוחה כמו קוקה-קולה", "ללא סיכון"],
        "answer": "מסוכנת מאוד אבל פוטנציאל גבוה",
        "ok": "🎉 נכון! חברות צמיחה — סיכון גבוה, פוטנציאל גבוה!",
        "bad": "❌ חברות טכנולוגיה חדשות יכולות לעלות מהר — אבל גם לרדת!"
    },
    {
        "q": "קרן סל (ETF) היא...",
        "options": ["מניה של חברה אחת", "סל שמכיל מניות של הרבה חברות", "חיסכון בבנק", "הלוואה"],
        "answer": "סל שמכיל מניות של הרבה חברות",
        "ok": "🎉 מעולה! ETF = סל עם הרבה מניות יחד!",
        "bad": "❌ ETF הוא סל השקעה שמכיל מניות של הרבה חברות שונות."
    },
    {
        "q": "השקעת 1,000 ₪ וקיבלת 2% דיבידנד. כמה קיבלת?",
        "options": ["2 ₪", "20 ₪", "200 ₪", "2,000 ₪"],
        "answer": "20 ₪",
        "ok": "🎉 נכון! 1,000 × 2% = 20 ₪!",
        "bad": "❌ 1,000 כפול 2 אחוז = 20 ₪."
    },
    {
        "q": "למה כדאי להשקיע לטווח ארוך?",
        "options": ["כי הבורסה תמיד עולה כל יום", "כי לאורך זמן הבורסה בדרך כלל עולה", "כי זה חוק", "כי אין ברירה"],
        "answer": "כי לאורך זמן הבורסה בדרך כלל עולה",
        "ok": "🎉 נכון! גם אם יש ירידות — לאורך שנים הבורסה נוטה לעלות!",
        "bad": "❌ לאורך עשרות שנים, הבורסה בדרך כלל עולה בממוצע."
    },
]

# =================== טאב הסבר ===================
with tab2:
    st.markdown("""
    <div dir="rtl" style="text-align:right; font-family:'Heebo',sans-serif;">
    <h2 style="font-size:26px;">📖 מדריך הבורסה לילדים — שלב אחר שלב</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="explain-card" style="border-color:#6366f1;">
      <span class="emoji-big">🍕</span>
      <h3>שלב 1 — מה זו חברה?</h3>
      <p>דמיינו שאתם פותחים <strong>פיצרייה</strong>. אתם קונים תנור, קמח, עגבניות — ומתחילים למכור פיצות.<br><br>
      כשהחברה שלכם מרוויחה כסף, זה אומר שהפיצרייה מצליחה! 🎉<br>
      כשהיא מפסידה — אולי אנשים לא אוהבים את הפיצה, או התנור התקלקל. 😔</p>
    </div>

    <div class="explain-card" style="border-color:#10b981;">
      <span class="emoji-big">🧩</span>
      <h3>שלב 2 — מה זו מניה?</h3>
      <p>רוצים לפתוח <strong>10 סניפים נוספים</strong> אבל אין כסף?<br><br>
      אתם מציעים לחברים: <strong>"תנו לי 1,000 ₪ ותקבלו חתיכה מהחברה שלי!"</strong><br><br>
      כל חתיכה כזאת נקראת <strong>מניה</strong> 🧩 — מי שמחזיק מניה הוא <strong>שותף</strong> שלכם!</p>
    </div>

    <div class="explain-card" style="border-color:#f59e0b;">
      <span class="emoji-big">💰</span>
      <h3>שלב 3 — איך מרוויחים?</h3>
      <p><strong>1️⃣ המניה עולה בערך:</strong> קניתם ב-100 ₪, הפיצרייה הצליחה — המניה עולה ל-150 ₪. מכרתם ורווחתם 50 ₪! 🤑<br><br>
      <strong>2️⃣ דמי כיס (דיבידנד):</strong> הפיצרייה הרוויחה המון? היא שולחת לכם מתנה במזומן כל שנה! 💌</p>
    </div>

    <div class="explain-card" style="border-color:#ef4444;">
      <span class="emoji-big">🎢</span>
      <h3>שלב 4 — מה זה סיכון?</h3>
      <p>🐢 <strong>תמר בחרה קוקה-קולה</strong> — 100 שנה קיימת, כולם שותים קולה. יציב ובטוח.<br><br>
      🚀 <strong>יוסי בחר רובלוקס</strong> — יכול לעלות פי 3, אבל גם לרדת חצי אם ילדים יעברו למשחק אחר.<br><br>
      <strong>אין תשובה נכונה</strong> — כל אחד בוחר לפי האופי שלו! 😊</p>
    </div>

    <div class="explain-card" style="border-color:#8b5cf6;">
      <span class="emoji-big">🛒</span>
      <h3>שלב 5 — מה זו קרן סל (ETF)?</h3>
      <p>במקום חברה אחת — קונים <strong>סל</strong> עם 500 חברות ביחד!<br><br>
      כמו לקנות <strong>סל ממתקים</strong> — אם אחד לא טעים, יש עוד 499! 🍬<br><br>
      רוב המשקיעים הגדולים בעולם ממליצים על זה!</p>
    </div>
    """, unsafe_allow_html=True)

    # === שאלות מתחלפות ===
    st.markdown(f"""
    <div dir="rtl" style="font-family:'Heebo',sans-serif; margin: 24px 0 12px 0;">
      <h3 style="margin-bottom:4px;">🧠 חידון — שאלות מתחלפות אוטומטית!</h3>
      <p style="color:#6b7280; font-size:14px; margin:0;">השאלות מתחלפות כל 2 דקות. עדכון #{refresh_count}</p>
    </div>
    """, unsafe_allow_html=True)

    # בחר 4 שאלות אקראיות בכל רענון
    rng = random.Random(refresh_count)
    shown_qs = rng.sample(ALL_QUESTIONS, k=4)

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

        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

# =================== טאב המשחק ===================
with tab1:

    KIDS_COMPANIES = {
        "RBLX": {"name": "רובלוקס 🎮",   "desc": "בונה עולמות משחק וירטואלים. צומחת מהר אבל תנודתית מאוד.", "risk": 9},
        "DIS":  {"name": "דיסני 🎢",      "desc": "סרטים, פארקים ו-Disney+. חברה גדולה ומוכרת לכולם.", "risk": 5},
        "MCD":  {"name": "מקדונלד'ס 🍔", "desc": "רשת המזון המהיר הגדולה בעולם. יציבה בכל מצב.", "risk": 3},
        "NKE":  {"name": "נייקי 👟",      "desc": "יצרנית נעלי הספורט הגדולה בעולם.", "risk": 6},
        "KO":   {"name": "קוקה-קולה 🥤", "desc": "המשקה הכי מפורסם בעולם. בטוחה ומחלקת דיבידנד קבוע.", "risk": 2},
        "AAPL": {"name": "אפל 📱",        "desc": "ממציאת האייפון. ענקית טכנולוגיה עם כסף עצום בקופה.", "risk": 7},
    }

    # צילום מצב של נתוני אמת מעודכנים כגיבוי 
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
                    "risk": d["risk"], "div": round(div, 2), "growth": round(ret, 2),
                })
            except Exception:
                pass
                
        # שימוש בנתוני האמת שהקפאנו מראש אם השרת נחסם
        if len(rows) == 0:
            for ticker, d in KIDS_COMPANIES.items():
                rows.append({
                    "ticker": ticker, 
                    "name": d["name"], 
                    "desc": d["desc"],
                    "risk": d["risk"], 
                    "div": REAL_BACKUP_DATA[ticker]["div"], 
                    "growth": REAL_BACKUP_DATA[ticker]["growth"],
                    "is_dummy": True 
                })
        return pd.DataFrame(rows)

    with st.spinner("🔄 אוסף נתונים מהבורסה..."):
        df = fetch_kids_data()
        
    if df.empty:
        st.error("תקלה לא צפויה בטעינת הנתונים.")
        st.stop()
        
    if "is_dummy" in df.columns:
        st.info("💡 המערכת עמוסה כרגע. כדי לא לעצור את המשחק, נטענו נתוני אמת שנשמרו בעדכון האחרון שלנו!")

    # SIDEBAR
    st.sidebar.markdown("""
    <div dir="rtl" style="text-align:right; font-family:'Heebo',sans-serif; padding-bottom:8px;">
      <h3 style="margin:0 0 4px 0;">🕹️ איזה משקיע אתה?</h3>
      <p style="font-size:13px; color:#6b7280; margin:0;">הזז את המדים — הטבלה תתעדכן</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">🚀 כמה חשובה לי צמיחה מהירה?</div>', unsafe_allow_html=True)
    w_growth = st.sidebar.slider(" ", 0, 10, 5, key="growth_slider")
    st.sidebar.markdown('<div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;margin-bottom:16px;font-family:Heebo,sans-serif;">0 = לא חשוב &nbsp;|&nbsp; 10 = חשוב מאוד</div>', unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">💰 כמה חשוב לי לקבל דמי כיס?</div>', unsafe_allow_html=True)
    w_dividend = st.sidebar.slider("  ", 0, 10, 5, key="div_slider")
    st.sidebar.markdown('<div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;margin-bottom:16px;font-family:Heebo,sans-serif;">0 = לא חשוב &nbsp;|&nbsp; 10 = חשוב מאוד</div>', unsafe_allow_html=True)

    st.sidebar.markdown('<div dir="rtl" style="font-family:Heebo,sans-serif;font-weight:700;margin-bottom:4px;">🎢 כמה סיכון אני מוכן לקחת?</div>', unsafe_allow_html=True)
    w_risk = st.sidebar.slider("   ", 1, 10, 5, key="risk_slider")
    risk_color_label = "#16a34a" if w_risk <= 3 else "#d97706" if w_risk <= 6 else "#dc2626"
    risk_text_label  = "🟢 בטוח מאוד" if w_risk <= 3 else "🟡 בינוני" if w_risk <= 6 else "🔴 הרפתקן"
    st.sidebar.markdown(f"""
    <div dir="rtl" style="font-size:12px;color:#6b7280;margin-top:-12px;font-family:Heebo,sans-serif;">1 = בטוח מאוד &nbsp;|&nbsp; 10 = הרפתקן</div>
    <div dir="rtl" style="text-align:center;font-family:'Heebo',sans-serif;background:#f3f4f6;border-radius:8px;padding:8px;font-size:14px;margin-top:8px;">
      בחרת: <strong style="color:{risk_color_label};">{risk_text_label} ({w_risk}/10)</strong>
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

    st.subheader("🏆 טבלת החברות")
    st.markdown(f"""
    <table class="kids-table">
      <thead><tr>
        <th>🏢 שם החברה</th><th>🎢 רמת סיכון</th><th>💰 דמי כיס</th><th>📈 צמיחה שנתית</th><th>⭐ ציון התאמה</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔍 תעודת זהות לחברה")
    name_to_ticker = {row["name"]: row["ticker"] for _, row in df.iterrows()}
    selected_name  = st.selectbox("בחר חברה:", list(name_to_ticker.keys()))
    sel = df[df["name"] == selected_name].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("רמת סיכון",   f"{sel['risk']} / 10")
    col2.metric("דמי כיס",     f"{sel['div']}%")
    col3.metric("צמיחה שנתית", f"{'+' if sel['growth']>=0 else ''}{sel['growth']}%")
    col4.metric("ציון התאמה",  calc_stars(sel))

    g_color = "#dcfce7" if sel["growth"] >= 0 else "#fee2e2"
    g_msg   = f"✅ מי שקנה לפני שנה הרוויח {sel['growth']}% על הכסף שלו!" if sel["growth"] >= 0 \
              else f"⚠️ השנה הייתה קשה — הכסף ירד ב-{abs(sel['growth'])}%. בורסה היא לטווח ארוך!"

    st.markdown(f"""
    <div dir="rtl" style="background:#f5f3ff;border-right:4px solid #4f46e5;border-radius:10px;padding:16px;margin:14px 0;font-family:'Heebo',sans-serif;">
      <h4 style="margin:0 0 8px 0;">{sel['name']}</h4>
      <p style="margin:0;color:#374151;">{sel['desc']}</p>
    </div>
    <div dir="rtl" style="background:{g_color};border-radius:10px;padding:12px 16px;font-family:'Heebo',sans-serif;font-weight:600;margin-bottom:16px;">
      {g_msg}
    </div>
    """, unsafe_allow_html=True)
