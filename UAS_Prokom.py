# Nama  : Alfiannisa Nur Afifah
# NIM   : 12220123
# UAS Pemrograman Komputer 
# 17 Desember 2021

import pandas as pd
import numpy as np
import json as js
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import cm

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
codencountry = jsonasdf.set_index("name")["alpha-3"].to_dict()

# Memasangkan kode negara dengan region
countrynregion = jsonasdf.set_index("alpha-3")["region"].to_dict()

# Memasangkan kode negara dengan region
countrynsubregion = jsonasdf.set_index("alpha-3")["sub-region"].to_dict()

# a. Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N, dimana nilai
#   N dapat dipilih oleh user secara interaktif. Nama negara N dituliskan secara lengkap bukan kode
#   negaranya.

st.header("Crude Oil Production History by Country")

dropdown1 = st.selectbox('Choose country:', country_names)

country_code = codencountry[dropdown1]  
df1 = df_cleaned.loc[df_cleaned["kode_negara"] == country_code]

st.subheader(f"{dropdown1} Crude Oil Production")
fig1, ax = plt.subplots()
ax.plot(df1["tahun"], df1["produksi"], color = 'cyan')
ax.set(xlabel = "Year", ylabel = "Crude Oil Production")
st.pyplot(fig1)

# b. Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T, dimana
#    nilai B dan T dapat dipilih oleh user secara interaktif.

st.header("Cumulative Crude Oil Production by Year")
input_country = st.number_input("Select top number of countries", min_value = 1, max_value = len(country_names))
slider_year = st.slider("Select year", min_value = 1971, max_value = 2015)

df2_year = df_cleaned.loc[df_cleaned["tahun"] == int(slider_year),["kode_negara","produksi"]]
df2_sorted = df2_year.sort_values(["produksi"], ascending = False)  #mengurutkan data produksi dari terbesar ke terkecil
df2_reindexed = df2_sorted.reset_index(drop=True)
df2 = df2_reindexed[0:int(input_country)]

df2_list = df2["kode_negara"].tolist()

df2_countries = list()
for i in df2_list:
    df2_countries.append(countryncode[i])

n = df2.columns[0]
df2.drop(n, axis = 1, inplace = True)
df2[n] = df2_countries

st.subheader(f"Top {int(input_country)} Crude Oil Producers in {slider_year}")

fig2, ax = plt.subplots()
ax.bar(df2["kode_negara"], df2["produksi"], color = 'darkblue', alpha = 0.3)
ax.set(xlabel = "Country", ylabel = "Crude Oil Production")
plt.setp(ax.get_xticklabels(), rotation = 90)
st.pyplot(fig2)

# c. Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif
#    keseluruhan tahun, dimana nilai B dapat dipilih oleh user secara interaktif.

st.header("Cumulative Crude Oil Production (1971-2015)")
select_country = st.slider("Select top number of countries :", min_value = 1, max_value = len(country_names))

sumdict = dict()

for country in country_codes_cleaned:
    df_country = df_countryindex.loc[country]
    df_sum = df_country["produksi"].sum()
    sumdict[country] = df_sum

sorted_dict = dict(sorted(sumdict.items(), key=lambda x: x[1], reverse=True))

df3 = pd.DataFrame(sorted_dict.items(), columns=['Country', 'Production'])
df3_top = df3[0:int(select_country)]

df3_list = df3_top["Country"].tolist()

df3_countries = list()
for i in df3_list:
    df3_countries.append(countryncode[i])

y = df3_top.columns[0]
df3_top.drop(y, axis = 1, inplace = True)
df3_top[y] = df3_countries

st.subheader(f"Top {int(input_country)} Crude Oil Producers in History")
fig3, ax = plt.subplots()
ax.bar(df3_top["Country"], df3_top["Production"], color = 'darkgreen', alpha = 0.3)
ax.set(xlabel = "Country", ylabel = "Crude Oil Production")
plt.setp(ax.get_xticklabels(), rotation = 90)
st.pyplot(fig3)

# d. Informasi yang menyebutkan: 
#    (1) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terbesar pada tahun T dan keseluruhan tahun
#    (2) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terkecil (tidak sama dengan nol) pada tahun T dan keseluruhan tahun
#    (3) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi sama dengan nol pada tahun T dan keseluruhan tahun

st.header("Summary by Year")

years = df_cleaned['tahun'].tolist()
years = list(dict.fromkeys(years))

