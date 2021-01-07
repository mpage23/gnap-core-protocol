#!/usr/bin/python3

import urllib.request, json 
import os
import zipfile
from io import BytesIO

print(os.environ)

gh = json.loads(os.environ['INCOMING_HOOK_BODY'])
print(gh)
artifact_tag = gh['artifact_tag']
token = os.environ['GITHUB_TOKEN']

urlbase = 'https://api.github.com/repos/jricher/gnap-core-protocol/actions/artifacts'

if artifact_tag:
    with urllib.request.urlopen(urlbase) as url:
        data = json.loads(url.read().decode())

        for a in data['artifacts']:
            if a['name'] == artifact_tag:
                print('Downloading artifact %s' % artifact_tag)
                print(a)
                req = urllib.request.Request(a['archive_download_url'], headers={
                    'Authorization': 'Bearer ' + token
                })
            
                with urllib.request.urlopen(req) as dl:
                    print('Downloaded file, extracting...')
                    with zipfile.ZipFile(BytesIO(dl.read())) as z:
                        z.extractall('public')
                        print('Extracted files')
