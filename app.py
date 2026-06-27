import streamlit as st

from agents.research_agent import ResearchAgent
from agents.report_agent import ReportAgent
from agents.answer_agent import AnswerAgent


st.set_page_config(
    page_title="Agentic Deep Research Engine",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# --------------------------------------------------
# Sidebar Chat History
# --------------------------------------------------

with st.sidebar:

    st.title("💬 Chat History")

    if st.button("🗑 Clear History"):

        st.session_state.chat_history = []
        st.session_state.last_result = None

        st.rerun()

    st.markdown("---")

    if len(st.session_state.chat_history) == 0:

        st.info("No previous conversations.")

    else:

        for i, chat in enumerate(
            reversed(st.session_state.chat_history),
            start=1
        ):

            with st.expander(chat["question"]):

                st.write(chat["answer"])

# --------------------------------------------------
# Theme
# --------------------------------------------------

st.markdown("""
<style>

header[data-testid="stHeader"]{
    background:transparent;
}

.stApp{
    background:linear-gradient(
        135deg,
        #EAF7F5,
        #DFF2EE,
        #E9F6F3
    );
}

.main-title{

    text-align:center;
    color:#3E6D68;
    font-size:48px;
    font-weight:700;

    margin-top:10px;
    margin-bottom:0px;
}

.sub-title{

    text-align:center;
    color:#5A7D78;
    font-size:22px;
    margin-bottom:35px;
}

.block-container{
    padding-top:2rem;
}

div[data-testid="stTextInput"] input{

    background:white;

    border-radius:12px;

    border:2px solid #3b82f6;

    color:black;

    font-size:18px;
}

.stButton>button{

    width:100%;

    height:55px;

    border:none;

    border-radius:12px;

    background:#69A297;

    color:white;

    font-size:18px;

    font-weight:bold;
}

.stButton>button:hover{

    background:linear-gradient(
        90deg,
        #1d4ed8,
        #0891b2
    );

    color:white;
}

[data-testid="stDownloadButton"] button{

    width:100%;

    background:#16a34a;

    color:white;

    border-radius:10px;

    height:50px;

    font-size:17px;

    font-weight:bold;
}

div[data-testid="stExpander"]{

    background:#f8fafc;

    border-radius:10px;
}

</style>
""",
unsafe_allow_html=True)

st.markdown("""
<h1 class="main-title">
🔬 Agentic Deep Research Engine
</h1>
""",
unsafe_allow_html=True)

st.markdown("""
<p class="sub-title">
AI Powered Multi-Agent Research Assistant
</p>
""",
unsafe_allow_html=True)

# --------------------------------------------------
# User Query
# --------------------------------------------------

query = st.text_input(
    "Enter your Research Topic"
)

if st.button(
    "🚀 Generate Research Report"
):

    if query.strip() == "":

        st.warning(
            "Please enter a research topic."
        )

    else:

        with st.spinner(
            "Researching... Please wait..."
        ):

            researcher = ResearchAgent()

            result = researcher.research(query)

            st.session_state.last_result = result

            report = ReportAgent()

            report.generate_report(

                query,

                result["documents"],

                result["plan"],

                result["sections"]

            )

            st.session_state.chat_history.append({

                "question": query,

                "answer": result["final_answer"],

                "result": result

            })

            st.rerun()
# --------------------------------------------------
# Display Results
# --------------------------------------------------

if st.session_state.last_result is not None:

    result = st.session_state.last_result

    documents = result["documents"]
    plan = result["plan"]
    sections = result["sections"]
    final_answer = result["final_answer"]

    st.success("✅ Research Completed Successfully!")

    # ------------------------------------------
    # Final Answer
    # ------------------------------------------

    st.subheader("🤖 Final Answer")

    st.write(final_answer)

    st.markdown("---")

    # ------------------------------------------
    # Research Plan
    # ------------------------------------------

    st.subheader("📋 Research Plan")

    for i, question in enumerate(
        plan["sub_questions"],
        start=1
    ):

        st.write(f"**{i}. {question}**")

    st.markdown("---")

    # ------------------------------------------
    # Detailed Answers
    # ------------------------------------------

    st.subheader("📖 Research Details")

    for i, section in enumerate(
        sections,
        start=1
    ):

        with st.expander(
            f"Question {i}: {section['question']}"
        ):

            st.write(section["answer"])

    st.markdown("---")

    # ------------------------------------------
    # Sources
    # ------------------------------------------

    st.subheader("📚 Sources")

    for i, doc in enumerate(
        documents,
        start=1
    ):

        with st.expander(
            f"📄 Source {i}"
        ):

            st.write("**URL**")

            st.write(doc["source"])

            st.write("**Content Preview**")

            st.write(
                doc["content"][:700]
            )

    st.markdown("---")

    # ------------------------------------------
    # Download Report
    # ------------------------------------------

    report = ReportAgent()

    report_path = report.generate_report(

        plan["original_query"],

        documents,

        plan,

        sections

    )

    with open(
        report_path,
        "r",
        encoding="utf-8"
    ) as file:

        report_text = file.read()

    st.download_button(

        "⬇ Download Research Report",

        report_text,

        file_name="final_report.md"

    )

    st.markdown("---")

    # ------------------------------------------
    # Follow-up Questions
    # ------------------------------------------

    st.subheader("💭 Ask a Follow-up Question")

    followup = st.text_input(

        "Ask another question about this research",

        key="followup_box"

    )

    if st.button("Send Follow-up"):

        if followup.strip() == "":

            st.warning(
                "Please enter a follow-up question."
            )

        else:

            answer_agent = AnswerAgent()

            answer = answer_agent.answer_followup(

                st.session_state.chat_history,

                followup

            )

            st.session_state.chat_history.append({

                "question": followup,

                "answer": answer

            })

            st.success("Answer")

            st.write(answer)

            st.rerun()
            