import streamlit as st
import datarobot as dr
import datarobotx as drx
import joblib
import requests
import json

mimetype = 'text/plain'
charset = 'UTF-8'
API_URL = ''
API_KEY = ''
DATAROBOT_KEY = ''
DEPLOYMENT_ID = '65c1eedb9384ac833ee8abby'
headers = {
        'Content-Type': '{};charset={}'.format(mimetype, charset),
        'Authorization': 'Bearer {}'.format(API_KEY),
        'DataRobot-Key': DATAROBOT_KEY,
    }
url = API_URL.format(deployment_id=DEPLOYMENT_ID)

st.title("Chat Bot with DR Deployment")

def get_deployment_response(prompt, model):
    data = json.dumps({
        "question": prompt
        })
    predictions_response = requests.post(
        url,
        data=data,
        headers=headers,
    )
    return json.loads(predictions_response.content)

if('messages' not in st.session_state):
    st.session_state.messages = [{'role':'assistant','content':'Hello, How can I help you today?'}]

if('chat_history' not in st.session_state):
    st.session_state.chat_history = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if(prompt:=st.chat_input("Hi")):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({'role':'user','content':prompt})
    response = 'Hello, please ask your question!'
    if(prompt!='Hi'):
        response_full = get_deployment_response(prompt)
        response = response_full.get('answer')
        #st.session_state.chat_history = completion['completion']['chat_history']
        print(response_full)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({'role':'assistant','content':response})