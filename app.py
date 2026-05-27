import streamlit as st
import yfinance as yf
import pandas as pd

# הגדרת תצורת הדף 
st.set_page_config(page_title="בורסה לילדים", layout="wide")

# החלת עיצוב בעברית + תיקון הבאג של המדים (סליידרים)
st.markdown("""
    <style>
    .stApp, .block-container, [data-testid="stSidebar"] { direction: rtl; }
    p, div, span, h1, h2, h3, h4, h5, h6, label { text-align: right !important; }
    [data-testid="stDataFrame"] { direction: rtl; }
    th, td { text-align: right !important; }
    .stTabs [data-baseweb="tab-list"] { display: flex; justify-content: flex-start; direction: rtl; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; font-weight: bold; }
    
    /* התיקון למדים - משאיר אותם משמאל לימין כדי שיעבדו טוב, אבל הטקסט מימין לשמאל */
    [data-testid="stSlider"] { direction: ltr !important; }
    [data-testid="stSlider"] label { direction: rtl !important; text-align: right !important; display: block; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🎢 משחק ההשקעות הראשון שלי!")
st.write("בואו ללמוד איך הכסף יכול לעבוד בשבילנו!")

# יצירת לשוניות (Tabs)
tab1, tab2 = st.tabs(["🚀 המשחק והחברות", "📚 מה זה בכלל בורסה?"])

with tab2:
    st.header("מה זה שוק ההון (הבורסה)? הסבר פשוט!")
    st.markdown("""
    ### 🍕 תארו לעצמכם שיש לכם פיצרייה...
    נניח שפתחתם פיצרייה קטנה וכולם אוהבים את הפיצה שלכם. אתם רוצים לפתוח עוד 10 סניפים, אבל אין לכם מספיק כסף. 
    אתם מציעים לאנשים: *"תנו לי קצת כסף, ובתמורה אתן לכם חתיכה מהחברה שלי!"*
    
    ### 🧩 מה זו בעצם 'מניה'?
    **מניה** היא כמו משולש של פיצה. כשאתם קונים מניה של חברה (כמו אפל או דיסני), אתם בעצם קונים חתיכה קטנטנה מהחברה הזו והופכים ל"שותפים" בה.
    
    ### 💰 איך מרוויחים מזה כסף?
    1. **הפיצה נהיית שווה יותר:** אם החברה מצליחה, כולם רוצים לקנות את החתיכות שלה. המחיר של החתיכה שלכם (המניה) עולה, ותוכלו למכור אותה ביותר כסף!
    2. **דמי כיס (דיבידנד):** חברות שמרוויחות המון כסף אומרות למשקיעים: *"בגלל שאתם שותפים שלנו, קבלו חלק מהרווחים במזומן!"*
    """)

with tab1:
    # מאגר חברות, עכשיו עם רמת סיכון מוגדרת (1 הכי בטוח, 10 הכי מסוכן/תנודתי)
    KIDS_COMPANIES = {
        "RBLX": {"name": "רובלוקס 🎮", "desc": "בונה עולמות משחק ווירטואלים. חברה טכנולוגית שצומחת מהר, אבל גם המחיר שלה קופץ למעלה ולמטה.", "risk": 9},
        "DIS": {"name": "דיסני 🎢", "desc": "מייצרת סרטים ופארקים. חברה גדולה ומוכרת, אבל לפעמים אנשים הולכים פחות לקולנוע.", "risk": 5},
        "MCD": {"name": "מקדונלד'ס 🍔", "desc": "רשת המזון המהיר הגדולה בעולם. נחשבת לחברה מאוד יציבה שמוכרת אוכל בכל מצב.", "risk": 3},
        "NKE": {"name": "נייקי 👟", "desc": "יצרנית בגדי ונעלי הספורט הגדולה בעולם.", "risk": 6},
        "KO": {"name": "קוקה-קולה 🥤", "desc": "המשקה המפורסם בעולם. חברה ותיקה מאוד ובטוחה שמחלקת דמי כיס קבועים.", "risk": 2},
        "AAPL": {"name": "אפל 📱", "desc": "ממציאת האייפון. ענקית טכנולוגיה חזקה מאוד עם המון כסף בקופה.", "risk": 7}
    }

    @st.cache_data(ttl=3600)
    def fetch_kids_data():
        data_list = []
        for ticker, details in KIDS_COMPANIES.items():
            try:
                asset = yf.Ticker(ticker)
                info = asset.info
                hist = asset.history(period="1y")
                
                return_1y = 0.0
                if len(hist) > 1:
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    return_1y = ((end_price - start_price) / start_price) * 100

                div_yield = (info.get('dividendYield') or 0.0) * 100 
                
                data_list.append({
                    "סמל": ticker,
                    "שם החברה": details["name"],
                    "רמת סיכון": details["risk"],
                    "דמי כיס (דיבידנד ב-%)": round(div_yield, 2),
                    "כמה הכסף גדל השנה? (%)": round(return_1y, 2),
                    "סיפור החברה": details["desc"]
                })
            except Exception as e:
                pass
        return pd.DataFrame(data_list)

    with st.spinner("אוסף נתונים מהבורסה..."):
        df = fetch_kids_data()

    if not df.empty:
        st.sidebar.header("🕹️ איזה סוג משקיעים אתם?")
        st.sidebar.write("הזיזו את המדים כדי לבחור מה חשוב לכם:")
        
        # שלושת המדים (סליידרים) - כולל מד סיכון!
        w_growth = st.sidebar.slider("🚀 אני רוצה חברות שצומחות מהר", 0, 10, 5)
        w_dividend = st.sidebar.slider("💰 אני אוהב/ת לקבל 'דמי כיס'", 0, 10, 5)
        w_risk = st.sidebar.slider("🎢 מד סיכון: כמה אני מוכן להסתכן?", 1, 10, 5)
        
        total_w = w_growth + w_dividend + 5 # משקל קבוע לסיכון כדי שלא נאפס חלוקה באפס

        scores = []
        for idx, row in df.iterrows():
            ret = row["כמה הכסף גדל השנה? (%)"]
            s_growth = min(max(ret, 0), 100)
            
            div = row["דמי כיס (דיבידנד ב-%)"]
            s_div = min(div * 30, 100) 
            
            # חישוב מדד הסיכון: אם הילד בחר סיכון גבוה, חברות מסוכנות יקבלו ניקוד טוב יותר. 
            # אם בחר סיכון נמוך, חברות יציבות יקבלו ניקוד טוב יותר.
            comp_risk = row["רמת סיכון"]
            s_risk = 100 - (abs(comp_risk - w_risk) * 10) 
            s_risk = max(s_risk, 0)
            
            final_score = ((s_growth * w_growth) + (s_div * w_dividend) + (s_risk * 5)) / total_w
            
            stars = round(final_score / 20)
            stars = max(1, min(stars, 5)) 
            scores.append("⭐" * stars)
            
        df["מדד הכוכבים שלנו"] = scores
        
        st.subheader("🏆 טבלת החברות הגדולות")
        display_cols = ["סמל", "שם החברה", "רמת סיכון", "דמי כיס (דיבידנד ב-%)", "כמה הכסף גדל השנה? (%)", "מדד הכוכבים שלנו"]
        st.dataframe(df[display_cols], use_container_width=True)

        st.markdown("---")
        st.subheader("🔍 תעודת זהות לחברה")
        
        selected_ticker = st.selectbox("בחרו חברה כדי ללמוד עליה עוד:", df["סמל"].tolist())
        
        if selected_ticker:
            asset_info = df[df["סמל"] == selected_ticker].iloc[0]
            
            st.info(f"### {asset_info['שם החברה']}")
            st.write(f"**מה החברה הזו עושה?** {asset_info['סיפור החברה']}")
            st.write(f"**מדד הסיכון שלה:** {asset_info['רמת סיכון']} מתוך 10.")
            st.write(f"**האם היא מביאה מתנות?** היא חילקה השנה {asset_info['דמי כיס (דיבידנד ב-%)']}% כדמי כיס למשקיעים שלה.")
            
            if asset_info['כמה הכסף גדל השנה? (%)'] > 0:
                st.success(f"**מה קרה למי שקנה אותה לפני שנה?** הוא הרוויח! הכסף שלו גדל ב-{asset_info['כמה הכסף גדל השנה? (%)']}%.")
            else:
                st.error(f"**מה קרה למי שקנה אותה לפני שנה?** השנה הייתה קצת קשה, והכסף ירד ב-{abs(asset_info['כמה הכסף גדל השנה? (%)'])}%.")