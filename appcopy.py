import streamlit as st
from PIL import Image
from pix2tex.cli import LatexOCR
import openai
from dotenv import load_dotenv
import os
import re
import pandas as pd
import re

load_dotenv()
openai.api_key = os.getenv("OPEN_AI_KEY")


st.markdown("<style>footer {display:none;}</style>", unsafe_allow_html=True)
st.title("EasyA")

# enables loading images
model = LatexOCR()

SOLUTION_INDEX = 2

if "count" not in st.session_state:
    st.session_state["count"] = SOLUTION_INDEX

if "text" not in st.session_state:
    st.session_state["text"] = []

if "disabled" not in st.session_state:
    st.session_state["disabled"] = True

if "disabled_solve" not in st.session_state:
    st.session_state["disabled_solve"] = True

if "question_index" not in st.session_state:
    st.session_state["question_index"] = 0

if "question_output" not in st.session_state:
    st.session_state["question_output"] = []


def text_to_list(text):
    """
    Takes a prompt formatted as a markdown string and returns a list of tuples
    key: ## TITLE
    value: CONTENT
    """
    # Regular expression pattern to match titles and content
    pattern = r"## (.*?)\n(.*?)(?=##|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    # Convert matches to a dictionary
    result_dict = {match[0].strip(): match[1].strip() for match in matches}

    t_s = []
    for k, v in result_dict.items():
        t_s.append(("## " + k, v))

    return t_s


database = pd.read_csv(
    "/Users/fonzieforsman/Desktop/github/EasyA/db/EasyA_Single_Variable_Calculus.csv"
)


# Logic to pick a question from database
if st.button(f"Get question {st.session_state['question_index']+1}"):
    st.markdown(database.Question.iloc[st.session_state["question_index"]])
    st.session_state["question_output"] = (
        "# Question:",
        database.Question.iloc[st.session_state["question_index"]],
    )
    st.session_state["disabled"] = True
    st.session_state["disabled_solve"] = False
    st.session_state["question_index"] = (
        st.session_state["question_index"] + 1
        if st.session_state["question_index"] < len(database) - 1
        else 0
    )


if st.button(
    "Generate a similair Question", disabled=st.session_state["disabled_solve"]
):
    message = f"""Generate a similar question as this assignment:
    {st.session_state['question_output'][1]} 
    
    I wan't a similar one of both in design and difficulty:  
    
    Wrap all equations and expressions by wrapping them in "$" or "$$". 
    For example, here is how you do a math equation in Markdown in the desired output:
    $$ x^2 + y^2 = z^2 $$
    
    Only answer with the assignment.

    """.strip()

    # preprocess prompt
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that reads math questions and create similair new ones.",
            },
            {"role": "user", "content": message},
        ],
        temperature=0.9,
    )

    st.session_state["question_output"] = (
        "# Question:",
        response.choices[0].message.content,
    )
    st.markdown(response.choices[0].message.content)
    st.session_state["disabled"] = True
    st.session_state["disabled_solve"] = False

if st.button("Solve problem", disabled=st.session_state["disabled_solve"]):
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
    {st.session_state['question_output']} 

    """.strip()

    # preprocess prompt
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that reads math questions and solves them.",
            },
            {"role": "user", "content": message},
        ],
        temperature=0.9,
    )
    text_list = [st.session_state["question_output"]]
    text_list.extend(text_to_list(response.choices[0].message.content))
    st.session_state["text"] = text_list
    st.session_state["count"] = 2
    st.session_state["disabled"] = False


if st.button("Generate next step", disabled=st.session_state.disabled):
    st.session_state["disabled_solve"] = True
    if st.session_state["count"] == len(st.session_state["text"]) - 1:
        st.session_state.disabled = True

    if st.session_state["count"] <= len(st.session_state["text"]):
        for i in range(st.session_state["count"]):
            k, v = st.session_state["text"][i]
            st.markdown(k)
            st.markdown(v)
        st.session_state["count"] += 1
