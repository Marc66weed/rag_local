# interface.py
import streamlit as st
from app import PaperAssistant 

st.set_page_config(page_title="AI研究助手", layout="centered")

# --- 強力樣式修正：白底黑字、移除 ICON ---
st.markdown("""
    <style>
    /* 1. 全域背景與基礎文字顏色 */
    .stApp { 
        background-color: #FFFFFF !important; 
    }
    
    /* 2. 強制所有文字、標題、Markdown 內容為黑色 */
    h1, h2, h3, p, span, li, label, div, strong { 
        color: #000000 !important; 
    }
    
    /* 3. 對話框樣式：使用淺灰區隔，文字黑，移除頭像空間 */
    [data-testid="stChatMessage"] {
        background-color: #F8F9FA !important; 
        border: 1px solid #E9ECEF !important;
        border-radius: 10px !important;
        margin-bottom: 12px !important;
        color: #000000 !important;
    }
    
    /* 4. 徹底隱藏頭像 (ICON) */
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    
    /* 5. 調整內容邊距，填補 ICON 消失後的空隙 */
    .stChatMessageContent { 
        margin-left: 0rem !important; 
    }
    
    /* 6. 輸入框內文字顏色 */
    .stChatInput textarea { 
        color: #000000 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

if "assistant" not in st.session_state:
    with st.status("正在本篇學術大腦...", expanded=True) as status:
        # 指向你的感測器論文
        target_path = r"C:\rag_local\paper\sensors-24-01869.pdf"
        st.session_state.assistant = PaperAssistant(target_path)
        status.update(label="系統已就緒", state="complete")

st.title("論文研究助理")

# 顯示抓取到的論文資訊
st.info(f"📄 **標題**：{st.session_state.assistant.full_title}\n\n👤 **作者群**：{st.session_state.assistant.authors}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示歷史紀錄：以標籤文字區分發言者
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        role_tag = "**你：**" if message["role"] == "user" else "**助手：**"
        st.markdown(role_tag)
        st.markdown(message["content"])

# 處理輸入
if prompt := st.chat_input("請詢問論文問題..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown("**你：**")
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("正在精確掃描論文內容..."):
            # 呼叫你 app.py 內部的邏輯大腦
            response = st.session_state.assistant.ask(prompt)
            st.markdown("**助手：**")
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})