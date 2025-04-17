import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# App Title & Description
st.title("Haris' Data Assistant 🧠")
st.write("""
Upload a dataset, clean it smartly, and explore visual insights.
Choose what to keep, fix missing data, and export your cleaned work easily.
""")

# File Upload
st.header("📁 Upload Your Dataset")
file = st.file_uploader("Select a CSV file to get started", type="csv")

if file is not None:
    base_name = file.name.split('.')[0]
    data = pd.read_csv(file)

    # Preview Section
    st.subheader("🔎 Quick Peek at Your Data")
    st.write(data.head())

    # Data Cleaning Section
    st.header("🧼 Clean Up Options")
    clean_copy = data.copy()

    missing_strategy = st.selectbox("Missing values strategy:", 
                                    ["Drop rows", "Replace with 0", "Fill with column mean"])

    if missing_strategy == "Drop rows":
        clean_copy = clean_copy.dropna()
    elif missing_strategy == "Replace with 0":
        clean_copy = clean_copy.fillna(0)
    elif missing_strategy == "Fill with column mean":
        num_cols = clean_copy.select_dtypes(include=[np.number]).columns
        clean_copy[num_cols] = clean_copy[num_cols].fillna(clean_copy[num_cols].mean())

    if st.checkbox("🚫 Remove duplicates"):
        clean_copy = clean_copy.drop_duplicates()

    # Column Selector
    st.header("🎯 Pick Columns to Keep")
    col_options = data.columns.tolist()
    chosen_cols = st.multiselect("Choose your desired columns", col_options, default=col_options)
    clean_copy = clean_copy[chosen_cols]

    # Cleaned Data Display
    st.subheader("🧾 Final Cleaned Dataset")
    st.write(clean_copy)

    # Visualization Section
    st.header("📈 Visual Analysis")
    numeric_cols = clean_copy.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        x_axis = st.selectbox("X-axis column", numeric_cols)
        y_axis = st.selectbox("Y-axis column", numeric_cols)

        if x_axis != y_axis:
            st.subheader(f"🔹 Scatter Plot: {x_axis} vs {y_axis}")
            fig, ax = plt.subplots()
            ax.scatter(clean_copy[x_axis], clean_copy[y_axis], alpha=0.7)
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            st.pyplot(fig)
        else:
            st.error("X and Y axis cannot be the same.")

        st.subheader(f"📊 Histogram of {x_axis}")
        fig, ax = plt.subplots()
        ax.hist(clean_copy[x_axis], bins=20, color="teal", edgecolor="white")
        ax.set_xlabel(x_axis)
        ax.set_ylabel("Count")
        st.pyplot(fig)

        st.subheader(f"📦 Boxplot for {x_axis}")
        fig, ax = plt.subplots()
        sns.boxplot(data=clean_copy[x_axis], ax=ax, color="lightblue")
        st.pyplot(fig)
    else:
        st.warning("No numeric data available for plotting.")

    # Export Options
    st.header("📤 Export Cleaned Data")
    export_type = st.radio("Choose a format to download:", ["CSV", "Excel"])

    if export_type == "CSV":
        to_csv = clean_copy.to_csv(index=False)
        st.download_button("⬇️ Download CSV", to_csv, f"{base_name}_cleaned.csv", "text/csv")
    else:
        excel_io = io.BytesIO()
        with pd.ExcelWriter(excel_io, engine="openpyxl") as writer:
            clean_copy.to_excel(writer, index=False)
        st.download_button("⬇️ Download Excel", excel_io.getvalue(), f"{base_name}_cleaned.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("""
    ✨ Great job cleaning and exploring your data!
    Keep learning, keep improving — your journey into data science has just begun.
    """)
    
# Footer
st.write("🧑‍💻 Crafted with care by: **Muhammad Haris Awan** 🚀")
