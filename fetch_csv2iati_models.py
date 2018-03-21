from os import mkdir
from os.path import join
import requests
import json


url_tmpl = 'http://csv2iati.iatistandard.org/model/{}.json'
counter = 0
failed = 0

counter -= 1
while True:
    if failed == 20:
        # if there are 20 failures in a row,
        # jump out
        break
    counter += 1
    print(counter)
    try:
        j = requests.get(url_tmpl.format(counter)).json()
    except json.decoder.JSONDecodeError:
        failed += 1
        continue
    ci = j.get('organisation', {}).get('contact-info')
    if ci and ci != {}:
        show = ci.get('add-to-activities', [])
        if len(show) == 0 or show[0] == 'false':
            j['organisation']['contact-info'] = {
                "person-name": "",
                "telephone": "",
                "email": "",
                "address": "",
            }
    failed = 0
    fp = 'csv2iati'
    orgref = j.get('organisation', {}).get('reporting-org', {}).get('ref')
    if orgref:
        orgref = orgref.replace('/', '_')
        fp = join(fp, orgref)
    else:
        fp = join(fp, 'noref')
    try:
        mkdir(fp)
    except FileExistsError:
        pass
    fp = join(fp, '{}.json'.format(counter))
    with open(fp, 'w') as f:
        json.dump(j, f, indent=4)
