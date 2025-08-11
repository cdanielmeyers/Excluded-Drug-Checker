import streamlit as st
import pandas as pd
import difflib

# -------------------------------------------------------
# Page config (must be first Streamlit call)
# -------------------------------------------------------
st.set_page_config(
    page_title="Medication Exclusion Checker: Study MTR-601-101",
    layout="wide"
)

# -------------------------------------------------------
# Load data
# -------------------------------------------------------
excluded_df = pd.read_csv("excluded_drug_list.csv")
EXCLUDED = set(excluded_df["excluded_drug"].str.lower().tolist())

# Known generic <-> brand pairs (for nicer display only)
GENERIC_TO_BRAND = {
    "aprepitant": "Emend", "apalutamide": "Erleada", "carbamazepine": "Tegretol", "enzalutamide": "Xtandi",
    "ivacaftor": "Kalydeco", "ivosidenib": "Tibsovo", "lumacaftor": "Orkambi", "mitotane": "Lysodren",
    "phenytoin": "Dilantin", "rifampin": "Rifadin", "alfentanil": "Alfenta", "avanafil": "Stendra",
    "budesonide": "Entocort", "buspirone": "Buspar", "conivaptan": "Vaprisol", "cyclosporine": "Neoral",
    "darifenacin": "Enablex", "darunavir": "Prezista", "dasabuvir": "Viekira Pak", "diltiazem": "Cardizem",
    "dronedarone": "Multaq", "elvitegravir": "Vitekta", "eletriptan": "Relpax", "eplerenone": "Inspra",
    "ergotamine": "Cafergot", "erythromycin": "Ery-Tab", "everolimus": "Afinitor", "felodipine": "Plendil",
    "fentanyl": "Duragesic", "fluconazole": "Diflucan", "ibrutinib": "Imbruvica", "idelalisib": "Zydelig",
    "imatinib": "Gleevec", "indinavir": "Crixivan", "isavuconazole": "Cresemba", "ivabradine": "Corlanor",
    "ketoconazole": "Nizoral", "lemborexant": "Dayvigo", "lomitapide": "Juxtapid", "lopinavir": "Kaletra",
    "lovastatin": "Mevacor", "lurasidone": "Latuda", "maraviroc": "Selzentry", "midazolam": "Versed",
    "naloxegol": "Movantik", "nefazodone": "Serzone", "nelfinavir": "Viracept", "nisoldipine": "Sular",
    "ombitasvir": "Viekira Pak", "paritaprevir": "Viekira Pak", "pimozide": "Orap", "posaconazole": "Noxafil",
    "quetiapine": "Seroquel", "quinidine": "Quinidex", "ritonavir": "Norvir", "rosuvastatin": "Crestor",
    "saquinavir": "Invirase", "sildenafil": "Viagra", "simvastatin": "Zocor", "sirolimus": "Rapamune",
    "sulfasalazine": "Azulfidine", "tacrolimus": "Prograf", "telithromycin": "Ketek", "ticagrelor": "Brilinta",
    "tipranavir": "Aptivus", "tolvaptan": "Samsca", "triazolam": "Halcion", "vardenafil": "Levitra",
    "venetoclax": "Venclexta", "verapamil": "Calan", "voriconazole": "Vfend", "clarithromycin": "Biaxin",
    "ciprofloxacin": "Cipro", "ceritinib": "Zykadia", "cobicistat": "Tybost", "crizotinib": "Xalkori",
    "dasatinib": "Sprycel", "itraconazole": "Sporanox"
}
BRAND_TO_GENERIC = {v.lower(): g for g, v in GENERIC_TO_BRAND.items()}

def pretty_name(name: str) -> str:
    """Show 'Brand (Generic)' when known; otherwise Title Case."""
    n = name.strip()
    lower = n.lower()
    if lower in GENERIC_TO_BRAND:
        return f"{GENERIC_TO_BRAND[lower]} ({n.title()})"
    if lower in BRAND_TO_GENERIC:
        gen = BRAND_TO_GENERIC[lower]
        return f"{n.title()} ({gen.title()})"
    return n.title()

# -------------------------------------------------------
# Sidebar disclaimer
# -------------------------------------------------------
with st.sidebar:
    st.markdown("### Study MTR-601-101")
    st.markdown(
        ":warning: **Disclaimer**\n\n"
        "This is not a validated tool, but rather an optional/support tool to assist study staff in evaluation of excluded medications. "
        "Please refer to the study protocol for full details on excluded medications. "
        "Please reach out to your CRA with any questions."
    )

# -------------------------------------------------------
# Main UI
# -------------------------------------------------------
st.title("Medication Exclusion Checker: Study MTR-601-101")
st.caption("Enter one or more drug names (comma-separated or one per line).")

if "entered_meds" not in st.session_state:
    st.session_state.entered_meds = []
if "corrections" not in st.session_state:
    st.session_state.corrections = {}
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

st.text_area("Drug name(s):", key="input_text")

colA, colB = st.columns([1, 1])
with colA:
    check_clicked = st.button("Check Medications", type="primary")
with colB:
    if st.button("Clear"):
        st.session_state.entered_meds = []
        st.session_state.corrections = {}
        st.session_state.input_text = ""
        st.rerun()

if check_clicked:
    st.session_state.corrections = {}
    st.session_state.entered_meds = [
        m.strip().lower()
        for m in st.session_state.input_text.replace(",", "\n").splitlines()
        if m.strip()
    ]

def check_one(med: str, excluded_items: list, allowed_items: list, suggestion_rows: list, idx: int):
    chosen = st.session_state.corrections.get(med, med)

    # If user already chose a path (original or suggestion)
    if chosen in EXCLUDED:
        excluded_items.append(pretty_name(chosen))
        return
    if chosen != med:
        # User selected a non-excluded alternative explicitly
        allowed_items.append(pretty_name(chosen))
        return

    # No prior choice: evaluate original input
    if med in EXCLUDED:
        excluded_items.append(pretty_name(med))
        return

    # Offer suggestion if very close to an excluded term; don't auto-allow
    close = difflib.get_close_matches(med, EXCLUDED, n=1, cutoff=0.85)
    if close:
        fixed = close[0]
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"✅ Check '{med}'", key=f"orig_{idx}_{med}"):
                st.session_state.corrections[med] = med
                st.rerun()
        with c2:
            if st.button(f"🔁 Check '{fixed}' instead", key=f"suggest_{idx}_{med}"):
                st.session_state.corrections[med] = fixed
                st.rerun()
    else:
        allowed_items.append(pretty_name(med))

# Show grouped results
if st.session_state.entered_meds:
    excluded_items, allowed_items, suggestion_rows = [], [], []
    for i, med in enumerate(st.session_state.entered_meds):
        check_one(med, excluded_items, allowed_items, suggestion_rows, i)

    st.markdown("---")
    left, right = st.columns(2)

    with left:
        st.subheader("❌ Excluded")
        if excluded_items:
            st.error("\n".join(f"- {item}" for item in sorted(set(excluded_items))))
        else:
            st.info("No excluded medications found in your list.")

    with right:
        st.subheader("✅ Not Excluded")
        if allowed_items:
            st.success("\n".join(f"- {item}" for item in sorted(set(allowed_items))))
        else:
            st.info("No allowed medications to display yet.")
