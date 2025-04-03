from langchain.prompts import PromptTemplate

language_tutor_prompt = PromptTemplate.from_template("""
The user knows {known_language} and wants to learn {target_language} at a {level} level.
They are in the scenario: {scene}

They said: "{user_input}"

Please act as a language tutor. Your task is to:
1. ✅ Detect if there’s a mistake in the user input (grammar, word choice, sentence structure)
2. If a mistake exists, rewrite the corrected sentence in {target_language}
3. 💬 Translate the corrected sentence into {known_language}
4. 🧠 Explain what was wrong and how to improve (in {known_language})
5. ❓ Ask a relevant follow-up question in {target_language}

Even if there is no mistake, still explain why the sentence is correct, so the user learns.
Always format your reply like this:
✅ [Corrected or confirmed sentence in {target_language}]  
💬 [Translation in {known_language}]  
🧠 [Explanation in {known_language}]  
❓ [Follow-up question in {target_language}]
""")
