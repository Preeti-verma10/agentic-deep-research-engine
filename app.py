# import streamlit as st

# from agents.research_agent import ResearchAgent
# from agents.report_agent import ReportAgent


# st.set_page_config(
#     page_title="Agentic Deep Research Engine",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ---------- Custom Theme ----------
# st.markdown("""
# <style>

# header[data-testid="stHeader"]{
#     background: transparent;
# }

# .stApp{
#     background: linear-gradient(135deg,#F5FBF8,#E8F6EF,#D7F0E6);
# }

# .main-title{
#     text-align:center;
#     color: #3E6B61;
#     font-size:48px;
#     font-weight:bold;
#     margin-top:10px;
# }

# .sub-title{
#     text-align:center;
#     color:#3E6B61;
#     font-size:20px;
#     margin-bottom:30px;
# }

# .block-container{
#     padding-top:2rem;
# }

# div[data-testid="stTextInput"] input{
#     background:#ffffff;
#     border-radius:12px;
#     border:2px solid #3b82f6;
#     color:black;
#     font-size:18px;
# }

# .stButton>button{
#     width:100%;
#     background:  #69A297;
#     color:white;
#     border:none;
#     border-radius:12px;
#     height:55px;
#     font-size:18px;
#     font-weight:bold;
# }

# .stButton>button:hover{
#     background:linear-gradient(90deg,#1d4ed8,#0891b2);
#     color:white;
# }

# [data-testid="stDownloadButton"] button{
#     width:100%;
#     background:#16a34a;
#     color:white;
#     border-radius:10px;
#     height:50px;
#     font-size:17px;
#     font-weight:bold;
# }

# div[data-testid="stExpander"]{
#     background:#f8fafc;
#     border-radius:10px;
# }

# h3{
#     color:#2563eb;
# }

# </style>
# """, unsafe_allow_html=True)

# st.markdown(
#     "<div class='main-title'>🔬 Agentic Deep Research Engine</div>",
#     unsafe_allow_html=True
# )

# st.markdown(
#     "<div class='sub-title'>AI Powered Multi-Agent Research Assistant</div>",
#     unsafe_allow_html=True
# )

# query = st.text_input(
#     "Enter your Research Topic"
# )

# if st.button("🚀 Generate Research Report"):

#     if query.strip() == "":
#         st.warning("Please enter a research topic.")

#     else:

#         with st.spinner("Researching... Please wait..."):

#             researcher = ResearchAgent()

#             result = researcher.research(query)

#             documents = result["documents"]
#             plan = result["plan"]

#             report = ReportAgent()

#             report_path = report.generate_report(
#                 query,
#                 documents,
#                 plan
#             )

#         st.success("✅ Research Completed Successfully!")

#         st.markdown("---")

#         st.subheader("📋 Research Plan")

#         for i, q in enumerate(plan["sub_questions"], start=1):
#             st.write(f"**{i}. {q}**")

#         st.markdown("---")

#         st.subheader("📚 Sources")

#         for i, doc in enumerate(documents, start=1):

#             with st.expander(f"📄 Source {i}"):

#                 st.write("**URL:**")
#                 st.write(doc["source"])

#                 st.write("**Content Preview:**")
#                 st.write(doc["content"][:600])

#         with open(report_path, "r", encoding="utf-8") as f:
#             report_text = f.read()

#         st.download_button(
#             "⬇ Download Research Report",
#             report_text,
#             file_name="final_report.md"
#         )









import streamlit as st

from agents.research_agent import ResearchAgent
from agents.report_agent import ReportAgent

st.set_page_config(
    page_title="Agentic Deep Research Engine",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Custom Theme ----------

# ---------- Custom Theme ----------

st.markdown("""
<style>

header[data-testid="stHeader"]{
    background: transparent;
}

/* Main background */
.stApp{
    background: linear-gradient(135deg,#EAF7F5,#DFF2EE,#E9F6F3);
}

/* Main title */
.main-title{
    text-align:center;
    color:#3E6D68;
    font-size:48px;
    font-weight:700;
    margin-top:10px;
    margin-bottom:0px;
}

/* Subtitle */
.sub-title{
    text-align:center;
    color:#5A7D78;
    font-size:22px;
    margin-bottom:40px;
}

.block-container{
    padding-top:2rem;
}

div[data-testid="stTextInput"] input{
    background:#ffffff;
    border-radius:12px;
    border:2px solid #3b82f6;
    color:black;
    font-size:18px;
}

.stButton>button{
    width:100%;
    background:  #69A297;
    color:white;
    border:none;
    border-radius:12px;
    height:55px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:linear-gradient(90deg,#1d4ed8,#0891b2);
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

h3{
    color:#2563eb;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 class="main-title">
🔬 Agentic Deep Research Engine
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p class="sub-title">
AI Powered Multi-Agent Research Assistant
</p>
""", unsafe_allow_html=True)


query = st.text_input(
    "Enter your Research Topic"
)

if st.button("🚀 Generate Research Report"):

    if query.strip() == "":
        st.warning("Please enter a research topic.")

    else:

        with st.spinner("Researching... Please wait..."):

            researcher = ResearchAgent()

            result = researcher.research(query)

            documents = result["documents"]
            plan = result["plan"]
            sections = result["sections"]     # ✅ Added

            report = ReportAgent()

            report_path = report.generate_report(
                query,
                documents,
                plan,
                sections                   # ✅ Added
            )

        st.success("✅ Research Completed Successfully!")

        st.markdown("---")

        st.subheader("📋 Research Plan")

        for i, q in enumerate(plan["sub_questions"], start=1):
            st.write(f"**{i}. {q}**")

        st.markdown("---")

        st.subheader("📖 Research Answers")

        for i, section in enumerate(sections, start=1):

            with st.expander(f"Question {i}: {section['question']}"):

                if section["answer"]:
                    st.write(section["answer"])
                else:
                    st.write("No answer generated.")

        st.markdown("---")

        st.subheader("📚 Sources")

        for i, doc in enumerate(documents, start=1):

            with st.expander(f"📄 Source {i}"):

                st.write("**URL:**")
                st.write(doc["source"])

                st.write("**Content Preview:**")
                st.write(doc["content"][:600])

        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()

        st.download_button(
            "⬇ Download Research Report",
            report_text,
            file_name="final_report.md"
        )