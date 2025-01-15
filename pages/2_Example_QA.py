import streamlit as st
from pathlib import Path

# Set page config
st.set_page_config(page_title="Example Q&A", page_icon="❓", layout="wide")

st.title("Example Q&A Session")

# Load example question from markdown file
try:
    question_path = Path("inputs/qa-question.md")
    if question_path.exists():
        with open(question_path, "r") as f:
            example_question = f.read().strip()
    else:
        example_question = "Error: Question file not found."
except Exception as e:
    example_question = f"Error loading question: {str(e)}"


# Display the example Q&A session
st.markdown("### Example Question & Answer Session")

# Display user question
with st.chat_message("user"):
    st.markdown(example_question)

# Display assistant response
with st.chat_message("assistant"):
    # Path to the markdown file containing the answer
    # For now using a placeholder message until the actual markdown file is specified
    try:
        answer_path = Path("inputs/qa-answer.md")
        if answer_path.exists():
            with open(answer_path, "r") as f:
                answer_content = f.read()
        else:
            answer_content = """
            > Note: This is a placeholder answer. Please create an `example_answer.md` file with the actual response.
            
            The actual answer will be loaded from a markdown file that you specify. For now, this is just a placeholder message.
            """
    except Exception as e:
        answer_content = f"Error loading answer: {str(e)}"

    st.markdown(answer_content)

# Add some context about this example
st.markdown(
    """
---
### About this Example

This page demonstrates a sample interaction with the Optimizely VAS Chat assistant. The question and answer shown above:
- Represents a typical user query
- Shows the format and depth of responses you can expect
- Serves as a reference for how to effectively use the chat interface

You can try asking similar questions in the main chat interface!
"""
)
