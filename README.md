**NayePankh AI Assistant**

A small Flask-based chat frontend that uses Google Generative AI (Gemini) to power a support chatbot for the NayePankh Foundation.

**Files of interest**
- **App:** [app.py](app.py)
- **Frontend:** [templates/index.html](templates/index.html)
- **Static JS:** [static/script.js](static/script.js)
- **Styles:** [static/style.css](static/style.css)

**Requirements**
- Python 3.10+ recommended
- A Google Generative AI API key with access to the desired Gemini model

**Setup**
- Create and activate a virtual environment (Windows example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Install dependencies:

```bash
pip install flask python-dotenv google-genai
```

(If `google-genai` is not the correct package for your environment, install the official client recommended by Google or use your package manager.)

**Environment variables**
- Create a `.env` file in the project root with your API key:

```
GOOGLE_API_KEY=your_actual_api_key_here
```


**Run locally**

```bash
python app.py
```

Open http://localhost:5000 in your browser.

**How the pieces work**
- The browser sends POST requests to `/api/chat` (see [static/script.js](static/script.js)).
- `app.py` constructs `types.Content` items from session history and calls `client.models.generate_content`.
- The `GOOGLE_API_KEY` is passed into the `genai.Client(api_key=...)` constructor.

**Troubleshooting**
- "I ran into an unexpected processing issue": open your browser console (DevTools) to see the server error returned by the Flask endpoint.
- If the server returns an error about models (e.g., model not found), update the model name in `app.py` to one you have access to (examples: `models/gemini-1.5-flash`, `models/gemini-1.5-pro`, `models/gemini-2.0-flash`).
- If you see `ValueError: GOOGLE_API_KEY environment variable is not set`, confirm the `.env` file exists and restart the server.
- Use logs printed by `app.py` (it prints the raw response when received) to inspect API responses.


