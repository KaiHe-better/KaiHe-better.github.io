import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import update_publications as u
import sync_publications as legacy

class UpdateTests(unittest.TestCase):
    def record(self):
        return {'title': ['Example paper'], 'DOI': '10.1234/paper', 'type': 'journal-article', 'published': {'date-parts': [[2026, 8, 20]]}, 'container-title': ['Real Journal'], 'author': [{'given': 'Kai', 'family': 'He', 'ORCID': 'https://orcid.org/' + u.ORCID}]}
    def page(self, body, news='- *2025.12*: An existing announcement.'):
        return 'Original bio\n' + legacy.NEWS_START + '\n' + news + '\n' + legacy.NEWS_END + '\n' + u.START + '\n' + body + '\n' + u.END + '\nHonors unchanged\n'
    def test_promotion_news_limit_order_and_idempotence(self):
        text = self.page('## 2026\n\n- Someone. Other [J]. Journal, 2026.\n\n## Preprints\n\n- K. He. Example paper [Preprint]. arXiv, 2025.', '\n'.join(f'- *2026.0{i}*: News {i}.' for i in range(1,8)))
        entry = u.citation(self.record(), 'Example paper')
        result, state, changes, conflicts = u.apply_candidates(text, [entry], {})
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['action'], 'promoted')
        self.assertNotIn('Example paper [Preprint]', result)
        self.assertIn('Other [J]', result)
        news = result.split(legacy.NEWS_START)[1].split(legacy.NEWS_END)[0]
        self.assertEqual(sum(line.startswith('- ') for line in news.splitlines()),5)
        self.assertLess(news.index('2026.08'),news.index('2026.07'))
        self.assertNotIn('News 1.',news)
        self.assertTrue(result.endswith('Honors unchanged\n'))
        again = u.apply_candidates(result, [entry], state)
        self.assertEqual(again[0], result)
        self.assertEqual(again[2], [])
    def test_existing_tool_cannot_revert_promotion(self):
        old = '- K. He. Example paper [Preprint]. arXiv, 2025.'
        text = self.page('## Preprints\n\n'+old)
        overrides = {'entries':[{'title':'Example paper','markdown':old,'year':2025,'section':'preprint','sort_date':'2025-01'}]}
        result, state, _, _ = u.apply_candidates(text,[u.citation(self.record(),'Example paper')],overrides)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)
            (path/'about.md').write_text(result)
            (path/'overrides.json').write_text(json.dumps(state))
            subprocess.run([sys.executable,str(ROOT/'scripts/sync_publications.py'),'--about',str(path/'about.md'),'--overrides',str(path/'overrides.json'),'--scholar-json',str(path/'absent.json'),'--write'],check=True)
            self.assertEqual((path/'about.md').read_text(),result)
    def test_rejects_wrong_author_title_or_missing_venue(self):
        record = self.record(); record['author'][0]['ORCID'] = 'https://orcid.org/0000-0000-0000-0000'
        with self.assertRaises(ValueError): u.citation(record, 'Example paper')
        with self.assertRaises(ValueError): u.citation(self.record(), 'Different paper')
        record=self.record();record['container-title']=[]
        with self.assertRaises(ValueError):u.citation(record,'Example paper')
    def test_suppression_and_duplicate_sources(self):
        text=self.page('## 2026\n')
        entry=u.citation(self.record(),'Example paper')
        result,_,changes,_=u.apply_candidates(text,[entry],{'suppressed_titles':['Example paper']})
        self.assertNotIn('Example paper',result);self.assertEqual(changes,[])
        result,_,changes,_=u.apply_candidates(text,[entry,entry],{})
        self.assertEqual(len(changes),1)
    def test_preserves_other_tools_edits_between_fetch_and_apply(self):
        old='- K. He. Example paper [Preprint]. arXiv, 2025.'
        text=self.page('## Preprints\n\n'+old)
        expected=u.baseline(text,{})
        other=text.replace('Original bio','Edited biography').replace('Example paper [Preprint]','Example paper [J]')
        result,_,changes,conflicts=u.apply_candidates(other,[u.citation(self.record(),'Example paper')],{},expected)
        self.assertIn('Edited biography',result)
        self.assertEqual(changes,[]);self.assertEqual(conflicts,['Example paper'])
        self.assertIn('Example paper [J]',result)
    def test_preserves_external_news(self):
        text=self.page('## 2026\n','- *2026.09*: Another tool added an award.')
        result,_,_,_=u.apply_candidates(text,[u.citation(self.record(),'Example paper')],{})
        self.assertIn('Another tool added an award.',result)
    def test_preprint_source_cannot_downgrade_formal(self):
        text=self.page('## 2026\n\n- K. He. Example paper [J]. Curated Journal, 2026.')
        record=self.record();record['type']='posted-content'
        result,_,changes,_=u.apply_candidates(text,[u.citation(record,'Example paper')],{})
        self.assertIn('Curated Journal',result);self.assertEqual(changes,[])
    def test_new_preprint_stays_in_preprints(self):
        text=self.page('## 2026\n')
        record=self.record();record['type']='posted-content'
        result,_,_,_=u.apply_candidates(text,[u.citation(record,'Example paper')],{})
        self.assertIn('Example paper [Preprint]',result.split('## Preprints')[1])
    def test_alias_survives_sort_date_enrichment(self):
        line='- K. He. Examples paper [J]. Journal, 2026.'
        text=self.page('## 2026\n\n'+line)
        state={'entries':[{'title':'Example paper','markdown':line,'section':'publication','year':2026}]}
        entry=u.citation(self.record(),'Example paper')
        first=u.apply_candidates(text,[entry],state)
        second=u.apply_candidates(first[0],[entry],first[1])
        self.assertEqual(first[0],second[0]);self.assertEqual(second[2],[])

    def test_news_crosses_year_boundary(self):
        e=legacy.Entry(title='New',markdown='',section='publication',year=2027,sort_date='2027-01',news='- *2027.01*: New year paper.')
        news=legacy.render_news({'x':e},existing='- *2026.12*: Last year news.')
        self.assertIn('Last year news.',news)
        self.assertLess(news.index('2027.01'),news.index('2026.12'))

if __name__ == '__main__': unittest.main()
