from scholarly import scholarly
import json
from datetime import datetime
import os
from pathlib import Path


SCHOLAR_ID = os.environ.get('GOOGLE_SCHOLAR_ID', '4nWk-HYAAAAJ')
RESULTS_DIR = Path(__file__).resolve().parent / 'results'


author: dict = scholarly.search_author_id(SCHOLAR_ID)
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
name = author['name']
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']:v for v in author['publications']}
print(json.dumps(author, indent=2))
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
with open(RESULTS_DIR / 'gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author['citedby']}",
}
with open(RESULTS_DIR / 'gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)


