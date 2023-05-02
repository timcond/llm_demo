import os

os.environ["SERPAPI_API_KEY"] = "3bf2924ce8c0e516bb992d1b4bfe01983dd19532c9a4bd2ae9907fcf6b64469a"
from typing import Optional, List
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from cohere_sagemaker import Client
from langchain.llms.base import LLM

cohere_gpt_xlarge = 'cohere-gpt-xlarge'
cohere_medium_2xlarge = 'cohere-gpt-medium-p3-2xlarge'

class SageMakerLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "cohere"
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        client = Client(endpoint_name=cohere_medium_2xlarge)
        response = client.generate(
            prompt=prompt,
            max_tokens=100,
            temperature=0,
            k=0,
            p=0.75,
            frequency_penalty=0,
            presence_penalty=0,
            truncate="NONE",
            stop_sequences=["--"]            
        )
        
        return response.generations[0].text

llm = SageMakerLLM()
tools = load_tools(["llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("what is 18034 minus 15446 ? --")

'''
    This code NEVER EVER CALLS THE TOOL EVER!!!!!
'''