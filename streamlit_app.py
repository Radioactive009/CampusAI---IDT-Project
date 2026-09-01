import json
import os

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CampusAI Evaluation Dashboard",
    page_icon="🎓",
    layout="wide"
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "evaluation",
    "results"
)

DATASET_FILE = os.path.join(
    BASE_DIR,
    "evaluation",
    "evaluation_dataset.json"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_json(filename):

    path = os.path.join(
        RESULTS_DIR,
        filename
    )

    if not os.path.exists(path):
        return None

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def load_dataset():

    if not os.path.exists(DATASET_FILE):
        return []

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# LOAD DATA
# ============================================================

quality_summary = load_json(
    "quality_summary.json"
)

rag_analysis = load_json(
    "rag_analysis.json"
)

rag_results = load_json(
    "rag_results.json"
)

repository_results = load_json(
    "repository_test_results.json"
)

dataset = load_dataset()


# ============================================================
# HEADER
# ============================================================

st.title("🎓 CampusAI")
st.subheader(
    "University Knowledge Assistant — Evaluation Dashboard"
)

st.caption(
    "Week 4: LLM Evaluation • Quantitative Analysis • RAG Analysis • Repository Understanding"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("CampusAI Demo")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "🏠 Overview",
        "🤖 Model Comparison",
        "📊 Quality Metrics",
        "⚡ Performance",
        "🔎 RAG Analysis",
        "🧩 Repository Understanding",
        "📝 Evaluation Dataset"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.header("CampusAI System Overview")

    st.markdown(
        """
        CampusAI is a university knowledge assistant that uses:

        - FastAPI
        - Retrieval / RAG
        - FAISS vector similarity search
        - Sentence-transformer embeddings
        - Ollama
        - Multiple local LLMs
        - Dockerized services
        """
    )

    st.divider()

    st.subheader("Application Architecture")

    st.code(
        """
                    USER
                      │
                      ▼
          ┌─────────────────────┐
          │ Application Service │
          │       :8000         │
          └──────────┬──────────┘
                     │
              ┌──────┴──────┐
              │             │
              ▼             ▼
       ┌────────────┐  ┌────────────┐
       │ Retrieval  │  │ LLM Service│
       │ Service    │  │   :8001    │
       │   :8002    │  └──────┬─────┘
       └─────┬──────┘         │
             │                ▼
             ▼             Ollama
           FAISS              │
             │                ▼
             ▼          Code Llama /
      Relevant Context       Phi /
                             StarCoder2
             │                │
             └───────┬────────┘
                     ▼
                 RESPONSE
        """,
        language="text"
    )

    st.divider()

    st.subheader("Evaluation Scope")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "LLM Models",
        "3"
    )

    col2.metric(
        "Evaluation Questions",
        "25"
    )

    col3.metric(
        "Total LLM Runs",
        "75"
    )

    col4.metric(
        "RAG Retrieval",
        "96%"
    )

    st.divider()

    st.info(
        "The same CampusAI application and the same evaluation questions "
        "were used to compare all three models."
    )


# ============================================================
# MODEL COMPARISON
# ============================================================

elif page == "🤖 Model Comparison":

    st.header("🤖 LLM Model Comparison")

    if not quality_summary:

        st.error(
            "quality_summary.json was not found."
        )

    else:

        rows = []

        for model, values in quality_summary.items():

            rows.append(
                {
                    "Model": model,
                    "Accuracy (%)":
                        values["accuracy_percent"],
                    "Hallucination (%)":
                        values[
                            "hallucination_rate_percent"
                        ],
                    "Similarity":
                        values[
                            "average_similarity"
                        ],
                    "Latency (sec)":
                        values[
                            "average_latency_seconds"
                        ],
                    "Avg Tokens":
                        values[
                            "average_total_tokens"
                        ]
                }
            )

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "Accuracy Comparison"
        )

        st.bar_chart(
            df.set_index("Model")[
                "Accuracy (%)"
            ]
        )

        st.subheader(
            "Hallucination Rate"
        )

        st.bar_chart(
            df.set_index("Model")[
                "Hallucination (%)"
            ]
        )

        st.divider()

        st.subheader(
            "Key Finding"
        )

        st.success(
            "Code Llama and Phi achieved the highest accuracy "
            "at 28%, while StarCoder2 3B achieved only 4%."
        )


