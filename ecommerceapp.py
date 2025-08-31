import streamlit as st
from transformers import pipeline
import time
import re

# Configure Streamlit page
st.set_page_config(
    page_title="Ecommerce Shopping Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .chat-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        animation: fadeIn 0.5s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        margin-left: 20%;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #333;
        margin-right: 20%;
    }
    
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    .title-text {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .stats-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    
    .stTextInput input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 15px 20px;
        font-size: 16px;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize the pipeline with error handling
@st.cache_resource
def load_model():
    try:
        pipe = pipeline(
            "text-generation", 
            model="Heem2/ecommerceX", 
            token="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",
            max_length=512,
            temperature=0.7,
            do_sample=True
        )
        return pipe
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Content filtering function
def filter_content(text):
    """Basic content filtering for inappropriate language"""
    inappropriate_words = ['fuck', 'shit', 'asshole', 'bitch', 'damn']
    for word in inappropriate_words:
        text = re.sub(r'\b' + re.escape(word) + r'\b', '[FILTERED]', text, flags=re.IGNORECASE)
    return text

# Initialize session state
if 'chat_history' in st.session_state:
    chat_history = st.session_state.chat_history
else:
    chat_history = []
    st.session_state.chat_history = chat_history

if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

# Main UI
st.markdown("""
<div class="title-container">
    <div class="title-text">🤖 Ecommerce Shopping Assistant</div>
    <p style="color: white; font-size: 1.2rem; margin-top: 0.5rem;">
        Powered by Hugging Face Transformers
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with stats and controls
with st.sidebar:
    st.header("📊 Chat Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <h3 style="color: #667eea; margin: 0;">{len(chat_history)}</h3>
            <p style="margin: 0; color: #666;">Total Messages</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <h3 style="color: #667eea; margin: 0;">{st.session_state.message_count}</h3>
            <p style="margin: 0; color: #666;">User Queries</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header("⚙️ Settings")
    enable_filtering = st.checkbox("Enable Content Filtering", value=True)
    max_response_length = st.slider("Max Response Length", 50, 500, 200)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.message_count = 0
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔗 Model Info")
    st.info("Model: Heem2/ecommerceX\nProvider: Hugging Face")

# Load model
pipe = load_model()

if pipe is None:
    st.error("⚠️ Failed to load the AI model. Please check your connection and token.")
    st.stop()

# Chat interface
st.header("💬 Chat Interface")

# Display chat history
chat_container = st.container()
with chat_container:
    for i, message in enumerate(chat_history):
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 AI Assistant:</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)

# Input section
st.markdown("---")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "💭 Ask me anything...",
        placeholder="Type your message here...",
        key="user_input"
    )

with col2:
    send_button = st.button("🚀 Send", type="primary")

# Handle user input
if send_button and user_input.strip():
    # Add user message to history
    chat_history.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1
    
    # Show loading spinner
    with st.spinner("🤔 AI is thinking..."):
        try:
            # Filter input if enabled
            filtered_input = filter_content(user_input) if enable_filtering else user_input
            
            # Prepare messages for the pipeline
            messages = [{"role": "user", "content": filtered_input}]
            
            # Generate response
            response = pipe(
                messages,
                max_length=max_response_length,
                num_return_sequences=1,
                pad_token_id=pipe.tokenizer.eos_token_id
            )
            
            # Extract the generated text
            if response and len(response) > 0:
                # Get the generated text (this might need adjustment based on the model's output format)
                generated_text = response[0].get('generated_text', '')
                
                # If the response contains the conversation format, extract just the assistant's response
                if isinstance(generated_text, list) and len(generated_text) > 1:
                    ai_response = generated_text[-1].get('content', 'Sorry, I could not generate a response.')
                elif isinstance(generated_text, str):
                    # Remove the input from the response if it's included
                    ai_response = generated_text.replace(filtered_input, '').strip()
                    if not ai_response:
                        ai_response = "I understand your query. How can I help you further?"
                else:
                    ai_response = "I received your message. How can I assist you?"
                
                # Filter response if enabled
                if enable_filtering:
                    ai_response = filter_content(ai_response)
                
                # Ensure response is not empty
                if not ai_response.strip():
                    ai_response = "Thank you for your message. How can I help you today?"
                    
            else:
                ai_response = "I'm sorry, I couldn't generate a response. Please try again."
            
            # Add AI response to history
            chat_history.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            error_msg = f"⚠️ Error generating response: {str(e)}"
            st.error(error_msg)
            chat_history.append({"role": "assistant", "content": "I apologize, but I encountered an error. Please try again."})
    
    # Update session state and rerun
    st.session_state.chat_history = chat_history
    st.rerun()

# Quick action buttons
st.markdown("---")
st.subheader("🚀 Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("👋 Say Hello"):
        st.session_state.user_input = "Hello! How are you today?"
        st.rerun()

with col2:
    if st.button("🛒 Product Help"):
        st.session_state.user_input = "Can you help me find a good product?"
        st.rerun()

with col3:
    if st.button("💡 Get Advice"):
        st.session_state.user_input = "Can you give me some advice?"
        st.rerun()

with col4:
    if st.button("❓ Ask Question"):
        st.session_state.user_input = "I have a question about..."
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🤖 AI Chat Assistant | Built with Streamlit & Hugging Face Transformers</p>
    <p style="font-size: 0.8rem;">This app uses the Heem2/ecommerceX model for text generation</p>
</div>
""", unsafe_allow_html=True)