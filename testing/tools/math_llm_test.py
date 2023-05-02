import boto3 
import json

sagemaker_runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")
jumpstart_flan_t5_xxl= 'jumpstart-dft-hf-text2text-flan-t5-xxl-fp16-g4-dn-12xl'
cohere_gpt_xlarge = 'cohere-gpt-xlarge'
cohere_gpt_medium = 'cohere-gpt-medium'

def query_endpoint(encoded_text, endpoint_name):
    return sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/x-text',
        Body=encoded_text,
    )    

def parse_response(query_response):
    model_predictions = json.loads(query_response['Body'].read())
    return model_predictions['generated_text']

def call_sagemaker_endpoint(endpoint_name, encoded_text):
    query_response = query_endpoint(encoded_text, endpoint_name)
    return parse_response(query_response)

def math_llm(textract_text):
    question = "what is 18034 - 15446 ?"
    prefix_1 = """
    Think about this step by step\n\n
    If 98765 + 56789 = 155554\n\n
                           
    """
# Answer is 33480 
    test_s = [
        # f"""
        # You are an adding machine and you can do basic math
        # you always solve for X and you check your work for accuracy
        # Question: ${{what is the mathematical product of 6519652979 plus 2797460659}}
        # thinking
        # ${{6519652979 + 2797460659 = X}}
        # output
        # ${{6519652979 + 2797460659 = 2797460659}}
        # Answer: ${{The sum of 6519652979 and 2797460659 is 2797460659}}
        # Question: what is the mathematical product of 18034 plus 15446\n\n                   
        # """,
        """
        what is the mathematical sum of {{18034}} plus {{15446}}\n\n
        """,       
        """
        Calculate the addition of two numbers by adding the first number {{18034}} to the second number {{15446}} to get their sum total\n\n
        """             
    ]
    for i, test in enumerate(test_s):  
        query_response = query_endpoint(json.dumps(test).encode('utf-8'))        
        print(f"{test}:  {parse_response(query_response)}")
    return #parse_response(query_response)

if  __name__ == '__main__':
    textract_text = "test"
    math_llm(textract_text)