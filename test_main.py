from urlshort import create_app

def teste_shorten(client):
    response = client.get('/') # / means go to the home page
    assert b'Shorten' in response.data # checking if we have shorten word on the web page
