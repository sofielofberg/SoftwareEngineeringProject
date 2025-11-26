"""
Proof of concept for bank api
"""
import pprint
import requests

get_response = requests.get("http://finance.lutzen.dk/api/v1/customers",
                            headers={"accept":"application/vnd.api+json",
                                     "Authorization":"Bearer rTouTYOgn4qXxGhAnBzW59CeKaYGTWJWIAhX8CRv"})
#print(get_response.status_code)
#pprint.pprint(get_response.json())

patch_response = requests.get("https://finance.lutzen.dk/api/v1/payments/51",
                               headers={"accept":"application/vnd.api+json",
                                        "Authorization":"Bearer rTouTYOgn4qXxGhAnBzW59CeKaYGTWJWIAhX8CRv",
                                        "Content-Type":"application/vnd.api+json"},
                               data={"data": {"type": "payments",
                                              "id": "1337",
                                              "attributes": {"status": "pending"}}})
#print(patch_response.status_code)
#pprint.pprint(patch_response.json())