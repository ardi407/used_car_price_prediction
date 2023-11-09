import streamlit as st
import pandas as pd
import joblib

# load pipelines dengan joblib
pipe = joblib.load('deployment/pipelines.pkl')

# load dataset
dataset = pd.read_csv('deployment/dataset.csv')
# buat fungsi untuk run
def run():
    # buat judul halaman
    st.write('## Predict Used Car Price')

    # dicitionary untuk mengunbah opsi pilihan model
    my_dict = {"Audi": dataset['model'][dataset['company']=='Audi'].unique().tolist(), 
                "Toyota": dataset['model'][dataset['company']=='Toyota'].unique().tolist(),
                "BMW": dataset['model'][dataset['company']=='BMW'].unique().tolist(),
                "Hyundai": dataset['model'][dataset['company']=='Hyundai'].unique().tolist()}
    
    # membuat layout column untuk company dan model
    col1, col2 = st.columns([1, 1])
    with col1:
        company = st.selectbox('Brand', options=my_dict.keys())

    # untuk model, options akan berubah berdasarkan brand yang dipilih
    with col2:
        model = st.selectbox('Pilih Model', options=my_dict[company])

    # membuat layout column untuk tahun, ukuran mesin dan tipe transmisi
    column1, column2, column3 = st.columns([2,2,2])
    with column1:
        year = st.selectbox('Tahun', options=[int(x) for x in range(2020, 1990, -1)]) # input tahun
    with column2:
        transimssion = st.selectbox('Tipe Transmisi', options=dataset['transmission'].unique().tolist()) # input tipe transmisi
    with column3:
        engineSize=st.selectbox('Ukuran Mesin', options=dataset['engineSize'].unique().tolist())

    # membuat layout column untuk mileage, fueltype dan mpg
    kol1, kol2, kol3 = st.columns([3,1,1])
    with kol1:
        mileage = st.slider('Jarak Tempuh',0,100000,1000)
    with kol2:
        fueltype = st.selectbox('Jenis Bahan Bakar', options=dataset['fuelType'].unique().tolist())
    with kol3:
         mpg = st.number_input('Efisiensi', min_value=0, value=50, step=1, max_value=600, help="Input Efisiensi Bahan Bakar dalam Miles Per Gallon untuk Petrol atau Miles per full Charge ")
    
    # untuk menyimpan hasil input ke dalam form
    with st.form('Form Car Details'):
        # containers
        company=company
        model=model
        tahun=year
        trans=transimssion
        efisiensi = mpg
        engine = engineSize

        # tombol predict
        submitted = st.form_submit_button('Predict')
    
    # dictionary hasil data input
    data = {
    'model': model,
    'year': (int(tahun)),
    'transmission': trans,
    'mileage':mileage,
    'fuelType':fueltype,
    'mpg':efisiensi,
    'engineSize': engine,
    'company':company, 
    }
    
    # data inference ke dataframe
    data_inf = pd.DataFrame([data]).reset_index(drop=True)

    # tampilkan hasil input dalam dataframe
    st.dataframe(data_inf)

    # if clause jika tombol sudah di tekan
    if submitted:
        prediction = pipe.predict(data_inf)
        formatted_prediction_gbp = '{:,.0f}'.format(int(prediction)) # format hasil untuk GBP
        formatted_prediction_idr = '{:,.0f}'.format(int(prediction) * 19230.08) #format hasil untuk Rupiah
        #tampilkan output
        st.write(f'#### Prediction: GBP {formatted_prediction_gbp} atau IDR {formatted_prediction_idr}')

# supaya halaman berjalan
if __name__ == '__main__':
    run()