import streamlit as st
import os
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
from dotenv import load_dotenv  
from openai import OpenAI


load_dotenv()  
st.title('HDB Resale Estimator (2020 onwards)')  

with st.expander("Important notice"):
    st.write('''
       IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

        Always consult with qualified professionals for accurate and personalized advice.
    ''')

if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
    print("OPENAI_API_KEY is not set")
    exit(1)
else:
    print("OPENAI_API_KEY is set")

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-4o-mini"),
    "./data/resale_data.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True
)

def get_completion(prompt, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create( 
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content

def step_1(original_prompt):
    prompt =  f"""
    Your task is to perform the following steps: 
    Step 1 - Understand if the user wishes to buy or sell a flat. Answer should be "buy" or "sell"
    Step 2 - Extract flat type
    Step 3 - Extract budget
    Step 4 - Extract storey
    Step 5 - Extract town
    
    The response MUST be in the following format:
    action: <step 1 output>
    flat type: <step 2 output> (example: 1 ROOM,2 ROOM,3 ROOM,4 ROOM,5 ROOM,EXECUTIVE,MULTI-GENERATION)
    budget: <step 3 output>
    storey: <step 4 output>
    town: <step 5 output>

    
    <text>
    {original_prompt}
    </text>
    """
    response = get_completion(prompt)
    return response



with st.expander("Towns and flat types"):
    st.write(agent("Give me two separate lists of the available values for the columns town and flat_type").get("output"))
"""
### Instructions
Let me know if you would like to buy or sell a hdb flat in the resale market. 
Include:
1. Town
2. Flat type
3. Budget 
4. Storey (which level)
> Example: I would like to buy a 5 room flat above the 1st floor in the town of geylang. Budget is unlimited.
"""

def step_2(extracted_criteria):
    prompt = f"""
    Based on the criteria below, 
    - for budget, anything resale_price below the specified budget is acceptable.
    - for storey, if the value is within the storey_range is acceptable.
    
    Using the dataset, make the following calculations for sales after 2020 only:
    - if the action is "buy", give the user some statistics of what they can expect to pay for the for the preferences given
    - if the action is "sell", look for sales within the last 12 months,and give the user some statistics of recently sold flats 
    the format can be as follows:
    Count of flats that met the criteria: <count>
    Average resale price: <average price>
    Standard deviation: <standard deviation>
    Minimum resale price: <price>
    25th percentile: <price>
    Median (50th percentile): <price>
    75th percentile: <price>
    Maximum resale price: <price>

    Include a table with the flats used inclusive of all columns in the data set here
    <criteria>
    {extracted_criteria}
    </criteria>
    """
    response = agent(prompt)
    return response.get("output")

og_prompt = st.text_input('How can I help?')

if og_prompt:
    st.write("Here are the criteria we're using for the search:")
    criteria = step_1(og_prompt)
    st.write(criteria)
    st.write(step_2(criteria))



