import os
import pandas as pd
import json
from utils.transformer import Transformer
from api_client.linear_client import LinearClient
pd.set_option('display.max_columns', None) 

def main():
    api_key = os.getenv("LINEAR_API_KEY")
    linear_client = LinearClient(api_key)
    json_dat = linear_client.query_issues()
    # transformer = Transformer()
    # print(transformer.process_linear_cycles(json_dat).info())
    # print(transformer.process_linear_cycles(json_dat).head())
    print(json.dumps(json_dat, indent=4))


if __name__=="__main__":
    main() 