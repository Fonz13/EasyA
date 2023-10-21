import streamlit as st
from PIL import Image
from pix2tex.cli import LatexOCR
import openai

openai.api_key = "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"


model = LatexOCR()
st.markdown("<style>footer {display:none;}</style>", unsafe_allow_html=True)


st.title("EasyA")
uploaded_file = st.file_uploader("Upload your file here...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    prompt = model(image)
    st.latex(fr''' {prompt} ''')
    
    message = f'''Answer the following prompt about an assignment. If the answer contains math, wrap all equations and expressions in latex . 
        Assignment Description: 
        {prompt} 
        
        
        Assignment Content: 
        {"make another question like this. take a deep breath and think about it."}
    '''.strip()
    
    #preprocess prompt


    response= openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant that reads math questions and create similair new ones."},
                {"role": "user", "content": message}
        ]
        )
    
    st.latex(fr''' {response.choices[0].message.content} ''')

