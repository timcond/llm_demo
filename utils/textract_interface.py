import boto3
import trp 
import trp.trp2 as t2
import pandas as pd 
from textractprettyprinter.t_pretty_print import convert_table_to_list

textract_client = boto3.client('textract')

def detect_text(doc):
    with open(doc, 'rb') as doc_file:
        doc_bytes = doc_file.read()
    try:    
        res = textract_client.detect_document_text(Document={'Bytes': doc_bytes})
        return ' '.join(
            [x.get('Text') for x in res.get('Blocks') if x and x.get('Text')]
        )
    except Exception as e:
        print(e)
        return e

def detect_tables_forms(doc):
    with open(doc, 'rb') as doc_file:
        doc_bytes = doc_file.read()
    try:    
        res = textract_client.analyze_document(Document={'Bytes': doc_bytes}, FeatureTypes=['TABLES'])
        dfs = []    
        tdoc = trp.Document(res)
        for page in tdoc.pages:
            for table in page.tables:
                tab_list = convert_table_to_list(trp_table=table)
                dfs.append(pd.DataFrame(tab_list))
        return dfs[0]
    except Exception as e:
        print(e)
        return e

def run_queries(doc):
    with open(doc, 'rb') as doc_file:
        doc_bytes = doc_file.read()
    try:
        return _textract_queries(doc_bytes)
    except Exception as e:
        print(e)
        return e

def _textract_queries(doc_bytes):
    res = textract_client.analyze_document(
        Document={'Bytes': doc_bytes}, 
        FeatureTypes=['QUERIES'],
        QueriesConfig={
            'Queries': [
                {
                    'Text': 'Who is the Chief Executive Officer?',
                    'Alias': 'CEO',
                    'Pages': [
                        '*',
                    ]
                },
                {
                    'Text': 'What is the company name?',
                    'Alias': 'Company',
                    'Pages': [
                        '*',
                    ]
                },
            ]
        }
    )
    t2doc = t2.TDocumentSchema().load(res)
    query_answers = t2doc.get_query_answers(page=t2doc.pages[0])
    query_response = []
    for query in query_answers:
        query_json = {'Query': query[0], 'Answer': query[2]}
        query_response.append(query_json)
    return query_response


if  __name__ == "__main__":
    doc_location = "static/examples/amazon-sec-demo.pdf"
    run_queries(doc_location)
    # detect_tables_forms(doc_location)
    # detect_text(doc_location)
