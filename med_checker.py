import streamlit as st
import pandas as pd
import difflib

# Load exclusions
excluded_df = pd.read_csv("excluded_drug_list.csv")
EXCLUDED = set(excluded_df["excluded_drug"].str.lower())

if "entered_meds" not in st.session_state:
    st.session_state.entered_meds = []
if "corrections" not in st.session_state:
    st.session_state.corrections = {}

st.title("Medication Exclusion Checker")
st.write("Enter one or more drug names (comma-separated or one per line):")

input_text = st.text_area("Drug name(s):")

if st.button("Check Medications"):
    st.session_state.entered_meds = [m.strip().lower() for m in input_text.replace(",", "\n").splitlines() if m.strip()]
    st.session_state.corrections = {}

def check_med(med):
    corrected = st.session_state.corrections.get(med)
    if corrected:
        if corrected in EXCLUDED:
            st.error(f"{corrected.title()} is excluded.")
        else:
            st.success(f"{corrected.title()} is not excluded.")
    elif med in EXCLUDED:
        st.error(f"{med.title()} is excluded.")
    else:
        suggestion = difflib.get_close_matches(med, EXCLUDED, n=1, cutoff=0.85)
        if suggestion:
            fixed = suggestion[0]
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Check '{med}'", key=f"orig_{med}"):
                    st.session_state.corrections[med] = med
                    st.rerun()
            with col2:
                if st.button(f"🔁 Check '{fixed}' instead", key=f"suggest_{med}"):
                    st.session_state.corrections[med] = fixed
                    st.rerun()
        else:
            st.success(f"{med.title()} is not excluded.")

if st.session_state.entered_meds:
    st.subheader("Results")
    for med in st.session_state.entered_meds:
        check_med(med)
