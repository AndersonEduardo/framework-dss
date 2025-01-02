
import streamlit as st

from awss3 import AwsS3 as s3
from bundles import *

bds = Bundles()
bds.load_backup_from_s3()

st.title("Bundles upload")
st.subheader("You can upload a Excel file to update the bundles.")


uploaded_file = st.file_uploader("Escolha um arquivo", type=["xlsx"])

print('PARTE A')

if uploaded_file is not None:

    print('PARTE B')

    try:

        print('PARTE C')



        bds._load_from_excel(
            excel_filepath = uploaded_file,
            offline = True if s3.check_s3_availability() is False else False
        )

        st.success("Success. Bundles updated.")

    except Exception as e:

        st.error(f"Erro ao extrair dados: {e}")

else:

    st.warning("Please, upload an Excel file.")
