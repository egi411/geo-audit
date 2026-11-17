#!/usr/bin/env python3
"""Prepare the custom-domain release only after public DNS points to GitHub Pages."""
from pathlib import Path
import json,subprocess,sys,urllib.request
root=Path(__file__).resolve().parents[1]
config=json.loads((root/'deploy/domain.json').read_text())
dns=json.load(urllib.request.urlopen('https://dns.google/resolve?name='+config['domain']+'&type=A',timeout=20))
actual={x['data'] for x in dns.get('Answer',[]) if x['type']==1}
expected={x['value'] for x in config['dnsRecords'] if x['type']=='A'}
if dns.get('Status')!=0 or actual!=expected:
 sys.exit('Domain not ready: configure the reviewed DNS records in deploy/domain.json first. Existing site remains unchanged.')
subprocess.run([sys.executable,str(root/'scripts/build_site.py'),'--base-url',config['targetBaseUrl']],check=True)
(root/'CNAME').write_text(config['domain']+'\n')
config['activated']=True
(root/'deploy/domain.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print('Custom-domain release prepared. Review and publish the changed files, then verify HTTPS.')
