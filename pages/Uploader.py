import requests
import streamlit as st

from awss3 import AwsS3 as s3
from bundles import *

bds = Bundles()
bds.load_backup_from_s3()

st.title("Bundles upload")
st.subheader("You can upload a Excel file to update the bundles.")


uploaded_file = st.file_uploader("Escolha um arquivo", type=["xlsx"])


if uploaded_file is not None:

    try:

        file = {'file': uploaded_file.getvalue()}

        response = requests.post(
            API_DSSF_UPLOAD_BUNDLE,
            files=file,
        )

        print('API - Bundle upload status code:', response.status_code)

        st.success("Success. Bundles updated.")

    except Exception as e:

        st.error(f"Erro ao extrair dados: {e}")

else:

    st.warning("Please, upload an Excel file.")
