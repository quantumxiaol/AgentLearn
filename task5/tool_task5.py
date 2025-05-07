from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
from openai import OpenAI as OpenAIClient
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.schema.runnable import RunnableSequence
import io
import yaml
import os
import sys
from langchain.agents import tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MCPtool.testtool import getPrimeinNumN_tool

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config

if __name__ == "__main__":
    img_path = "bus.jpg"

    model,api_key,api_base = get_openai_config()

    tools = [getPrimeinNumN_tool]
    llm = ChatOpenAI(model=model, temperature=0, api_key=api_key, base_url=api_base, timeout=120)
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    
    query = "100以内的质数有哪些？"
    response = agent.invoke({"input": query})
    print("\n最终回答：")
    print(response['output'])