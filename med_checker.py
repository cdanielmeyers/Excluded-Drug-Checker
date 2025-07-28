import streamlit as st
import pandas as pd
import difflib

# Load excluded list
excluded_df = pd.read_csv("excluded_drug_list.csv")
EXCLUDED = set(excluded_df["excluded_drug"].str.lower().tolist())

# Set up session state
if "entered_meds" not in st.session_state:
    st.session_state.entered_meds = []
if "corrections" not in st.session_state:
    st.session_state.corrections = {}

st.title("Exclusion Checker")
st.write("Enter one or more drug names (comma-separated or one per line):")

input_text = st.text_area("Drug name(s):")

if st.button("Check Medications"):
    st.session_state.entered_meds = [m.strip().lower() for m in input_text.replace(",", "\n").splitlines() if m.strip()]
    st.session_state.corrections = {}

def check_med(med):
    corrected = st.session_state.corrections.get(med, med)
    if corrected in EXCLUDED:
        st.error(f"{corrected.title()} is excluded.")
    elif corrected != med:
        st.success(f"{corrected.title()} is not excluded.")
    else:
        suggestion = difflib.get_close_matches(med, EXCLUDED, n=1, cutoff=0.8)
        if suggestion:
            fixed = suggestion[0]
            if st.button(f"🔁 Check '{fixed}' instead", key=med):
                st.session_state.corrections[med] = fixed
                st.rerun()
        else:
            st.success(f"{med.title()} is not excluded.")

if st.session_state.entered_meds:
    st.subheader("Results")
    for med in st.session_state.entered_meds:
        check_med(med)
