import requests

class SSLCOMMERZ:
    def __init__(self, settings):
        self.store_id = settings['store_id']
        self.store_pass = settings['store_pass']
        self.issandbox = settings.get('issandbox', True)
        
        if self.issandbox:
            self.base_url = "https://sandbox.sslcommerz.com"
        else:
            self.base_url = "https://securepay.sslcommerz.com"

    def createSession(self, post_body):
        url = f"{self.base_url}/gwprocess/v4/api.php"
        post_body['store_id'] = self.store_id
        post_body['store_passwd'] = self.store_pass
        
        try:
            response = requests.post(url, data=post_body)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"SSLCommerz Error: {e}")
            return {"status": "FAILED", "failedreason": str(e)}
