import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def run():
    # title dan deskripsi pendek
    st.title('EDA Analysis Used Car Price')
    st.write('EDA ini terfokus pada eksplorasi untuk memahami data lebih dalam dengan melihat distribusi data, korelasi atau hubungan antar kolom dan eksplorasi berdasarkan business domain.')
    st.markdown('---')

    #load dataset dan tampilkan dataset
    dataset = pd.read_csv('dataset.csv')
    st.markdown("<h4 style='text-align: center; color: white;'>Dataset Preview</h4>", unsafe_allow_html=True)
    st.dataframe(dataset,hide_index=True, height=200, width=1000)

    # Tulis deskripsi kolom
    st.write("Deskripsi Kolom: ")
    st.write('`model` = Tipe atau model mobil (categorical - nominal)')
    st.write('`year` = Tahun pembuatan mobil (categorical - ordinal)')
    st.write('`price` = Harga (dalam Pound Sterling - numerical)') 
    st.write('`transmission` = Tipe transmisi mobil (categorical - nominal)')
    st.write('`mileage` = Jumlah jarak tempuh dalam miles (numerical)')
    st.write('`fuelType` = Jenis bahan bakar (cateogrical - nominal)')
    st.write('`tax` = Jumlah pajak dalam Pound Sterling')
    st.write('`mpg`= Miles per Gallon (1 gallon = 3.78541 liter - numerical) ')
    st.write('`engineSize` = Ukuran mesin (Numerical)')
    st.write('`company` = Brand atau nama perusahaan pembuat mobil (categorical - nominal)')
    st.markdown('---')

    # numeric data untuk chart 1
    numeric_data = dataset[['mileage','tax','engineSize','mpg']]

    # title chart 1
    st.markdown("<h3 style='text-align: center; color: white;'>Perkembangan Harga Pertahun</h3>", unsafe_allow_html=True)

    # group dataset berdasarkan tahun dan brand
    year = dataset[['year', 'price']].groupby('year').mean()
    audi = dataset[['year', 'price']][dataset['company'] == "Audi"].groupby('year').mean()
    toyota = dataset[['year', 'price']][dataset['company'] == "Toyota"].groupby('year').mean()
    hyundai = dataset[['year', 'price']][dataset['company'] == "Hyundai"].groupby('year').mean()
    bmw = dataset[['year', 'price']][dataset['company'] == "BMW"].groupby('year').mean()

    # melakukan index ulang supaya range x sama
    audi = audi.reindex(year.index, fill_value=0)
    toyota = toyota.reindex(year.index, fill_value=0)
    hyundai = hyundai.reindex(year.index, fill_value=0)
    bmw = bmw.reindex(year.index, fill_value=0)

    fig=plt.figure(figsize=(20, 7))

    # Plot rata-rata semua mobil pertahun dengan garis
    plt.plot(year.index, year['price'], label='All Cars', linestyle='-', color='cyan')

    # plot rata-rata per brand dengan warna garis yang berbeda
    plt.plot(audi.index, audi['price'], label='Audi', linestyle='--', color='red')
    plt.plot(toyota.index, toyota['price'], label='Toyota', linestyle='--', color='blue')
    plt.plot(hyundai.index, hyundai['price'], label='Hyundai', linestyle='--', color='yellow')
    plt.plot(bmw.index, bmw['price'], label='BMW', linestyle='--', color='black')

    # modifikasi xticks
    plt.xticks(year.index, labels=year.index, rotation=45)

    # legend dengan posisi kiri atas
    plt.legend(loc=2)

    # title dan label
    plt.title('Average Price by Year')
    plt.xlabel('Year')
    plt.ylabel('Average Price')
    plt.grid(True)

    # Munculkan plot dan keterangan
    st.pyplot(fig)
    st.write('Dari chart di atas, kita bisa melihat bahwa:\n- Setiap perusahaan memiliki rata-rata yang berbeda dari tahun ke tahun.\n- Rata-rata harga pada semua perusahaan mengalami kenaikan yang mirip sebagaimana bertambahnya tahun. Ini menandakan semakin muda sebuah mobil, maka harga nya semakin tinggi.')
    st.markdown('---')

    # title chart 2
    st.markdown("<h3 style='text-align: center; color: white;'>Average Price berdasarkan Brand</h3>", unsafe_allow_html=True)
    # figure
    fig=plt.figure(figsize=(7,5))
    #barplot
    ax=sns.barplot(dataset, x='company', y='price', estimator='mean')
    plt.bar_label(ax.containers[0], label_type='center', color='white') # bar label
    st.pyplot(fig) # tampilkan plot
    st.write('Terlihat bahwa company yang ada terbagi seperti terbagi menjadi 2 kelas. Kelas dengan rata-rata harga yang tinggi yaitu Audi dan BMW, lalu kelas dengan harga rata-rata yang rendah yaitu Toyota dan Hyundai.')
    st.markdown('---')

    # judul plot 3
    st.markdown("<h3 style='text-align: center; color: white;'>Average Price Model berdasarkan Brand</h3>", unsafe_allow_html=True)
    # mendapatkan list nama brand atau company
    company = dataset['company'].unique().tolist()

    # figure
    fig=plt.figure(figsize=(20,30))
    #looping subplot
    for i, comp in enumerate(company):
        plt.subplot(3,2,i+1) 
        data = dataset[['model','price']][dataset['company']==comp].groupby('model').mean().sort_values("price", ascending=False) # filter dataset
        ax=sns.barplot(data, x='price', y=data.index) # bar plot
        plt.bar_label(ax.containers[0]) #bar label
        plt.title(f"Rata-Rata Harga {comp}") #title per chart
    # tampilkan chart dan keterangan
    st.pyplot(fig)
    st.write('Kita bisa melihat bahwa setiap model dari setiap company memiliki harga rata-rata yang berbeda satu sama lain namun terdapat kemiripan antar model, hal ini akan digunakan sebagai tolak ukur pada proses pengurangan cardinality di feature engineering. ')
    st.markdown('---')
    
    # judl chart 4
    st.markdown("<h3 style='text-align: center; color: white;'>Average Price berdasarkan Tipe Transmisi</h3>", unsafe_allow_html=True)
    #figure
    fig=plt.figure(figsize=(12,8))
    ax=sns.barplot(dataset, x='transmission', y='price', estimator='mean') # label
    plt.bar_label(ax.containers[0], label_type='center', fontsize=14) # bar label
    # tampilkan chart dan keterangan
    st.pyplot(fig)
    st.write('Ketika melihat rata-rata harga setiap transmission, kita bisa lihat bahwa yang paling mahal justru adalah semi-auto, disusul automatic, lalu other, dan Manual. Ini bisa disebabkan oleh adanya outliers. Pada dunia nyata jika diurutkan dari yang termurah yaitu manual, semi-auto, automatic.')
    st.markdown('---')

    # judul chart 5
    st.markdown("<h3 style='text-align: center; color: white;'>Rata-Rata Efisiensi Bahan Bakar berdasarkan Brand</h3>", unsafe_allow_html=True)

    fig = plt.figure(figsize=(10, 8)) #figure
    ax=sns.barplot(dataset, x='company', y='mpg', estimator='mean') # bar plot
    plt.bar_label(ax.containers[0], label_type='center')

    # tampilkan chart dan keterangan
    st.pyplot(fig)
    st.write('Dari sini kita melihat bahwa Brand dengan efisiensi bahan bakar terbaik adalah Audi, disusul dengan Hyundai, BMW dan Toyota. Semakin kecil rata-rata efisiensi bahan bakar, semakin irit atau hemat konsumsi bahan bakar sebuah mobil.')
    st.markdown('---')


    # judul chart 6
    st.markdown("<h3 style='text-align: center; color: white;'>Efisiensi Berdasarkan Transmission</h3>", unsafe_allow_html=True)

    fig=plt.figure(figsize=(10,6))
    ax = sns.barplot(data=dataset, x='transmission', y='mpg', estimator='mean') # barplot
    plt.bar_label(ax.containers[0], label_type='center') # bar label
    # tampilkan chart dan keterangan
    st.pyplot(fig)
    st.write('Disini kita bisa melihat bahwa Semi-Auto memiliki efisiensi yang paling baik di antara tipe transmissi lain.')
    st.markdown('---')


    # Judul chart 7
    st.markdown("<h3 style='text-align: center; color: white;'>Data Distribution</h3>", unsafe_allow_html=True)
    # list nama kolom
    cols = dataset[['price', 'mileage', 'tax', 'mpg', 'engineSize']]
    # figur size
    fig=plt.figure(figsize=(30,13))

    # iterasi untuk membuat chart
    for i, col in enumerate(cols):
        plt.subplot(2,3, i+1) # subplot
        sns.histplot(dataset[col], kde=True, bins=30) #histogram plot
        plt.title(f' Distribusi {col} \nskewness: {dataset[col].skew():.4f}') # judul plot beserta skewness
        plt.xticks(rotation=20)
    st.pyplot(fig)
    st.write('Terlihat hanya kolom tax yang memiliki skewness mendekati normal.')
    st.markdown('---')
    
    #judul chart 8
    st.markdown("<h3 style='text-align: center; color: white;'>Korelasi antara numerik Variables</h3>", unsafe_allow_html=True)
    fig=plt.figure(figsize=(7,7))
    sns.heatmap(numeric_data.corr("spearman"), annot=True, cmap='Blues')
    st.pyplot(fig)
    st.write('- Nilai korelasi terkuat terhadap price ada pada variable year dan engine Size.\n- Sedangkan variable yang paling lemah ada pada kolom Tax')
    st.markdown('---')

    #Judul chart 9
    st.markdown("<h3 style='text-align: center; color: white;'>Linearitas antara price dengan variable lain</h3>", unsafe_allow_html=True)

    # list pair untuk scatter
    pair = ['mileage', 'year','engineSize', 'mpg']

    fig=plt.figure(figsize=(15,10)) # figure
    for i, col in enumerate(pair):
        plt.subplot(2,2,i+1)
        sns.scatterplot(dataset, y='price', x=col)
        plt.title(f'Korelasi antara price dan {col}')
    st.pyplot(fig)
    st.write("Dari chart di atas dapat dikatakan:\n- Semakin tinggi jarak tempuh (mileage) sebuah mobil, maka semakin murah harganya. Mobil dengan jarak tempuh yang sedikit, cenderung memiliki harga yang tinggi.\n- Semakin muda usia mobil, harga nya pun semakin mahal. \n- Untuk engineSize, tidak terlalu terlihat pola pada scatter. Namun, kita bisa sedikitnya melihat bahwa ada kecenderungan ketika engineSize semakin besar, maka harga cenderung lebih mahal.\n- Hubungan antara price dan mpg menunjukan bahwa semakin efisien konsumsi bahan bakar mobil, maka harga cenderung bisa lebih mahal")
    st.markdown('---')

if __name__ == '__main__':
    run()
