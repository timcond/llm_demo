import os
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "3bf2924ce8c0e516bb992d1b4bfe01983dd19532c9a4bd2ae9907fcf6b64469a"
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")