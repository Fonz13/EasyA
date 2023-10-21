import streamlit as st
from PIL import Image
from pix2tex.cli import LatexOCR
import openai
from dotenv import load_dotenv
import os
import re

load_dotenv()
openai.api_key = os.getenv("OPEN_AI_KEY")

st.markdown("<style>footer {display:none;}</style>", unsafe_allow_html=True)
st.title("EasyA")
uploaded_file = st.file_uploader(
    "Upload your file here...", type=["png", "jpg", "jpeg"]
)


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

import re

# Regular expression pattern to match titles and content
pattern = r"## (.*?)\n(.*?)(?=##|$)"


if "count" not in st.session_state:
    st.session_state["count"] = 1

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = False

if "text" not in st.session_state:
    st.session_state["text"] = []


if st.button("Generate next step") and st.session_state["uploaded_file"]:
    print(st.session_state["count"])
    for i in range(st.session_state["count"]):
        k, v = st.session_state["text"][i]
        st.markdown(k)
        st.markdown(v)
        st.session_state["count"] += 1


if uploaded_file is not None:
    if st.session_state["uploaded_file"] == True:
        st.session_state["count"] = 1
        st.session_state["text"] = []

    st.session_state["uploaded_file"] = True
    image = Image.open(uploaded_file)

    prompt = model(image)

    message = f"""Answer the following prompt about an assignment. 
    If the answer contains math, wrap all equations and expressions by wrapping them in "$" or "$$" and split up each step of the answer in subsections . 
    
    Follow these step in your response:
    <example>
    ## Step 1: Explain the first step 
    Here is how you do a math equation in Markdown:
    $$ x^2 + y^2 = z^2 $$

    ## Step 2: Explain the second step
    $$ x^2 + y^2 = z^2 $$
    </example>


    Take a deep breath, and solve this problem step-by-step:
    Assignment Description:  
    {prompt} 

    """.strip()

    # preprocess prompt

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that reads math questions and create similair new ones.",
            },
            {"role": "user", "content": message},
        ],
    )
    matches = re.findall(pattern, text, re.DOTALL)

    # Convert matches to a dictionary
    result_dict = {match[0].strip(): match[1].strip() for match in matches}

    t_s = []
    for k, v in result_dict.items():
        t_s.append(("## " + k, v))

    st.session_state["text"] = t_s
    # st.markdown(fr''' {response.choices[0].message.content} ''')
