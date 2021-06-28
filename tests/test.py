import unittest
import json
import sys
import os

sys.path.insert(
      1
    , os.path.split(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])[0]
)

from pylogprim.Factories import LogPrimFactory, JSONLogPrimFactory

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


class LogPrimFactoryTest(unittest.TestCase):
    def testSetDefault(self):
        lf = LogPrimFactory()
        lf.setDefaultVal('test')
        self.assertEqual('test',lf._LP['default_val'])

    def testSetBaseFormInit(self):
        test_form = {'tst':'me','wait':{'for':'it'}}
        lf = LogPrimFactory(base_form=test_form)
        for k, v in test_form.items():
            self.assertTrue(k in lf._LP['base_form'])
            self.assertEqual(v, lf._LP['base_form'][k])

    def testSetDeepcopy(self):
        lf = LogPrimFactory()
        lf.setDeepcopy(True)
        self.assertEqual(True,lf._LP['deepcopy'])

    def testCreation(self):
        tmp_base_form = {'just':'a','bit':{'of':'testing'}}
        tmp_ephemeral_log = {'just':'change','twelve':42}
        lf = LogPrimFactory(base_form=tmp_base_form)
        logObj = lf.logObj('key0',**tmp_ephemeral_log)
        self.assertEqual(logObj,{'key0':lf._LP['default_val'],'just':'change','twelve':42,'bit':{'of':'testing'}})

    def testAddRedaction(self):
        prior_redaction = {
            "tst_redact_0": {
                  "which": "key"
                , "replace_val": "//"
                , "re": "/"
            }
        }
        lf = LogPrimFactory(base_form={'test':'redaction'}, redaction=prior_redaction)
        new_redaction = {
            "tst_redact_1": {
                  "which": "val"
                , "replace_val": "*****"
                , "re": "/"
            }
        }
        lf.addRedaction(new_redaction)
        self.assertEqual(lf._LP['redaction'],{**prior_redaction,**new_redaction})

    def testRedaction(self):
        replace_val = "-----"
        redactions = {
              "tst_redact_key": {
                  "which": "key"
                , "replace_val": replace_val
                , "re": "do_redact"
            }
            , "tst_redact_val": {
                  "which": "val"
                , "replace_val": replace_val
                , "re": "^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$"
            }
        }
        base_form = {'test':'redaction'}
        lf = LogPrimFactory(base_form=base_form, redaction=redactions)
        orig_log_vals = {
              "dont_redact": "something here"
            , "do_redact": "blah"
            , "more": {
                  "burried_do_redact": "but you won't"
            }
            , "another_test": "5488089413725543"
        }
        redacted_to = {
              "dont_redact": "something here"
            , "do_redact": replace_val
            , "more": {
                  "burried_do_redact": replace_val # o but you did
            }
            , "another_test": replace_val

        }
        logObj = lf.logObj(**orig_log_vals)
        self.assertEqual(logObj,{**redacted_to,**base_form})


class JSONLogPrimFactoryTest(unittest.TestCase):
    def testCreation(self):
        tmp_base_form = {'just':'a','bit':{'of':'testing'}}
        tmp_ephemeral_log = {'just':'change','twelve':42}
        lf = JSONLogPrimFactory(base_form=tmp_base_form)
        logObj = lf.logObj(**tmp_ephemeral_log)
        logObjDict = json.loads(logObj)
        logObjTst = json.dumps({'just':'change','twelve':42,'bit':{'of':'testing'}})
        logObjTstDict = json.loads(logObjTst)
        self.assertEqual(ordered(logObjDict),ordered(logObjTstDict))
        self.assertTrue(isinstance(logObj,str))


if __name__ == '__main__':
    unittest.main()