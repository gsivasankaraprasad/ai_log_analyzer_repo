
import ollama


def analyze_errors(error_messages):
    """
    Analyze application errors using local Ollama AI.
    """

    if error_messages.empty:
        return "No errors found in the application logs."

    # Convert all available error columns into text.
    error_text = error_messages.to_string(index=False)

    prompt = f"""
You are an experienced DevOps engineer
and application support expert.

Analyze these application log errors:

{error_text}

Provide your analysis under these headings:

1. Error Summary
2. Possible Root Cause
3. Recommended Solution
4. Troubleshooting Steps
5. Prevention Recommendations

Explain everything in simple language.
Do not claim a root cause is certain unless
the logs provide sufficient evidence.
"""

    try:
        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as error:
        return f"AI analysis failed: {error}"
