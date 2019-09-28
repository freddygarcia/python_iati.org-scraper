import requests

BASE_URL = 'http://datastore.iatistandard.org/api/1/access/activity.csv?{}&stream=True'

def download(url):
    # get file content from url
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f'Cannot retrieve file (reason: {r.reason})')
    file_content = r.text
    return file_content

def build_url(url, query_dict):
    # build url using query params dict
    prepare_args = tuple(x + '=' +  '|'.join(y) for x, y in query_dict.items())
    query = '&'.join(prepare_args)
    final_url = BASE_URL.format(query)
    return final_url

def retrieve_file(query_dict):
    # abstration to download file from url
    url = build_url(BASE_URL, query_dict)
    f_content = download(url)
    return f_content
