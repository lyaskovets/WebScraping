import requests


def use_get():
    response = requests.get('https://www.lejobadequat.com/emplois')
    print('statusCode: ', response.status_code)
    print('text:', response.text)


def use_post():
    payload = {
        "action": "facetwp_refresh",
        "data": {
            "facets": {
                "recherche": [],
                "ou": [],
                "type_de_contrat": [],
                "fonction": [],
                "load_more": [
                    2
                ]
            },
            "frozen_facets": {
                "ou": "hard"
            },
            "http_params": {
                "get": [],
                "uri": "emplois",
                "url_vars": []
            },
            "template": "wp",
            "extras": {
                "counts": True,
                "sort": "default"
            },
            "soft_refresh": 1,
            "is_bfcache": 1,
            "first_load": 0,
            "paged": 2
        }
    }
    response = requests.post('https://www.lejobadequat.com/emplois', json=payload)
    print('statusCode: ', response.status_code)
    content = response.json()['template']
    print('content: ', content)




def use_header():
    response = requests.get('https://www.lejobadequat.com/emplois')

if __name__ == '__main__':
    use_get()
    # use_post()
