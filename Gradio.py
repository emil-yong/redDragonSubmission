import gradio as gr
import random
import time
import pandas as pd
global_user_message = "";
import requests
import json


def post_message(string):
    url = "http://127.0.0.5:5000/post_string/"

#   Data to be sent as a query parameter
    params = {"data": string}

# Send a GET request with query parameters
    response = requests.post(url, params=params)

    return response
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    # file_upload = gr.File(type="file", label="Upload File")
    clear = gr.Button("Clear")
    
    def user(user_message, history):
        global global_user_message 
        global_user_message = user_message
        print("inside user " + global_user_message)
        return "", history + [[user_message, None]]
        
    def bot(history):
        global global_user_message
        print("outside user " + global_user_message)
        # bot_message = "same as " + global_user_message
        url = "http://127.0.0.5:5000/post_string/"

    #   Data to be sent as a query parameter
        params = {"data": global_user_message}

    # Send a post request with query parameters
        response = requests.post(url, params=params)
        print(response.json().get("output"))
        output_object = response.json().get("output")
        print(output_object)
        # bot_message = json.loads(output_object).get("Item")
        bot_message = output_object

        # try:
        #     df = pd.read_excel("//home//dsta//Desktop//AWQ//first.xlsx")
        #     print(df.head(1))
        
        # except Exception as e:
        #     print(f"Error : {str(e)}")
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            time.sleep(0.05)
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)
    
demo.queue()
demo.launch()


def post_message(string):
    url = "http://127.0.0.5:5000/post_string/"

    print("the string " + string)
#   Data to be sent as a query parameter
    params = {"data": string}

# Send a GET request with query parameters
    response = requests.post(url, params=params)
    print(response)
    string_data = response.decode('utf-8')
    return string_data