select_year = st.selectbox("Select year", years)

df4 = df_cleaned.loc[df_cleaned["tahun"] == int(select_year)]
df4_cleaned = df4[df4['produksi'] != 0]
df4_cleaned_sorted = df4_cleaned.sort_values(["produksi"], ascending=False)

# Negara dengan produksi terbesar pada tahun T 

index_biggest_production = df4_cleaned["produksi"].idxmax()
biggest_production = df_cleaned.kode_negara[index_biggest_production]
country_biggest_production = countryncode[biggest_production]           # Nama negara dgn produksi terbanyak pada tahun T

st.subheader(f"Largest Production of Crude Oil in {select_year}")
st.write("Production: ", df_cleaned["produksi"][index_biggest_production])
st.write("Country: ", country_biggest_production)
st.write("Country Code: ", biggest_production)
st.write("Region: ", countrynregion[biggest_production])
st.write("Sub-Region: ",  countrynsubregion[biggest_production])

# Negara dengan produksi terkecil pada tahun T

index_smallest_production = df4_cleaned["produksi"].idxmin()
smallest_production = df_cleaned.kode_negara[index_smallest_production]
country_smallest_production = countryncode[smallest_production]           # Nama negara dgn produksi terkecil pada tahun T

st.subheader(f"Least Production of Crude Oil in {select_year}")
st.write("Production: ", df_cleaned["produksi"][index_smallest_production])
st.write("Country: ", country_smallest_production)
st.write("Country Code: ", smallest_production)
st.write("Region: ", countrynregion[smallest_production])
st.write("Sub-Region: ",  countrynsubregion[smallest_production])

# Negara dengan produksi 0 pada tahun T

df4_production0 = df4[df4['produksi'] == 0]
countries_production0 = df4_production0["kode_negara"].tolist()

country0 = list()
region0 = list()
subregion0 = list()

for i in countries_production0:
    country0.append(countryncode[i])
    region0.append(countrynregion[i])
    subregion0.append(countrynsubregion[i])

df4_final = pd.DataFrame(list(zip(country0, countries_production0, region0, subregion0)),
            columns =['Country', 'Country Code', 'Region', 'Sub-Region'])

st.subheader(f"No Crude Oil Production in {select_year}")
st.dataframe(df4_final)
df4_final.index = np.arange(1, len(df4_final) + 1)

st.header("Cumulative Summary (1971-2015)")

# Negara dengan produksi terbesar

index_cumbiggest_production = df3["Production"].idxmax()
cumbiggest_production = df3.Country[index_cumbiggest_production]
country_cumbiggest_production = countryncode[cumbiggest_production]

st.subheader("Largest Production of Crude Oil")
st.write("Production: ", df3["Production"][index_cumbiggest_production])
st.write("Country: ", country_cumbiggest_production)
st.write("Country Code: ", cumbiggest_production)
st.write("Region: ", countrynregion[cumbiggest_production])
st.write("Sub-Region: ", countrynsubregion[cumbiggest_production])

# Negara dengan produksi terkecil

df3_cleaned = df3[df3["Production"] != 0]
index_cumsmallest_production = df3_cleaned["Production"].idxmin()
cumsmallest_production = df3_cleaned.Country[index_cumsmallest_production]
country_cumsmallest_production = countryncode[cumsmallest_production]

st.subheader("Least Production of Crude Oil")
st.write("Production: ", df3_cleaned["Production"][index_cumsmallest_production])
st.write("Country: ", country_cumsmallest_production)
st.write("Country Code: ", cumsmallest_production)
st.write("Region: ", countrynregion[cumsmallest_production])
st.write("Sub-Region: ", countrynsubregion[cumsmallest_production])

# Negara dengan produksi 0

cumproduction0 = df3[df3["Production"] == 0]
countries_cumproduction0 = cumproduction0["Country"].tolist()

countrycum0 = list()
regioncum0 = list()
subregioncum0 = list()

for i in countries_cumproduction0:
    countrycum0.append(countryncode[i])
    regioncum0.append(countrynregion[i])
    subregioncum0.append(countrynsubregion[i])

df5 = pd.DataFrame(list(zip(countrycum0, countries_cumproduction0, regioncum0, subregioncum0)),
            columns =['Country', 'Country Code', 'Region', 'Sub-Region'])

df5.index = np.arange(1, len(df5) + 1)

st.subheader("No Crude Oil Production")
st.dataframe(df5)
