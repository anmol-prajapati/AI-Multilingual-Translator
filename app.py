"""
app.py - Streamlit user interface. Run with:  streamlit run app.py
All translation logic lives in translator.py.
"""
import streamlit as st

import translator

st.set_page_config(page_title="AI Text Translator", page_icon="🌐", layout="centered")


@st.cache_resource(show_spinner=False)
def get_model(source, target):
    """Load the model only once per language pair; Streamlit keeps it in memory."""
    return translator.load_model(source, target)


def clear_all():
    """Callback for the Clear button."""
    st.session_state["input_text"] = ""
    st.session_state["result"] = ""


# Session state keeps values between button clicks
st.session_state.setdefault("input_text", "")
st.session_state.setdefault("result", "")

st.title("🌐 AI-Based Multilingual Text Translation System")
st.write("Translate text between **English** and **Hindi** using pretrained MarianMT models. "
         "Runs locally on your CPU. No API key needed.")

names = list(translator.LANGUAGES)  # ["English", "Hindi"]
col1, col2 = st.columns(2)
source_name = col1.selectbox("Source language", names, index=0)
target_name = col2.selectbox("Target language", names, index=1)

st.text_area("Enter text", key="input_text", height=180,
             placeholder="Type or paste text here...")

btn1, btn2, _ = st.columns([1, 1, 4])
translate_clicked = btn1.button("Translate", type="primary")
btn2.button("Clear", on_click=clear_all)

if translate_clicked:
    source = translator.LANGUAGES[source_name]
    target = translator.LANGUAGES[target_name]
    try:
        clean_text = translator.validate_input(st.session_state["input_text"], source, target)
        with st.spinner("Translating... (the first run downloads the model, please wait)"):
            tokenizer, model = get_model(source, target)
            st.session_state["result"] = translator.translate(clean_text, tokenizer, model)
    except ValueError as err:  # invalid input
        st.session_state["result"] = ""
        st.warning(str(err))
    except OSError as err:  # model download / file problem
        st.session_state["result"] = ""
        st.error(f"Could not load the model. Check your internet connection and disk space. Details: {err}")
    except Exception as err:  # anything unexpected
        st.session_state["result"] = ""
        st.error(f"Translation failed: {err}")

if st.session_state["result"]:
    st.subheader("Translation")
    st.text_area("Translated text", value=st.session_state["result"], height=180, disabled=True)
    st.caption("Copy: use the copy icon at the top-right of the box below.")
    st.code(st.session_state["result"], language=None)