# ============================================================
# QUALITY METRICS
# ============================================================

elif page == "📊 Quality Metrics":

    st.header("📊 Quality Evaluation")

    if not quality_summary:

        st.error(
            "Quality evaluation results not found."
        )

    else:

        for model, values in quality_summary.items():

            st.subheader(
                model
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Accuracy",
                f'{values["accuracy_percent"]}%'
            )

            col2.metric(
                "Hallucination",
                f'{values["hallucination_rate_percent"]}%'
            )

            col3.metric(
                "Semantic Similarity",
                values["average_similarity"]
            )

            col4.metric(
                "Questions",
                values["questions"]
            )

        st.divider()

        st.subheader(
            "How were quality metrics calculated?"
        )

        st.markdown(
            """
            **Accuracy**

            Correct answers / Total questions × 100

            **Semantic Similarity**

            Cosine similarity between the expected answer
            and the generated answer using sentence embeddings.

            **Correct**

            Similarity ≥ 0.75

            **Partially Correct**

            0.55 ≤ similarity < 0.75

            **Incorrect / Potential Hallucination**

            Similarity < 0.55

            **Hallucination Rate**

            Potentially incorrect answers / Total questions × 100
            """
        )


# ============================================================
# PERFORMANCE
# ============================================================

elif page == "⚡ Performance":

    st.header(
        "⚡ Performance & Resource Analysis"
    )

    if not quality_summary:

        st.error(
            "Evaluation results not found."
        )

    else:

        rows = []

        for model, values in quality_summary.items():

            rows.append(
                {
                    "Model": model,
                    "Latency (seconds)":
                        values[
                            "average_latency_seconds"
                        ],
                    "Average Tokens":
                        values[
                            "average_total_tokens"
                        ]
                }
            )

        df = pd.DataFrame(rows)

        st.subheader(
            "Response Latency"
        )

        st.bar_chart(
            df.set_index("Model")[
                "Latency (seconds)"
            ]
        )

        st.subheader(
            "Average Token Usage"
        )

        st.bar_chart(
            df.set_index("Model")[
                "Average Tokens"
            ]
        )

        st.divider()

        st.subheader(
            "Observed Ollama Resource Usage"
        )

        resource_df = pd.DataFrame(
            {
                "Model": [
                    "Code Llama",
                    "Phi",
                    "StarCoder2 3B"
                ],
                "Model Size / Memory": [
                    "6.3 GB",
                    "2.4 GB",
                    "2.1 GB"
                ],
                "Processor": [
                    "59% CPU / 41% GPU",
                    "100% GPU",
                    "100% GPU"
                ]
            }
        )

        st.table(
            resource_df
        )

        st.divider()

        st.warning(
            "Performance trade-off: StarCoder2 3B is the fastest "
            "and uses the fewest tokens, but has substantially "
            "lower answer quality."
        )


# ============================================================
# RAG ANALYSIS
# ============================================================

