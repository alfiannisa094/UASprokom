# Nama  : Alfiannisa Nur Afifah
# NIM   : 12220123
# UAS Pemrograman Komputer 
# 17 Desember 2021

import pandas as pd
import numpy as np
import json as js
import streamlit as st

st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Crude Oil Production throughout History")

fhand = open('kode_negara_lengkap.json')
data_country = js.load(fhand)                           
data_production = pd.read_csv('produksi_minyak_mentah.csv')
jsonasdf = pd.read_json('kode_negara_lengkap.json')

# Menghilangkan data produksi kode negara yang tidak terdapat di file json

country_codes = list()
country_codes = list()
removed_data = list()

for code in data_country:                                   # Membuat list kode negara dari file json                   
    country_codes.append(code["alpha-3"])

for index in data_production.index :                        # Membuat list kode kumpulan/organisasi negara 
    if data_production["kode_negara"][index] in country_codes :
        continue
    else:
        removed_data.append(data_production["kode_negara"][index])

removed_data = list(dict.fromkeys(removed_data))            # Menghilangkan kode negara yg double 

df_countryindex= data_production.set_index("kode_negara")   # Mengubah index menjadi kode negara 
df_cleaned = df_countryindex.drop(removed_data)             # Menghilangkan baris yang mengandung kode kumpulan/organisasi negara
df_cleaned = df_cleaned.reset_index()

# Menghilangkan kode negara yang tidak terdapat di data produksi

codes_cleaned = list()

for index in data_production.index :
    if data_production["kode_negara"][index] in codes_cleaned :
        continue
    else :
        codes_cleaned.append(data_production["kode_negara"][index])

def minus(l1,l2):
    return list(set(l1) - set(l2)) + list(set(l2) - set(l1))

country_codes_cleaned = minus(codes_cleaned,removed_data)
country_codes_cleaned.sort()

# Membuat list nama negara 

country_names = list()

for code in data_country:  
    if code["alpha-3"] in country_codes_cleaned :
        country_names.append(code["name"])

# Memasangkan kode negara dengan nama negara 
countryncode = jsonasdf.set_index("alpha-3")["name"].to_dict()

# Memasangkan kode negara dengan region
countrynregion = jsonasdf.set_index("alpha-3")["region"].to_dict()

# Memasangkan kode negara dengan region
countrynregion = jsonasdf.set_index("alpha-3")["sub-region"].to_dict()

# a. Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N, dimana nilai
#   N dapat dipilih oleh user secara interaktif. Nama negara N dituliskan secara lengkap bukan kode
#   negaranya.

st.subheader("Crude Oil Production History by Country")

# dropdown1 = st.multiselect('Choose country:', country_names)
# dropdown1 = input("Negara:")

# for country in data_country :
#     if country["name"] == dropdown1:
#         country_code = country ["alpha-3"]
#     else:
#         continue

# df1 = df_cleaned.loc[df_cleaned["kode_negara"] == country_code,["tahun","produksi"]]
# print (df1)

# st.line_chart(data=df1, width = 10, height = 400)

# b. Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T, dimana
#    nilai B dan T dapat dipilih oleh user secara interaktif.

# st.write("Crude Oil Production History by Country")
# slider_country = st.slider("Top number of countries")
# slider_year = st.slider("Year")

# slider1_country = input("Masukkan berapa besar negara: ")
# dropdown2 = input("Masukkan tahun (1971-2015): ")

# df2_year = df_cleaned.loc[df_cleaned["tahun"] == int(dropdown2),["kode_negara","produksi"]]
# df2_sorted = df2_year.sort_values(["produksi"], ascending = False)  #mengurutkan data produksi dari terbesar ke terkecil
# df2_reindexed = df2_sorted.reset_index(drop=True)
# df2_final = df2_reindexed[0:int(slider1_country)]
# print(df2_final)

# c. Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif
#    keseluruhan tahun, dimana nilai B dapat dipilih oleh user secara interaktif.

# st.write("Cumulative Crude Oil Production")
# slider2_country = input("Masukkan berapa besar negara: ")

# sumdict = dict()

# for country in country_codes_cleaned:
#     df_country = df_countryindex.loc[country]
#     df_sum = df_country["produksi"].sum()
#     sumdict[country] = df_sum

# sorted_dict = dict(sorted(sumdict.items(), key=lambda x: x[1], reverse=True))

# for country in data_country :
#     if country["name"] == slider2_country:
#         country_code = country ["alpha-3"]
#     else:
#         continue

# df3 = pd.DataFrame(sorted_dict.items(), columns=['Country', 'Production'])
# df3_final = df3[0:int(slider2_country)]

# d. Informasi yang menyebutkan: 
#    (1) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terbesar pada tahun T dan keseluruhan tahun
#    (2) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terkecil (tidak sama dengan nol) pada tahun T dan keseluruhan tahun
#    (3) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi sama dengan nol pada tahun T dan keseluruhan tahun

years = df_cleaned['tahun'].tolist()
years = list(dict.fromkeys(years))

slider3_year = input("Masukkan tahun(1971-2015): ")
# slider3_year = st.slider

df4 = df_cleaned.loc[df_cleaned["tahun"] == int(slider3_year)]
df4_cleaned = df4[df4['produksi'] != 0]
df4_cleaned_sorted = df4_cleaned.sort_values(["produksi"], ascending=False)

index_biggest_production = df4_cleaned["produksi"].idxmax()
biggest_production = df_cleaned.kode_negara[index_biggest_production]
country_biggest_production = countryncode[biggest_production]           # Nama negara dgn produksi terbanyak pada tahun T

index_smallest_production = df4_cleaned["produksi"].idxmin()
smallest_production = df_cleaned.kode_negara[index_smallest_production]
country_smallest_production = countryncode[smallest_production]           # Nama negara dgn produksi terkecil pada tahun T

df4_production0 = df4[df4['produksi'] == 0]
countries_production0 = df4_production0["kode_negara"].tolist()

# Negara dengan produksi terbesar 
# Negara dengan produksi terkecil
# Negara dengan produksi terbesar 
