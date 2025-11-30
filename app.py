import streamlit as st
import subprocess
import sys
import os

st.set_page_config(page_title="Super Mario Game", layout="centered")
st.title("🍄 Super Mario - Vintage Edition")

st.write("Retro-style Super Mario platformer built with Pygame")


def running_headless() -> bool:
    """Return True when running in a headless environment (no DISPLAY on Unix).

    On Windows this usually isn't headless, but on Linux servers (Streamlit Cloud)
    there is no display and Pygame windows cannot open.
    """
    if sys.platform == "win32":
        return False
    return os.environ.get("DISPLAY") is None


repo_zip = "https://github.com/KyawZawHlyan/SuperMario/archive/refs/heads/main.zip"
mario_path = os.path.join(os.path.dirname(__file__), "mario.py")

if running_headless():
    st.warning("This hosting environment is headless — a Pygame window cannot open here.")
    st.markdown(f"- Download the game to run locally: [{repo_zip}]({repo_zip})")
    st.markdown("- After downloading, run locally: `python -m venv .venv` then activate and `pip install -r requirements.txt`")
    st.markdown(f"- Run locally with: `python \"{mario_path}\"`")
else:
    if st.button("Play Game"):
        st.info("Starting game... close the game window to return to Streamlit")
        try:
            subprocess.run([sys.executable, mario_path])
        except Exception as e:
            st.error(f"Failed to start game: {e}")


st.markdown("""
**Controls:**

- LEFT / RIGHT arrows — move
- SPACE — jump

**Notes:**

- This app launches the local `mario.py` Pygame script when a display is available.
- Streamlit Cloud (and many hosting providers) run headless — use the download link to run locally.
""")
