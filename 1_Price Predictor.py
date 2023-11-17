import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="viz demo")

with open("df.pkl", 'rb') as file:
    df=pickle.load(file)

with open("pipeline.pkl", 'rb') as file:
    pipeline=pickle.load(file)

st.header("Enter your inputs")

# property_type
property_type = st.selectbox('Property Type', ['flat', 'house'])

# sector
sector = st.selectbox("Sector", sorted(df['sector'].unique().tolist()))

#bedRoom
bedroom = float(st.selectbox("Number of Bedroom", sorted(df['bedRoom'].unique().tolist())))

#bathroom
bathroom = float(st.selectbox("Number of Bathroom", sorted(df['bathroom'].unique().tolist())))

#Balcony
balcony = st.selectbox("Balconies", sorted(df['balcony'].unique().tolist()))

#agePossession
property_age = st.selectbox("Property Age", sorted(df['agePossession'].unique().tolist()))

#built_up_area
built_up_area = float(st.number_input("Built up Area"))

# Servant room
servant_room = float(st.selectbox("Servant Room", [0.0, 1.0]))

# store room
store_room = float(st.selectbox("Store Room", [0.0, 1.0]))

# furnishing_type
furnishing_type = st.selectbox("Furnishing Type", sorted(df['furnishing_type'].unique().tolist()))

# luxury_category
luxury_category = st.selectbox("Luxury Category", sorted(df['luxury_category'].unique().tolist()))

# floor_category
floor_category = st.selectbox("Floor Category", sorted(df['floor_category'].unique().tolist()))

if st.button('Predict'):
    # form a dataframe
    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
       'agePossession', 'built_up_area', 'servant room', 'store room',
       'furnishing_type', 'luxury_category', 'floor_category']

# Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)


    # st.dataframe(one_df)

    # predict
    base_price=np.expm1(pipeline.predict(one_df))[0]
    low= base_price - 0.22
    high = base_price + 0.22

    # display
    st.text("The price of the flat is between {} crore and {} crore".format(round(low,2), round(high,2)))

