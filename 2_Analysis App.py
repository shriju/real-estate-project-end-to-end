import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="plotting demo")

st.title("Page 2")

new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()

# geo map
st.header("Sector wise Geo Map-Gurgaun")
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft",  size='built_up_area',color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map", width=1200, height=700,
                        hover_name=group_df.index)

st.plotly_chart(fig, use_container_width=True)

plt.rcParams["font.family"] = "Arial"

st.set_option('deprecation.showPyplotGlobalUse', False)
#word Cloud
st.header("Features WordCloud")
wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='white',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot()

# Area vs. Price
st.header("Area vs. Price")
property_type = st.selectbox('Select Property Type',['flat', 'house'])
if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type']=='house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig2 = px.scatter(new_df[new_df['property_type']=='flat'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig2, use_container_width=True)

# pie chart
st.header("BHK Pie-Chart")
sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'Overall')
selected_sector = st.selectbox("Select Sector", sector_options)

if selected_sector == 'Overall':
    fig3 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig3,use_container_width=True)

else:
    fig3 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig3,use_container_width=True)

# BHK vs price comparision
st.header("Side by Side BHK comparision")
fig4 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')
st.plotly_chart(fig4,use_container_width=True)

# comparision between houses price and flats price
st.header("Side by Side Distplot for Property Type")
sns.distplot(new_df[new_df['property_type'] == 'house']['price'], label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot()








