import os
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "3bf2924ce8c0e516bb992d1b4bfe01983dd19532c9a4bd2ae9907fcf6b64469a"
import json
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms.sagemaker_endpoint import ContentHandlerBase
from langchain.llms.sagemaker_endpoint import SagemakerEndpoint

class SagemakerContentHandler(ContentHandlerBase):
    content_type = "application/json"
    accepts = "application/json"
    
    def transform_input(self, prompt, model_kwargs):
        test = {"text_inputs": prompt}
        return json.dumps(test).encode("utf-8")
    
    def transform_output(self, output):
        response_json = json.loads(output.read().decode("utf-8")).get('generated_texts')
        print(response_json)
        return response_json[0]

SagemakerContentHandler = SagemakerContentHandler()
sagemaker_endpoint = SagemakerEndpoint(
        endpoint_name="jumpstart-dft-hf-text2text-flan-t5-xxl-fp16-g4-dn-12xl",
        model_kwargs={"temperature":1e-10, "max_length": 500},
        region_name="us-east-1", 
        content_handler=SagemakerContentHandler
    )

tools = load_tools(["serpapi", "llm-math"], llm=sagemaker_endpoint)
agent = initialize_agent(tools, sagemaker_endpoint, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power? \n\n")

'''
    This NEVER EVER CALLS THE TOOL
'''