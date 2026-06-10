from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

###----- FOR SINGLE QUERY-----####
# que = "Who is the PM of India?"

# result = llm.invoke(que)

# print(result.content)
###----- FOR SINGLE QUERY-----####

####  ---------------------------------------------------------------------------------------#####
###------ FOR ASKING QUERIES IN A LOOP-----####
# while True:
#     query = input("User: ")
    
#     if query.lower() in ["bye", "quit", "exit"]:
#         print("Goodbye...See you soon")
#         break
    
#     res = llm.invoke(query)
#     print("AI: ",res.content)
###------ FOR ASKING QUERIES IN A LOOP-----####


####-----USING STREAMLIT TO BUILD CHATBOT INTERFACE -----####

st.title("👨‍💻 AskBuddy AI QNA BOT")
st.markdown("Welcome to QNA Bot with Langchain and Google Gemini!")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)
    

query = st.chat_input("Ask me anything ?")
if query:
   st.session_state.messages.append({"role": "user", "content": query})
   st.chat_message("user").markdown(query)
   res = llm.invoke(query)
   st.chat_message("ai").markdown(res.content)
   st.session_state.messages.append({"role": "ai", "content": res.content})
   
