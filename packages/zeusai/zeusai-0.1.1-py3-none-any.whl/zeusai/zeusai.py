import requests

class ZeusAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "http://ai.zeusdrive.cloud:26509/send_message"
    
    def send_message(self, prompt):
        prompt += "\nEscreva em português, por favor."
        
        data = {'message': prompt}
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        response = requests.post(self.url, data=data)
        return response.text
