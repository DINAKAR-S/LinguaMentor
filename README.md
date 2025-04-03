# LinguaMentor

LinguaMentor is an interactive language-learning chatbot that helps users learn new languages through practical scenarios. It utilizes AI-powered feedback and mistake correction to provide personalized language practice, focusing on real-world conversations. The chatbot tracks user progress, logs mistakes, and offers valuable insights to enhance learning.

---

## **Features**:

- **Scenario-based learning**: Choose from various real-life scenarios such as cafés, restaurants, shopping, and more.
- **Grammar & Vocabulary correction**: Detects and corrects mistakes with detailed explanations.
- **Personalized feedback**: Logs mistakes in a database and offers suggestions on areas to focus on.
- **Auto-conclusion after every 4 chat turns**: Option to conclude the session and receive a review of your progress.
- **Supports multiple languages**: Learn different languages with real-time feedback.

---

## **Tech Stack**:

- **Backend**: FastAPI for API creation
- **Frontend**: Streamlit for interactive UI
- **AI Model**: OpenRouter AI or DeepSeek for language understanding
- **Database**: SQLite for mistake tracking
- **Language Model**: DeepSeek (or OpenAI's GPT models)
- **Other**: Requests library for API communication

---

## **Installation Instructions**:

### Clone the repository:
```bash
git clone https://github.com/your-username/linguamentor.git
cd linguamentor
```

### Backend Setup:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the backend**:
   ```bash
   uvicorn app:app --reload
   ```

### Frontend Setup:

1. **Install Streamlit** (if not already installed):
   ```bash
   pip install streamlit
   ```

2. **Run the frontend**:
   ```bash
   streamlit run ui.py
   ```

---

## **Usage**:

1. **Open the web interface**: 
   After running the `streamlit` command, open your browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

2. **Set your learning preferences**:
   - Select your **native language**, **target language**, **current level**, and **scenario** (e.g., Café, Restaurant, etc.).

3. **Start chatting with the AI**:
   - The chatbot will guide you through the scenario in the target language.
   - It will give you feedback on your input, correct your mistakes, and provide explanations for grammar and vocabulary.
   
4. **Automatic feedback**:
   - After every 4 turns, the bot will ask: _"Shall we conclude this session?"_
   - If you answer "yes", the chatbot will show a review of your progress, including categorized mistakes and suggestions for improvement.
   - If you answer "no", the chat continues.

---

## **Contributing**:

We welcome contributions! If you find any bugs or have feature requests, feel free to submit an issue or a pull request.

### Steps for contributing:

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature-name
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add new feature'
   ```
4. **Push to your branch**:
   ```bash
   git push origin feature-name
   ```
5. **Submit a pull request**.

---

## **License**:

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**:

For questions or inquiries, feel free to reach out to me via GitHub or email at [your-email@example.com].

---

```

---

### Explanation of Sections:

- **Project Overview**: Brief description of the chatbot and its functionalities.
- **Tech Stack**: Lists technologies used in the project.
- **Installation Instructions**: Guides to clone, install, and run the project.
- **Usage**: How to interact with the chatbot and its features.
- **Contributing**: Instructions for contributing to the project.
- **License**: Information about the project's licensing.
- **Contact**: Optional, for users to get in touch.

---
