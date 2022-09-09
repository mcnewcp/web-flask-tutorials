from urlshort import create_app

#can we find the word shorten on the homepage?
def test_shorten(client):
    response = client.get('/')
    assert b'Shorten' in response.data