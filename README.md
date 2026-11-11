# AI-Based Multilingual Text Translation System Using Python

English <-> Hindi text translation with pretrained **MarianMT** models (Hugging Face Transformers + PyTorch) and a **Streamlit** interface. Runs on CPU. No paid API or API key.

| Direction | Model |
|---|---|
| English -> Hindi | `Helsinki-NLP/opus-mt-en-hi` |
| Hindi -> English | `Helsinki-NLP/opus-mt-hi-en` |

Only these two directions are supported. Each model handles one direction.

## Project structure
```
translation_project/
  app.py            Streamlit UI (buttons, dropdowns, caching)
  translator.py     Validation, model loading, translation (no UI code)
  requirements.txt  Dependencies
  tests/test_logic.py  Tests for validation logic (no model needed)
  README.md  .gitignore
```

## Setup and run (VS Code)
1. Install Python 3.9+ from python.org (tick "Add Python to PATH" on Windows). Check: `python --version`.
2. Open VS Code -> **File > Open Folder...** -> choose `translation_project`.
3. Open the terminal: **Terminal > New Terminal**.
4. Create a virtual environment:
   - Windows: `python -m venv venv`
   - macOS/Linux: `python3 -m venv venv`
5. Activate it:
   - Windows (PowerShell): `venv\Scripts\Activate.ps1`  (CMD: `venv\Scripts\activate.bat`)
   - macOS/Linux: `source venv/bin/activate`
   - In VS Code, choose the interpreter: Ctrl+Shift+P -> "Python: Select Interpreter" -> the `venv` one.
6. Install requirements: `python -m pip install --upgrade pip` then `pip install -r requirements.txt`
7. Run: `streamlit run app.py` (browser opens at http://localhost:8501).

**Internet is needed on the first translation of each direction** to download the model (a few hundred MB). After that the files are cached on your laptop.

## Optional: run the logic tests
`python -m unittest discover tests -v`

## Troubleshooting
- **`streamlit` is not recognized**: the virtual environment is not active, or run `python -m streamlit run app.py`.
- **PowerShell "running scripts is disabled"**: run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or use CMD.
- **`ModuleNotFoundError`**: activate the venv and run `pip install -r requirements.txt` again.
- **SentencePiece / tokenizer error**: `pip install sentencepiece sacremoses`. On very new Python versions, try Python 3.10-3.12.
- **Torch install fails or is huge**: use Python 3.10-3.12 (64-bit); the CPU build is enough.
- **"Could not load the model" / connection error**: check internet and free disk space; retry.
- **First translation is slow**: the model is downloading/loading; later ones are faster.
- **Port in use**: `streamlit run app.py --server.port 8502`.
- **Warning "text looks like Hindi/English"**: the selected source language does not match the text script.

## Limitations
Only en<->hi; translations can be fluent but wrong; idioms and ambiguous words may fail; very long text is limited to 2000 characters; sentences are translated one by one (no cross-sentence context).

## Testing note
The unit tests check validation logic only. Translation quality has to be checked by running the app; any example outputs you put in a report should be copied from your real runs.
