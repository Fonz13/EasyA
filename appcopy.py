import streamlit as st
from PIL import Image
from pix2tex.cli import LatexOCR
import openai
from dotenv import load_dotenv
import os
import re
load_dotenv()
import re
openai.api_key = os.getenv('OPEN_AI_KEY')

st.markdown("<style>footer {display:none;}</style>", unsafe_allow_html=True)
st.title("EasyA")


model = LatexOCR()



text = r"""## Step 1: Find the derivative of the given function
To find the derivative of a function with respect to x, we need to differentiate each term of the function using the rules of differentiation.

The given function is:
$$ f(x) = 3x^2 - 4x + 7 $$

To differentiate each term, we apply the power rule and the constant rule of differentiation.

The power rule states that the derivative of x raised to the power of n is n times x raised to the power of n-1.

The constant rule states that the derivative of a constant is 0.

Differentiating each term of the given function, we have:

$$ f'(x) = \frac{d}{dx}(3x^2) - \frac{d}{dx}(4x) + \frac{d}{dx}(7) $$
## Step 1.5: Additional Challenge

Applying the power rule and constant rule, we get:

$$ f'(x) = 6x^{2-1} - 4 \cdot 1 + 0 $$

Simplifying further:

$$ f'(x) = 6x - 4 $$ 

Therefore, the derivative of the given function with respect to x is:
$$ f'(x) = 6x - 4 $$


## Step 2: Additional Challenge
If you want an additional challenge, you can try finding the second derivative of the given function.

"""


if 'count' not in st.session_state:
    st.session_state['count'] = 1
        
if 'text' not in st.session_state:
    st.session_state['text'] = []
    
if 'disabled' not in st.session_state:
    st.session_state['disabled'] = False
    

def text_to_list(text):
    # Regular expression pattern to match titles and content
    pattern = r"## (.*?)\n(.*?)(?=##|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    # Convert matches to a dictionary
    result_dict = {match[0].strip(): match[1].strip() for match in matches}

    t_s = []
    for k, v in result_dict.items():
        t_s.append(("## "+k, v))
        
    return t_s




if st.button('get text'):
    st.session_state['text'] = text_to_list(text)
    st.session_state['count'] = 1
    st.session_state['disabled'] = False




if st.button('Generate next step', disabled=st.session_state.disabled):
    if st.session_state['count'] == len(st.session_state['text'])-1:
        st.session_state.disabled = True

    if st.session_state['count'] <= len(st.session_state['text']):
        for i in range(st.session_state['count']):
            k,v = st.session_state['text'][i]
            st.markdown(k)
            st.markdown(v) 
        st.session_state['count'] += 1
        
        
    
