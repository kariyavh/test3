import streamlit as st
from pathlib import Path
import tempfile
import pandas as pd
from app.data_tools import merge_and_clean
from app.pdf_tools import merge_pdfs

st.set_page_config(page_title="Office Efficiency Toolkit", page_icon="🗂️", layout="centered")
st.title("Office Efficiency Toolkit")
st.caption("Merge & clean Excel/CSV, merge PDFs, and batch-rename files — fast.")

tab1, tab2, tab3 = st.tabs(["📊 Merge Excel/CSV", "📄 Merge PDFs", "📝 Batch Rename"])

with tab1:
    st.subheader("Merge Excel/CSV")
    uploads = st.file_uploader("Upload multiple .xlsx/.xls/.csv files", accept_multiple_files=True, type=["xlsx","xls","csv"])
    drop_dups = st.checkbox("Drop duplicate rows", value=True)
    if uploads:
        tmp_paths = []
        for f in uploads:
            tmp = Path(tempfile.gettempdir()) / f.name
            with open(tmp, "wb") as out:
                out.write(f.getbuffer())
            tmp_paths.append(tmp)
        df = merge_and_clean(tmp_paths, drop_duplicates=drop_dups)
        st.success(f"Merged rows: {len(df)}")
        st.dataframe(df.head(50))
        out_fmt = st.selectbox("Export format", ["xlsx", "csv"])
        if st.button("Download merged file"):
            if out_fmt == "xlsx":
                from io import BytesIO
                bio = BytesIO()
                df.to_excel(bio, index=False)
                st.download_button("Download .xlsx", data=bio.getvalue(), file_name="merged_clean.xlsx")
            else:
                st.download_button("Download .csv", data=df.to_csv(index=False).encode("utf-8"), file_name="merged_clean.csv")

with tab2:
    st.subheader("Merge PDFs")
    pdfs = st.file_uploader("Upload PDFs to merge (order matters)", type=["pdf"], accept_multiple_files=True)
    if pdfs and st.button("Merge PDFs"):
        tmp_paths = []
        for i, f in enumerate(pdfs):
            tmp = Path(tempfile.gettempdir()) / f"pdf_{i}_{f.name}"
            with open(tmp, "wb") as out:
                out.write(f.getbuffer())
            tmp_paths.append(tmp)
        out_file = Path(tempfile.gettempdir()) / "merged.pdf"
        merge_pdfs(tmp_paths, out_file)
        with open(out_file, "rb") as fh:
            st.download_button("Download merged.pdf", data=fh.read(), file_name="merged.pdf", mime="application/pdf")

with tab3:
    st.subheader("Batch Rename Files")
    files = st.file_uploader("Upload files to rename (we simulate rename and let you download renamed copies)", accept_multiple_files=True)
    prefix = st.text_input("Prefix", value="")
    suffix = st.text_input("Suffix", value="")
    replace_from = st.text_input("Replace text (optional)", value="")
    replace_to = st.text_input("Replace with (optional)", value="")
    start_number = st.number_input("Start number", min_value=1, value=1)
    pad = st.number_input("Zero pad length", min_value=1, value=3)

    if files and st.button("Generate renamed files"):
        import zipfile, io
        mem_zip = io.BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            seq = int(start_number)
            for f in files:
                stem = Path(f.name).stem
                if replace_from:
                    stem = stem.replace(replace_from, replace_to)
                new_name = f"{prefix}{stem}{suffix}_{str(seq).zfill(int(pad))}{Path(f.name).suffix}"
                zf.writestr(new_name, f.getbuffer())
                seq += 1
        st.download_button("Download renamed files (.zip)", data=mem_zip.getvalue(), file_name="renamed_files.zip", mime="application/zip")
