import streamlit as st
import pickle
import numpy as np

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://i.pcmag.com/imagery/roundups/02naaOkVLe7DIiejFUyDPJp-31..v1588859331.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()

# import the model
pipe = pickle.load(open('model.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

st.title("Laptop Price Predictor")

# brand
company = st.selectbox('Brand',df['Company'].unique())

# type of laptop
type_ = st.selectbox('Type',df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM, GB',[2,4,6,8,12,16,24,32,64])

# weight
weight = st.number_input('Weight of the Laptop, kg')

# Touchscreen
touchscreen = st.selectbox('Touchscreen',['No','Yes'])

# IPS
ips = st.selectbox('IPS',['No','Yes'])

# screen size
inches = st.number_input('Screen Size, inch')

# resolution
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

#cpu
cpu = st.selectbox('CPU',df['Cpu Brand'].unique())

hdd = st.selectbox('HDD, GB',[0,128,256,512,1024,2048])

ssd = st.selectbox('SSD, GB',[0,8,128,256,512,1024])

hybrid = st.selectbox('Hybrid Storage, GB', [0,256,508,512,1000])

flash = st.selectbox('Flash Storage, GB', [0,16,32,64,128,256,512])

gpu = st.selectbox('GPU',df['Gpu brand'].unique())

os = st.selectbox('OS',df['os'].unique())

if st.button('Predict Price'):
    # query
    ppi = None
    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'Yes':
        ips = 1
    else:
        ips = 0

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5/inches
    query = np.array([company,type_,inches,cpu,ram,weight,touchscreen,ips,ppi,ssd,hdd,hybrid,flash,gpu,os])

    query = query.reshape(1,15)
    st.header("The predicted price of this configuration is around Rs. " + str(int(np.exp(pipe.predict(query)[0]))))