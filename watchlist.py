import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WishList:
    def __init__(self):
        self.endpoint = os.environ['SHEETY_ENDPOINT']
        self.token = os.environ['SHEETY_TOKEN']
        self.auth = {
            'Authorization': f'Bearer {self.token}'
        }

        # Updated JSON copy of Google Doc
        self.content = None
        self.refresh()

    def add_url(self, url):
        # Package the code found
        if url not in [row['url'] for row in self.content]:
            payload = {
                'product':{
                    'url':url,
                }
            }
            # Update row with info
            response = requests.post(url=self.endpoint, json=payload, headers=self.auth)
            return True
        else:
            return False

    def refresh(self):
        """Update JSON copy of Google Doc sheet"""
        response = requests.get(url=self.endpoint, headers=self.auth)
        self.content = response.json()['products']


if __name__ == "__main__":
    my_wishlist = WishList()
    print(my_wishlist.content)
