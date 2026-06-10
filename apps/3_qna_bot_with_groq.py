# ##-------PREREQUISITIES-------
# ## LLM Model 
# ## TOOL - Google Search Tool 
# ## Agent 
# ## Memory
# ## Streaming

from dotenv import load_dotenv      ## To load environment variables from .env file such as API KEYS , credentials etc.
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent 
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

llm = ChatGroq(model="openai/gpt-oss-20b", streaming=True)
search = GoogleSerperAPIWrapper()
tools = [search.run]

### MAINTAINS THE MEMORY ----------
if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()
    ### SAVES THE PREVIOUSLY ASKED QUESTIONS --------
    st.session_state.history = []
    ### SAVES THE PREVIOUSLY ASKED QUESTIONS --------
    

### MAINTAINS THE MEMORY ----------

agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt="An Ai agent that can search on Google."
)

print(st.session_state.memory)

#### BUILDING WEB INTERFACE -------------
st.subheader("QuickAnswer - Answers at the speed of thought")

### DISPLAYING ALL THE MESSAGES IN CHATBOT ----------
for message in st.session_state.history:
    role = message["role"]
    content= message["content"]
    st.chat_message(role).markdown(content)
### DISPLAYING ALL THE MESSAGES IN CHATBOT ----------
    
query = st.chat_input("Ask Anything?.....")
if query:
    st.chat_message("user").markdown(query)
    ### SAVES THE PREVIOUSLY ASKED QUESTIONS --------
    st.session_state.history.append({"role":"user", "content":query})
    ### SAVES THE PREVIOUSLY ASKED QUESTIONS --------
    
    response = agent.invoke(
    {"messages":[{"role":"user", "content":query}]},
    {"configurable":{"thread_id":"1"}},
    stream_mode="messages"
)
    ###------STREAMING THE CHATS IN REAL TIME 
    ai_container = st.chat_message("ai")
    with ai_container:
        space = st.empty()
        
        message=""
        
        for chunk in response:
            message = message + chunk[0].content
            space.write(message)
            
        st.session_state.history.append({"role":"ai", "content":message})
            
    ###------STREAMING THE CHATS IN REAL TIME 

    # answer = response["messages"][-1].content
    # st.chat_message("ai").markdown(answer)
    # ### SAVES THE PREVIOUSLY ASKED QUESTIONS --------
    # st.session_state.history.append({"role":"ai", "content":answer})
    ### SAVES THE PREVIOUSLY ASKED QUESTIONS --------


### PROBLEM 1 TILL THE ABOVE LINE OF CODE :::: 

###---- Every time we ask a question , it will replace the previously asked question and its answer -----###

### PROBLEM 2 TILL THE ABOVE LINE OF CODE :::: 

##---- DOES NOT HAVE THE MEMORY YET ------Every time I ask the chatbot a question related to an event or a person by using the pronouns after I have already mentioned the same using nouns , then it will not remember what I am talking about ....###


#### BUILDING WEB INTERFACE -------------

# response = agent.invoke(
#     {"messages":[{"role":"user", "content":"Who is the PM of India?"}]},
#     {"configurable":{"thread_id":"1"}}
# )

# print(response["messages"][-1].content)