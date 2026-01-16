import streamlit as st
import google.generativeai as genai
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Judul aplikasi
st.title("💬 Gemini Chatbot")
st.caption("Clone chatbot menggunakan Google Gemini API")

# Sidebar untuk API Key
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    api_key = st.text_input("Gemini API Key", type="password", 
                            help="Masukkan API key dari Google AI Studio")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ### Cara mendapatkan API Key:
    1. Kunjungi [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Buat API key baru
    3. Copy dan paste di atas
    """)

# Inisialisasi session state untuk menyimpan history chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan history chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari user
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    # Cek apakah API key sudah diisi
    if not api_key:
        st.error("⚠️ Silakan masukkan API Key terlebih dahulu di sidebar!")
        st.stop()
    
    # Tambahkan pesan user ke history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Tampilkan response dari Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Konfigurasi Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Buat context dari history chat
            chat_history = []
            for msg in st.session_state.messages[:-1]:  # Exclude pesan terakhir
                chat_history.append({
                    "role": msg["role"],
                    "parts": [msg["content"]]
                })
            
            # Generate response
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt)
            
            # Tampilkan response
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Tambahkan response ke history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_message
            })

# Informasi tambahan di sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**Total Pesan:** {len(st.session_state.messages)}")
    
    if len(st.session_state.messages) > 0:
        st.info("💡 Tips: Gunakan tombol 'Clear Chat History' untuk memulai percakapan baru")
