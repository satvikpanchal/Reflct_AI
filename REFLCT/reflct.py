import google.generativeai as genai

# genai.configure(api_key="")

# genai.configure(api_key=os.getenv("GENAI_API_KEY"))


model = genai.GenerativeModel("gemini-2.5-pro")

def analyze_feelings(timestamp, transcript):
    prompt = f"""
            You are a calm and thoughtful assistant that reflects on voice logs spoken in English.

            Given the following transcript, do the following:

            1. Summarize what the speaker said in 1–2 sentences (in English).
            2. Identify their emotional tone (one word, e.g., sad, hopeful, stressed).
            3. Ask one self-reflection question based on what they shared.
            4. End with a short motivational message — keep it warm and encouraging.

            Transcript:
            \"\"\"
            {transcript}
            \"\"\"
            """

    response = model.generate_content(prompt)
    reflection = response.text.strip()
    
    # Save to log
    reflection_filename = f"logs/{timestamp}_reflection.txt"
    with open(reflection_filename, "w") as f:
        f.write("Transcript:\n" + transcript + "\n\nReflection:\n" + reflection)
    
    return reflection

