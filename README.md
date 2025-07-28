# Medication Exclusion Checker

This app allows users to check if one or more drug names are part of an exclusion list for clinical trials. It supports generic and U.S. brand names and handles spelling corrections.

## How to Use on Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click **“Deploy an app”**
4. Choose this repository and `med_checker.py` as the entrypoint
5. Share the generated link with your team

## Example Inputs

- `rosuvastatin` ✅
- `Crestor` ✅ (brand name)
- `metformin` ✅
- `clarithromycin` ❌ (excluded)

## Excluded Medications

- rosuvastatin (Crestor)
- simvastatin (Zocor)
- clarithromycin (Biaxin)
- itraconazole (Sporanox)
- carbamazepine (Tegretol)
- sulfasalazine (Azulfidine)

