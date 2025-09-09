import streamlit as st
import asyncio 
import os
from config.openai_model_client import get_model_client
from config.docker_utils import getDockerCommandLineExecutor, start_docker_container, stop_docker_container
from team.analyzer_gpt import getDataAnalyzerTeam
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult


st.set_page_config(page_title="Analyzer GPT", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
        :root {
            --bg1: #f0f4f8;
            --bg2: #d9e2ec;
            --bg3: #bcccdc;
            --card-bg: #ffffff;
            --muted: #6c757d;
            --brand: #007bff;
            --accent: #28a745;
        }
        .stApp {
            background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 50%, var(--bg3) 100%);
            color: #212529; /* dark text for light background */
        }
        /* Make Streamlit header match background (remove white bar) */
        header[data-testid="stHeader"] {
            background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 50%, var(--bg3) 100%) !important;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }
        /* Some Streamlit builds add a decoration strip - match it */
        div[data-testid="stDecoration"] {
            background: transparent !important;
        }
        /* Center content and widen page */
        .block-container {
            max-width: 1100px;
            padding-top: 0.6rem; /* tighter top spacing */
            padding-bottom: 4rem;
        }
        /* Hero header */
        .hero {
            background: linear-gradient(180deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.02) 100%);
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 16px;
            padding: 28px 28px 22px 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            backdrop-filter: blur(6px);
            color: #212529;
            margin-bottom: 1rem;
        }
        .hero .title {
            font-size: 1.9rem;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .hero .subtitle {
            margin-top: 6px;
            color: #495057;
        }
        /* Glass card */
        .glass-card {
            background: var(--card-bg);
            border-radius: 14px;
            border: 1px solid rgba(0,0,0,0.1);
            box-shadow: 0 8px 24px rgba(0,0,0,0.05);
            padding: 14px 16px;
            margin: 10px 0 14px;
            color: #212529;
        }
        /* Chat input spacing */
        [data-testid="stChatInput"] {
            margin-top: 6px;
        }
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            color: #212529 !important;
            background: rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.1);
        }
        [data-testid="stChatInput"] textarea::placeholder,
        [data-testid="stChatInput"] input::placeholder {
            color: #6c757d !important;
        }
        .stAlert {
            background: rgba(255, 243, 205, 0.8) !important;
            border: 1px solid #ffe58f !important;
            color: #856404 !important;
            border-radius: 10px;
        }
        .stAlert p {
            color: #856404 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero header
st.markdown(
        """
        <div class="hero">
            <div class="title">📊 Analyzer GPT — Digital Data Analyzer</div>
            <div class="subtitle">Upload a CSV and chat your analysis requests. We'll write and run the code for you.</div>
        </div>
        """,
        unsafe_allow_html=True,
)

# Sidebar UI
with st.sidebar:
    st.markdown("<div class='sidebar-card'><h4>ℹ️ About this app</h4><p>Analyzer GPT lets you upload a CSV and ask questions. It generates Python code, runs it in Docker, and returns results and charts saved as <code>output.png</code>.</p></div>", unsafe_allow_html=True)

cols = st.columns([1,2,1])
with cols[1]:
    st.markdown("<div class='glass-card' style='text-align:center'><h4>📁 Drag & drop your CSV</h4><p>Supported: .csv</p></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader('Upload CSV file', type='csv', label_visibility='collapsed', accept_multiple_files=False)

# Session state and chat input
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'autogen_team_state' not in st.session_state:
    st.session_state['autogen_team_state'] = None

task = st.chat_input("Ask a question about your CSV…")

# Stream the analyzer team and render chat
async def run_analyzer_gpt(docker, openai_model_client, task_text: str):
    try:
        await start_docker_container(docker)
        team = getDataAnalyzerTeam(docker, openai_model_client)

        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)

        async for message in team.run_stream(task=task_text):
            if isinstance(message, TextMessage):
                msg = f"{message.source}: {message.content}"
                print(msg)
                # Render in chat UI
                if msg.startswith('user'):
                    with st.chat_message('user', avatar="🧑"):
                        st.markdown(msg)
                elif msg.startswith('Data_Analyzer_Agent'):
                    with st.chat_message('assistant', avatar="🤖"):
                        st.markdown(msg)
                elif msg.startswith('CodeExecutor'):
                    with st.chat_message('assistant', avatar="💻"):
                        st.markdown(msg)
                st.session_state.messages.append(msg)
            elif isinstance(message, TaskResult):
                stop_msg = f"Stop Reason : {message.stop_reason}"
                print(stop_msg)
                st.markdown(stop_msg)
                st.session_state.messages.append(stop_msg)
        st.session_state.autogen_team_state = await team.save_state()
    except Exception as e:
        print(e)
        return str(e)
    finally:
        await stop_docker_container(docker)

# Replay chat history
if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(msg)

if task:
    if uploaded_file is not None and task:
        if not os.path.exists('temp'):
            os.makedirs('temp')
        with open('temp/data.csv', 'wb') as f:
            f.write(uploaded_file.getbuffer())
    
    openai_model_client=get_model_client()
    docker= getDockerCommandLineExecutor()

    error=asyncio.run(run_analyzer_gpt(docker,openai_model_client,task))
    
    if error:
        st.error(f"Error occurred: {error}")
    if os.path.exists('temp/output.png'):
        st.image('temp/output.png',caption='Analysis File')
else:
    st.warning("Please upload a CSV file and enter a task.")