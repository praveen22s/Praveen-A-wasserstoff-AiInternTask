import httpx
import os
from dotenv import load_dotenv
import re # Import re if you removed it earlier

print(">>> Loading ai_client.py module <<<")
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

async def ask_gemini(seed: str, guess: str, persona: str = "cheery") -> str:
    prompt = (
        f"Does a {guess} beat {seed}? "
        f"Explain creatively in 2 lines like a {persona} game show host. "
        f"Then clearly say 'YES' or 'NO' at the end."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    headers = {
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_URL, headers=headers, json=payload)

        if response.status_code == 200:
            text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return text
        else:
            raise Exception(f"Gemini API Error: {response.status_code} - {response.text}")
        
def parse_verdict(ai_response: str) -> tuple[bool, str]:
    """Parse AI response to extract verdict and a cleaned explanation."""
    print(f"--- Inside parse_verdict ---")
    print(f"Raw input: {repr(ai_response)}")

    cleaned_response_initial = ai_response.strip()
    print(f"After initial strip: {repr(cleaned_response_initial)}")

    if cleaned_response_initial.startswith('"') and cleaned_response_initial.endswith('"'):
        ai_response_no_quotes = cleaned_response_initial[1:-1]
        print(f"After quote removal: {repr(ai_response_no_quotes)}")
    else:
        ai_response_no_quotes = cleaned_response_initial
        print("No quotes to remove.")
    
    lines = ai_response_no_quotes.splitlines()
    print(f"Lines from splitlines: {repr(lines)}")

    explanation = ""
    for line in lines:
        clean_line = line.strip()
        upper_line = clean_line.upper()
        print(f"Checking line: {repr(clean_line)}")
        if upper_line in {"YES", "YES."}:
            print("!!! Matched YES on a line. Returning True.")
            return True, explanation
        if upper_line in {"NO", "NO."}:
            print("!!! Matched NO on a line. Returning False.")
            return False, explanation
        # Save first meaningful non-empty line as explanation
        if explanation == "" and clean_line != "":
            explanation = clean_line

    print("Option 1 failed. Checking Option 2 (regex match)...")
    verdict_match = re.search(r'\b(YES|NO)[.!]?\s*$', ai_response_no_quotes.strip(), flags=re.IGNORECASE)
    if verdict_match:
        verdict = verdict_match.group(1).upper()
        print(f"Regex matched verdict: {verdict}")
        return verdict == "YES", explanation

    print(f"--- parse_verdict failed to find a clear verdict ---")
    raise ValueError(f"Could not find YES/NO in AI response: {ai_response}")
