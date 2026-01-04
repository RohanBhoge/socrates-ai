import google.generativeai as genai
import sys

print(f"Python executable: {sys.executable}")
print(f"google-generativeai version: {genai.__version__}")

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are a helper."
    )
    print("Successfully created GenerativeModel with system_instruction.")
except TypeError as e:
    print(f"Failed to create GenerativeModel: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
