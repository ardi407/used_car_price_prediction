import streamlit as st
import eda
import predictions

halaman = st.sidebar.selectbox('Halaman: ',('Prediction', 'EDA'))
if halaman == 'Prediction':
    predictions.run()
else:
    eda.run()