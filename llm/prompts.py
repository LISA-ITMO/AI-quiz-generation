# Note: Precise formatting of spacing and indentation of the prompt template is important,
# as it is highly sensitive to whitespace changes. For example, it could have problems generating
# a summary from the pieces of context if the spacing is not done correctly

qa_template = """Act as a teacher. Come up with a quiz assessment test.

Course materials: {context}
Question: {question}

Helpful answer:
"""
