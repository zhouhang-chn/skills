import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import normalize, json_for_script, build, SpecError

class ContractTests(unittest.TestCase):
    def test_escape_script_breakout(self):
        src={'rows':[{'x':'</script><script>alert(1)</script>','s':'&\u2028'}]}
        result=json_for_script(src)
        self.assertNotIn('</script>',result)
        self.assertIn('\\u003c',result)
        self.assertEqual(json.loads(result),src)
    def test_invalid_widget(self):
        with self.assertRaises(SpecError):
            normalize({'title':'A','datasets':{'d':{'columns':['x'],'rows':[[1]]}},'widgets':[{'id':'v','type':'bar','dataset':'missing'}]},Path('.'))
    def test_build(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'out.html'; build(ROOT/'examples'/'nyc_taxi.json',out)
            html=out.read_text()
            self.assertIn('window.dash=dash',html)
            self.assertIn('id="dashboard-data"',html)
            self.assertNotIn('script src=',html)

if __name__=='__main__':unittest.main()
