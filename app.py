import requests
import json

API_KEY = "AIzaSyBEhLDLWzv-Hvtf2eYEa8yCbZRA4XzpgDg"
# Using the stable 2026 endpoint
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"

print("--- AI CODE COMMENTER LOADED ---")
print("Paste your confusing code below. (Type 'exit' to close)")

while True:
    user_code = input("\nPASTE CODE HERE: ")
    
    if user_code.lower() == 'exit':
        break

    # The 'System Prompt' tells the AI exactly how to behave
    prompt = (
        "You are an expert developer. I will give you a snippet of code. "
        "Please return the exact same code but add helpful, simple comments "
        "to every line explaining what it does for a beginner. "
        f"Here is the code: \n{user_code}"
    )

    data = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            commented_code = result['candidates'][0]['content']['parts'][0]['text']
            print("\n--- COMMENTED CODE ---")
            print(commented_code)
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {e}")