import streamlit as st
import pandas as pd
import datetime     

st.title("CSV Column Standardization Tool")

@st.cache_data
def load_file(file):
    return pd.read_csv(file)

if "step" not in st.session_state:
    st.session_state.step = 1

if "df" not in st.session_state:
    st.session_state.df = None

if "mdf" not in st.session_state:
    st.session_state.mdf = None

if 'fdf' not in st.session_state:
    st.session_state.fdf = None

def next_step():
    st.session_state.step += 1

def back_step():
    st.session_state.step -= 1


if st.session_state.step == 1:
    st.subheader("Step 1 : Upload File")

    file = st.file_uploader("Upload your CSV file", type="csv")

    if file:
        df = load_file(file)
        st.session_state.df = df

        st.success("File uploaded successfully")
        st.dataframe(df.head(5))

        st.button("Next", on_click=next_step)


elif st.session_state.step == 2:
    st.header("Step 2: Column Mapping")

    df = st.session_state.df

    user = st.selectbox("Select column for User ID", df.columns)
    date = st.selectbox("Select column for Transaction", df.columns)
    amount = st.selectbox("Select column for Amount", df.columns)

    if st.button("Apply Mapping"):
        mdf = pd.DataFrame()

        mdf["User_ID"] = df[user]
        mdf["Transaction_Date"] = df[date]
        mdf["Amount"] = df[amount]

        st.session_state.mdf = mdf

        st.success("Mapping done")
        st.dataframe(mdf.head(10))

    col1, col2 = st.columns(2)

    with col1:
        st.button("Back", on_click=back_step)

    with col2:
        st.button("Next", on_click=next_step)

elif st.session_state.step == 3:
    st.header("Step 3: Validation and Transformation")

    df = st.session_state.mdf.copy()

    df["Amount"] = pd.to_numeric(df["Amount"])
    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"])

    if df["Transaction_Date"].isnull().sum() > 0:
        st.error("Date column has invalid dates")
    else:
        st.success("Date column is valid")

    if st.checkbox("Remove duplicate rows"):
        key = st.selectbox("Select column to remove duplicates", df.columns)
        df = df.drop_duplicates(subset=key)
        st.success("Duplicates removed")

    null_choice = st.selectbox(
        "Null Handling",
        ["Do nothing", "Fill with value", "Fill numeric columns with mean"]
    )

    if null_choice == "Fill with value":
        value = st.text_input("Enter value", "Unknown")
        df = df.fillna(value)
        st.success("Null values filled")

    elif null_choice == "Fill numeric columns with mean":
        num_cols = df.select_dtypes(include="number").columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
        st.success("Numeric null values filled with mean")

    if st.checkbox("Create Adjusted Amount"):
        tax = st.number_input("Enter Tax Multiplier", value=1.18)
        df["Adjusted_Amount"] = df["Amount"] * tax
        st.success("Adjusted Amount created")

    st.session_state.fdf = df

    st.dataframe(df.head(10))

    col1, col2 = st.columns(2)

    with col1:
        st.button("Back", on_click=back_step)

    with col2:
        st.button("Next", on_click=next_step)   

elif st.session_state.step == 4:
    st.header("Step 4: Export File")

    df = st.session_state.fdf

    st.dataframe(df.head(10))

    csv = df.to_csv()

    st.download_button("Download CSV", csv)

    st.button("Back", on_click=back_step)