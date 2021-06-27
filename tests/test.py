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