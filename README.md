# Recipe Assistant — Memory-Personalized Chatbot

Chatbot that remembers your health conditions/allergies/preferences across
sessions (via Mem0 + Qdrant) and tailors recipe suggestions accordingly
(via OpenAI).

## Architecture
```
main.py            -> CLI loop
memory_manager.py   -> Mem0 wrapper (Mem0 uses Qdrant internally as vector store)
recipe_agent.py      -> OpenAI call, builds prompt from retrieved facts
```

## Setup (do this in order)

### 1. Install Docker Desktop (if you don't have it)
Download from https://www.docker.com/products/docker-desktop/ — needed to run
Qdrant locally. Confirm it's running before step 2.

### 2. Start Qdrant locally
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```
Leave this running in its own terminal. Verify it's up at http://localhost:6333/dashboard

### 3. Clone/open this project in VS Code
Open the `recipe-assistant` folder in VS Code.

### 4. Create a virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

### 6. Set your API key
```bash
cp .env.example .env
```
Get a free Gemini API key at https://aistudio.google.com/apikey (no card
required). Open `.env` and paste it in place of `your-gemini-key-here`
(the variable is `GOOGLE_API_KEY` — that's what both Mem0 and the Gemini
SDK look for, not `GEMINI_API_KEY`).

### 7. Run it
```bash
python main.py
```

## Try this flow to prove the memory works
```
You: I have high cholesterol
Assistant: [generic acknowledgment/recipe]
You: I'm craving something spicy, give me a recipe
Assistant: [recipe that avoids high-cholesterol ingredients, explains substitutions]
You: /profile
[shows "high cholesterol" was extracted and stored]
```

Close the app, restart `python main.py`, ask for a spicy recipe again —
it'll still remember your cholesterol without you repeating yourself. That
persistence across sessions is the whole point of the project.

## Known limitations (be upfront about these in interviews, don't hide them)
- Single hardcoded user (`USER_ID` in main.py) — swap for real auth in a
  production version.
- No web search yet — recipes come from the LLM's own knowledge. Easy to
  add: a `web_search.py` module that fetches candidate recipes, then feeds
  them into `recipe_agent.py`'s prompt instead of "cook from scratch."
- No conversation memory (short-term chat history) — only long-term facts.
  Each turn is stateless except for what Mem0 retrieves.

## Extending for your resume (do at least one of these)
1. **Web search integration** — use Tavily or Serper API to fetch real
   recipes, then have the LLM adapt them instead of generating from scratch.
2. **Streamlit UI** — swap the CLI for a simple web interface (1-2 hours of
   work, makes a much better demo video/screenshot for your resume).
3. **Multi-user support** — real user_id from a login system instead of the
   hardcoded string.
