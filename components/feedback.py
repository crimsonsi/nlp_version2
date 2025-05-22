import streamlit as st

def show_feedback(score, feedback):
    """Show feedback for the current answer"""
    # Determine color based on score
    if score >= 8:
        color = "var(--success)"
        emoji = "🎉"
    elif score >= 6:
        color = "var(--warning)"
        emoji = "👍"
    else:
        color = "var(--error)"
        emoji = "💡"
    
    st.markdown(f"""
    <div style="
        background-color: var(--neutral-50);
        padding: var(--space-6);
        border-radius: var(--radius-lg);
        border-left: 4px solid {color};
        margin: var(--space-4) 0;
    ">
        <h3 style="color: {color}; margin-bottom: var(--space-4);">
            {emoji} Feedback
        </h3>
        <div style="margin-bottom: var(--space-4);">
            <h4 style="color: var(--neutral-700); margin-bottom: var(--space-2);">
                Score: {score}/10
            </h4>
            <div style="
                background-color: var(--neutral-100);
                padding: var(--space-4);
                border-radius: var(--radius-md);
            ">
                <p style="
                    font-size: 1.1em;
                    line-height: 1.6;
                    color: var(--neutral-800);
                    margin: 0;
                ">
                    {feedback}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
