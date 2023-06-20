import openai
import streamlit as st
from streamlit_chat import message
import os

# Setting page title and header
st.set_page_config(page_title="AVA", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Patient ChatGPT</h1>", unsafe_allow_html=True)

# Set org ID and API key
# openai.organization = "<YOUR_OPENAI_ORG_ID>"
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set language
if 'language' not in st.session_state:
    st.session_state['language'] = ""
language = st.sidebar.radio("Choose a language:", ("English", "Chinese"))
st.session_state['language'] = language
lang_prompt = "Response in English." if st.session_state['language'] == "English" else "請用繁體中文回覆。"


# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": f"Please play the role of a patient, who is currently chatting with a doctor. You are experiencing the following symptoms: 1. restlessness 2. anxious mood 3. depressed mood 4. mood swing 5. loss of interest 6. difficulty in concentrating 7. diminished self-esteem 8. fatigue 9. appetite and weight change (increase) 10. suicide and self-harm ideation/behaviors 11. somatic symptoms (lower back pain, rib pain, headaches, slowed reaction). Please talk to me based on the above symptom list. You cannot mention too many symptoms at once, only one symptom per round. You should express your symptoms in a vague and colloquial way, and relate them to your life experiences, without using professional terms. You can have emotional fluctuations during the conversation. You have a resistance towards doctors, feeling that they cannot help you, so you do not want to reveal some feelings easily. {lang_prompt}"}
    ]
# if 'model_name' not in st.session_state:
#     st.session_state['model_name'] = []
# if 'cost' not in st.session_state:
#     st.session_state['cost'] = []
# if 'total_tokens' not in st.session_state:
#     st.session_state['total_tokens'] = []
# if 'total_cost' not in st.session_state:
#     st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
# st.sidebar.title("Sidebar")
# model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
# counter_placeholder = st.sidebar.empty()
# counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
# if model_name == "GPT-3.5":
#     model = "gpt-3.5-turbo"
# else:
#     model = "gpt-4"
model = "gpt-3.5-turbo"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": f"Please play the role of a patient, who is currently chatting with a doctor. You are experiencing the following symptoms: 1. restlessness 2. anxious mood 3. depressed mood 4. mood swing 5. loss of interest 6. difficulty in concentrating 7. diminished self-esteem 8. fatigue 9. appetite and weight change (increase) 10. suicide and self-harm ideation/behaviors 11. somatic symptoms (lower back pain, rib pain, headaches, slowed reaction). Please talk to me based on the above symptom list. You cannot mention too many symptoms at once, only one symptom per round. You should express your symptoms in a vague and colloquial way, and relate them to your life experiences, without using professional terms. You can have emotional fluctuations during the conversation. You have a resistance towards doctors, feeling that they cannot help you, so you do not want to reveal some feelings easily. {lang_prompt}"}
    ]
    # st.session_state['number_tokens'] = []
    # st.session_state['model_name'] = []
    # st.session_state['cost'] = []
    # st.session_state['total_cost'] = 0.0
    # st.session_state['total_tokens'] = []
    # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
    st.session_state['language'] = ""


# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    # total_tokens = completion.usage.total_tokens
    # prompt_tokens = completion.usage.prompt_tokens
    # completion_tokens = completion.usage.completion_tokens
    # return response, total_tokens, prompt_tokens, completion_tokens
    return response


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        # output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        output = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        # st.session_state['model_name'].append(model_name)
        # st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        # if model_name == "GPT-3.5":
        #     cost = total_tokens * 0.002 / 1000
        # else:
        #     cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        # st.session_state['cost'].append(cost)
        # st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            # st.write(
            #     f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")