elif page == "🔎 RAG Analysis":

    st.header(
        "🔎 Retrieval-Augmented Generation Analysis"
    )

    if not rag_analysis:

        st.error(
            "RAG analysis results not found."
        )

    else:

        summary = rag_analysis[
            "summary"
        ]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Questions",
            summary[
                "total_questions"
            ]
        )

        col2.metric(
            "Relevant",
            summary[
                "relevant_retrievals"
            ]
        )

        col3.metric(
            "Partially Relevant",
            summary[
                "partially_relevant_retrievals"
            ]
        )

        col4.metric(
            "Retrieval Relevance",
            f'{summary["retrieval_relevance_percent"]}%'
        )

        st.divider()

        st.subheader(
            "Retrieval Quality"
        )

        chart_data = pd.DataFrame(
            {
                "Retrieval Quality": [
                    "Relevant",
                    "Partially Relevant",
                    "Poor"
                ],
                "Questions": [
                    summary[
                        "relevant_retrievals"
                    ],
                    summary[
                        "partially_relevant_retrievals"
                    ],
                    summary[
                        "poor_retrievals"
                    ]
                ]
            }
        )

        st.bar_chart(
            chart_data.set_index(
                "Retrieval Quality"
            )
        )

        st.divider()

        st.subheader(
            "RAG Relationship"
        )

        st.code(
            """
Question
   ↓
Query Embedding
   ↓
Vector Similarity
   ↓
Relevant Context
   ↓
LLM
   ↓
Final Response
            """,
            language="text"
        )

        st.info(
            "Retrieval relevance was 96%: 24 of 25 questions "
            "received relevant context."
        )

        st.divider()

        st.subheader(
            "RAG Cases"
        )

        if rag_analysis.get("questions"):

            questions = rag_analysis[
                "questions"
            ]

            for item in questions:

                if item[
                    "retrieval_quality"
                ] == "partially_relevant":

                    with st.expander(
                        f'Question {item["id"]} — Partial Retrieval'
                    ):

                        st.write(
                            "**Question:**",
                            item["question"]
                        )

                        st.write(
                            "**Sources:**",
                            ", ".join(
                                item["sources"]
                            )
                        )

                        st.write(
                            "**Context Coverage:**",
                            f'{item["context_coverage_percent"]}%'
                        )

                        st.write(
                            "**Expected Answer:**",
                            item[
                                "expected_answer"
                            ]
                        )

                        st.write(
                            "**LLM Answer:**",
                            item["answer"]
                        )

                        st.warning(
                            "Interesting case: retrieval was "
                            "only partially relevant, but the "
                            "LLM still produced the correct answer."
                        )

                        break


# ============================================================
# REPOSITORY UNDERSTANDING
# ============================================================

elif page == "🧩 Repository Understanding":

    st.header(
        "🧩 Repository-Level Understanding"
    )

    st.markdown(
        """
        This experiment investigates whether the current
        LLM + RAG system can understand relationships across
        application components and source files.
        """
    )

    st.divider()

    if repository_results:

        successful = sum(
            1
            for item in repository_results
            if item.get("error") is None
        )

        failed = len(
            repository_results
        ) - successful

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Repository Questions",
            len(repository_results)
        )

        col2.metric(
            "Responses",
            successful
        )

        col3.metric(
            "Service Errors",
            failed
        )

        st.divider()

        for item in repository_results:

            with st.expander(
                f'Question {item["id"]}: {item["question"]}'
            ):

                if item.get("error"):

                    st.error(
                        item["error"]
                    )

                else:

                    st.write(
                        "**LLM Answer:**"
                    )

                    st.write(
                        item.get(
                            "answer",
                            ""
                        )
                    )

                    st.write(
                        "**Retrieved Sources:**"
                    )

                    st.write(
                        ", ".join(
                            item.get(
                                "sources",
                                []
                            )
                        )
                    )

    else:

        st.warning(
            "repository_test_results.json was not found."
        )

    st.divider()

    st.subheader(
        "Finding"
    )

    st.warning(
        "The current RAG system is designed around university "
        "documents, not source-code files. Therefore it cannot "
        "reliably perform repository-level code understanding. "
        "This is a limitation that can be addressed in future "
        "work using repository-aware retrieval and semantic code navigation."
    )


# ============================================================
# DATASET
# ============================================================

elif page == "📝 Evaluation Dataset":

    st.header(
        "📝 Evaluation Dataset"
    )

    st.write(
        f"Total evaluation questions: **{len(dataset)}**"
    )

    if dataset:

        df = pd.DataFrame(
            dataset
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "Questions by Category"
        )

        category_counts = (
            df["category"]
            .value_counts()
        )

        st.bar_chart(
            category_counts
        )

    else:

        st.error(
            "Evaluation dataset not found."
        )