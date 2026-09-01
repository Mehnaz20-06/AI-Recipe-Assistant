# Recipe Assistant — Memory-Personalized Chatbot

Chatbot that remembers your health conditions/allergies/preferences across
sessions (via Mem0 + Qdrant) and tailors recipe suggestions accordingly


## Architecture
```
main.py            -> CLI loop
memory_manager.py   -> Mem0 wrapper (Mem0 uses Qdrant internally as vector store)
recipe_agent.py      -> GEMINI AI call, builds prompt from retrieved facts
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



