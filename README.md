# Super Mario - Vintage Edition

Retro-style Super Mario platformer built with Pygame.

Files:
- `mario.py` - Pygame game (already present)
- `app.py` - Streamlit front-end that launches `mario.py`
- `requirements.txt` - Python dependencies

Quick local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py  # run Streamlit locally, or run `python mario.py` to play directly
```

Git + GitHub

```powershell
cd "d:\business\super mario"
git init
git add .
git commit -m "Add Super Mario game + Streamlit wrapper"
# create repo on GitHub and add remote, then:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

Deploy on Streamlit Cloud

1. Push repository to GitHub.
2. Go to https://streamlit.io/cloud and sign in.
3. Create New App → select your GitHub repo → set main file to `app.py` → Deploy.

Notes

- Streamlit Cloud and other hosting providers may run in headless environments where opening a Pygame window is not possible. In that case, consider reworking the game to render to an image buffer and stream frames to Streamlit, or provide downloadable instructions for running locally.
