
from fastapi import FastAPI , HTTPException
app = FastAPI()

import requests
import json
import pandas as pd
from pydantic import BaseModel

global USER_INPUT

class DataModel:
    data: str


def getEntriesByDateTime(startDateTime,endDateTime):
    # Load the Excel file into a DataFrame
    excel_file_path = '/home/dsta/Desktop/redDragonEnv/code/data.xlsx'
    df = pd.read_excel(excel_file_path)
    print("here")
# Assuming your datetime column is named 'DateTime', you can filter based on the datetime range
    start_datetime = pd.to_datetime(startDateTime)  # Adjust the time component as needed
    end_datetime = pd.to_datetime(endDateTime)    # Adjust the time component as needed

# Filter entries within the datetime range
    filtered_df = df[(df['DateTime'] >= start_datetime) & (df['DateTime'] <= end_datetime)]

# Display or use the filtered DataFrame
    return filtered_df


def getEntriesByLatest(num):
    # Load the Excel file into a DataFrame
    excel_file_path = '/home/dsta/Desktop/redDragonEnv/code/data.xlsx'
    df = pd.read_excel(excel_file_path)


# Filter entries within the datetime range
    filtered_df = df['Assault Incidents'].tail(int(num))

# Display or use the filtered DataFrame
    return filtered_df


def getVicunaAnswer(prompt):
    FASTCHAT_ENDPOINT = "http://127.0.0.1:7862/v1/chat/completions" ## hardcoded api endpoint
    vicuna_response = requests.post(url=FASTCHAT_ENDPOINT, json={
        "model": "vicuna-7b-v1.5",
        "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        "temperature" : 0
    })

    print("Seconds it takes to compute : " + str(vicuna_response.elapsed.total_seconds()))
    response_dict = json.loads(vicuna_response.content.decode("utf-8")) 
    answer = response_dict["choices"][0]["message"]["content"]
    return answer

@app.post("/post_string/")
async def get_posted_string(data: str):
    print("the content the is sending to vicuna: " + data)

    global USER_INPUT 
    USER_INPUT = data
    file_path = '/home/dsta/Desktop/redDragonEnv/code/prompt.txt'

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        prompt_template = file.read()

#    Now, file_contents contains the content of the file as a string
    general_prompt = prompt_template % data

    # FASTCHAT_ENDPOINT = "http://127.0.0.1:7862/v1/chat/completions" ## hardcoded api endpoint
    # vicuna_response = requests.post(url=FASTCHAT_ENDPOINT, json={
    #     "model": "vicuna-7b-v1.5",
    #     "messages": [
    #             {
    #                 "role": "user",
    #                 "content": prompt
    #             }
    #         ],
    #     "temperature" : 0
    # })

    # print("Seconds it takes to compute : " + str(vicuna_response.elapsed.total_seconds()))
    # response_dict = json.loads(vicuna_response.content.decode("utf-8")) 
    # answer = response_dict["choices"][0]["message"]["content"]
    # print(answer)
    get_LLM_response_methodCall = getVicunaAnswer(general_prompt)

    print("rThe result"+get_LLM_response_methodCall.strip())
    get_LLM_Object = json.loads(get_LLM_response_methodCall)
    print("OutCome ::: " + get_LLM_Object["format"])
    get_LLM_reponse , return_answer_to_display = switch_case(get_LLM_Object["format"])

    # # Examples of reading by date and time  and get from the 
    # df_feedback = getEntriesByDateTime('2022-01-01 08:00:00','2022-12-31 17:00:00')  
    # print(df_feedback['Assault Incidents'])

    return {"output": return_answer_to_display}


@app.get("/get_string/")
async def get_string(getData: str):
    print(getData)
    return {"dfdsfsd": f"You provided the following string: {getData}"}


def case1():
    print("Inside getting the latest Entry")
    file_path = '/home/dsta/Desktop/redDragonEnv/code/getLatestEntriesPrompt.txt'

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        prompt_template = file.read()

    global USER_INPUT
#    Now, file_contents contains the content of the file as a string
    getLatestEntriesPrompt = prompt_template % USER_INPUT
    print(getLatestEntriesPrompt)

    get_LLM = getVicunaAnswer(getLatestEntriesPrompt)
    get_LLM_Object = json.loads(get_LLM)
    get_numerical = get_LLM_Object["num"]

    data = getEntriesByLatest(get_numerical)
    your_series = pd.Series(data)

    # Convert the Series to a string
    output_string = your_series.to_string(index=False)
    return output_string
def case3():
    df_feedback = getEntriesByDateTime('2022-01-01 08:00:00','2022-12-31 17:00:00')  
    data = (df_feedback['Assault Incidents'])
    print (data)
    print (type(data))
    print("HIHIHIH")
    # Assuming your Series is named 'your_series'
    your_series = pd.Series(data)

    # Convert the Series to a string
    output_string = your_series.to_string(index=False)
    return output_string

def case2():
    return 'Inside getting the assult Type'

def default_case():
    return 'This is the default case'

def switch_case(case_value):
    print("casee0 " +case_value)
    switch_fn = {
        'getLatestEntriesTemplate': case1,
        'getAssultTypeTemplate': case2,
        'getTimeFrameTemplate': case3,
        # Add more cases as needed
    }

    swtich_return = switch_fn.get(case_value, default_case)()
    return case_value , swtich_return
# where the .py file is main.py
#uvicorn main:app --host 0.0.0.0 --port 8000 --reload
#uvicorn main_server:app --host 127.0.0.5 --port 5000 --reload


# Question: Extract the main idea from the following sentence in json format: "Get me the latest 10 entries of police data"
# Answer: {"Item": "10"}

# Question: Extract the main idea from the following sentence in json format: "Get me the latest 20 entries of police data"
# Answer: {"Item": "20"}

# Question: Extract the main idea from the following sentence in json format: "Get me the latest 30 entries of police data"
# Answer: {"Item": "30"}

# Question: Extract the main idea from the following sentence in json format : "Get me the latest 40 entries of police data"
# Answer: {"Item": "40"}

# Question: Extract the main idea from the following sentence in json format: "Get me the latest 50 entries of police data"
# Answer: {"Item": "50"}

# Question: Extract the main idea from the following sentence in json format : "%s"
# Answer: