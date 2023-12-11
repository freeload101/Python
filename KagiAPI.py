import requests, json, sys, os, logging, yaml

############################################################ FUNCTIONS
class Phantom:
    @staticmethod
    def error(message):
        logging.error(f"Error: {message}")

    @staticmethod
    def debug(message):
        logging.debug(f"Debug: {message}")

class Config:
    def __init__(self, config_file="config.yml"):
        Phantom.debug("Running Config")
        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.KagiFastAPIToken = cfg['KagiFastAPIToken']

def KagiFast(String1):
    config = Config()
    KagiFastAPIToken = config.KagiFastAPIToken
    base_url = 'https://kagi.com/api/v0/fastgpt'
    data = {
        "query": String1,
    }
    headers = {'Authorization': f'Bot {KagiFastAPIToken}'}

    response = requests.post(base_url, headers=headers, json=data)
    data = response.json()
    print(json.dumps(data['data'], indent=4))

if len(sys.argv) <= 1:
    Phantom.debug("Usage: " + sys.argv[0] + " Options ")
    print("""
Normal options:

    -f "String" ( FastGPT is a Kagi service using powerful LLMs to answer user queries running a full search engine underneath. Think ChatGPT, but on steroids and faster! You can try the web app) 
     
    """)
    sys.exit(1)

for x in sys.argv:
    if x == '-f':
        String1 = sys.argv[2]
        KagiFast(String1)
