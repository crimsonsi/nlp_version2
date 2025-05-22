import streamlit as st

def show_question(question):
    """Show the current interview question"""
    st.markdown(f"""
    <div style="
        background-color: var(--neutral-50);
        padding: var(--space-6);
        border-radius: var(--radius-lg);
        border-left: 4px solid var(--brand-primary);
        margin: var(--space-4) 0;
    ">
        <h3 style="color: var(--brand-primary); margin-bottom: var(--space-4);">
            📝 Question
        </h3>
        <p style="
            font-size: 1.1em;
            line-height: 1.6;
            color: var(--neutral-800);
            margin: 0;
        ">
            {question}
        </p>
    </div>
    """, unsafe_allow_html=True)
