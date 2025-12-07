import streamlit as st
from datetime import datetime
from tools import get_invoice_details, get_invoice_status, download_invoice_pdf
from utility import check_ollama_status
from agent import invoice_agent

MODEL_NAME = "llama3.1:8b"

st.set_page_config(
    page_title="Invoice AI Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #1E88E5;
    }
    .assistant-message {
        background-color: #F5F5F5;
        border-left: 4px solid #4CAF50;
    }
    .tool-call {
        background-color: #FFF3E0;
        border-left: 4px solid #FF9800;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .status-success {
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
    }
    .status-error {
        background-color: #FFEBEE;
        border-left: 4px solid #F44336;
    }
    .status-warning {
        background-color: #FFF3E0;
        border-left: 4px solid #FF9800;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: bold;
    }
    .sidebar-info {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

if 'agent' not in st.session_state:
    st.session_state.agent = None

with st.sidebar:
    st.markdown("### 📄 Invoice AI Assistant")
    st.markdown("---")
    
    # System Status
    st.markdown("#### 🔧 System Status")

    # ollama_status, ollama_msg = check_ollama_status()
    
    # if ollama_status:
    #     st.markdown(f'<div class="status-box status-success">{ollama_msg}</div>', unsafe_allow_html=True)
    # else:
    #     st.markdown(f'<div class="status-box status-error"> {ollama_msg}</div>', unsafe_allow_html=True)
    #     st.markdown("""
    #     **To fix:**
    #     1. Install Ollama from https://ollama.ai
    #     2. Run: `ollama serve`
    #     3. Run: `ollama pull llama3.1:8b`
    #     """)
    
    st.markdown("---")
    
    # Session Info
    st.markdown("#### Session Info")
    st.markdown(f'<div class="sidebar-info"><strong>Session ID:</strong><br/>{st.session_state.session_id}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-info"><strong>Model:</strong><br/>{MODEL_NAME}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-info"><strong>Messages:</strong> {len(st.session_state.messages)}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("#### Quick Actions")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🔄 New Session"):
        st.session_state.messages = []
        st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state.agent = None
        st.rerun()
    
    st.markdown("---")
    
    # Example Queries
    st.markdown("####  Example Queries")
    st.markdown("""
    - "Get details for invoice 1008"
    - "What's the status of invoice 1008?"
    - "Download invoice 1008 PDF"
    - "Show me invoice 1234"
    """)
    
    st.markdown("---")
    
    # About
    with st.expander("About"):
        st.markdown("""
        **Invoice AI Assistant**
        
        Powered by:
        - 🤖 Phidata Framework
        - 🦙 Local LLM (Ollama)
        - 🎨 Streamlit UI
        - 💾 MySQL Memory
        
        Version: 1.0.0
        """)

st.markdown('<div class="main-header">📄 Invoice AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your intelligent invoice management companion</div>', unsafe_allow_html=True)

# if not ollama_status:
#     st.error("⚠️ Ollama is not running or model is not available. Please check the sidebar for setup instructions.")
#     st.stop()

# Initialize agent if not already done
if st.session_state.agent is None:
    with st.spinner("🔄 Initializing AI agent..."):
        try:
            st.session_state.agent = invoice_agent(st.session_state.session_id)
            st.success("✅ Agent initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize agent: {str(e)}")
            st.stop()

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br/>{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong><br/>{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "tool":
        st.markdown(f'<div class="tool-call">🔧 <strong>Tool:</strong> {message["tool_name"]}<br/>📊 <strong>Result:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me about invoices... (e.g., 'Get details for invoice 3479')")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br/>{user_input}</div>', unsafe_allow_html=True)
    
    # Get agent response
    with st.spinner("🤔 Thinking..."):
        try:
            # Create a placeholder for streaming response
            response_placeholder = st.empty()
            full_response = ""
            
            # Get streaming response
            response = st.session_state.agent.run(user_input, stream=False)
            
            # Extract content from RunResponse
            full_response = ""
            
            if hasattr(response, 'content'):
                # It's a RunResponse object
                full_response = response.content
            elif isinstance(response, str):
                # It's already a string
                full_response = response
            else:
                # Convert to string as fallback
                full_response = str(response)

            st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong><br/>{full_response}</div>', unsafe_allow_html=True)
           
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Rerun to update the UI
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.markdown("Please check if Ollama is running and the model is available.")
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Built with using Phidata, Ollama, and Streamlit | 
</div>
""", unsafe_allow_html=True)
