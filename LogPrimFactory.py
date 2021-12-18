#!/usr/bin/env python3

import copy
import re

from .SamplingClasses import Sampling
from . import _DEV
if _DEV:
    from .util.logging import _L
    import json

class LogPrimFactory:
    """
    Base Log Primitive Factory.

    Goals: Easy generation of log structures with defined and default values in a dictionary format

    Workflow:
        1. Create Log Factory (LF) object using base_form to define common values for the algorithm (or whatever)
                Can update via convenience methods setBaseForm (and defineStructure)
        2. Call LF.logObj( some_key: 42, MORE_STUFF={'log':'it'} )
                LF.serialize works same way.  Convenience rename
        3. Send the log object to your log stream.  Default values defined in the factory will be included
            for all the logs.  Defined values will overwrite the default values

    Log Format: Dictionary

    Functions
        * logObj - create log object (the factory floor)
        * setDefaultVal
        * setDeepcopy
        * setBaseForm - set the default values for the log object
        * addBase - add things to the base_form
        * removeBase - remove from the base_form
        * sendCheck - check if the log should be sent via a sampling function
        * __iter__ - Just loops the base_form
        * __str__ - returns base_form wrapped as a string
    """
    def __init__(self, base_form={}, default_val=None, deepcopy=False, redaction={}, sampling_instance=Sampling()):
        """
        base_form: the base form of the log.  This is essentially the
                   structure that will be your log.  Overwrite at creation
                   or use the default val you provide.
        default_val: Value to place for a parameter if defined via *args
        deepcopy: Whether or not to "deepcopy" things.
        redaction: Dictionary of redaction patterns to employ of the form
                                { 'key': { # key is arbitrary but must be unique
                                        'which': 'key' OR 'val'
                                      , 'replace_val':'value to use as the replacement'
                                      , 're':'regex pattern'
                                  }
                                  , ...
                                }
        sampling_instance: # Sampling class instance.  Defaults to send everything via base class
        """
        self._LP = {
              'base_form': {}
            , 'default_val': default_val
            , 'deepcopy': deepcopy
            , 'redaction': {}
        }
        if isinstance(base_form,set) or isinstance(base_form,frozenset):
            for k in base_form:
                self._LP['base_form'][k] = self._LP['default_val']
        else:
            self.setBaseForm(**base_form) # Safer just in case.  Honors deepcopy

        self.setRedaction( redaction )
        self.sampling_instance = sampling_instance

    ''' CREATION '''
    def logObj(self, *args, **kwargs):
        """
        Creation of the Log Primitive.  This is the actual "factory"

        Set special values by using keyword assignment.  IE

        IN_==>
            _lf.logObj(keyword1={'log':'it'},message="Just some message to display")
        <==_OUT
            {
                  'keyword1': {
                      'log': 'it'
                  }
                , 'message': 'Just some message to display'
                , ...default values for base_form where "log" and "message" are overwritten by logObj if present
            }
        """
        new_log = {}
        if self._LP['deepcopy']:
            new_log = copy.deepcopy(self._LP['base_form'])
            if _DEV: _L.debug('{"message":"deep-copied base_form to new_log"}')
            for a in args:
                new_log.update( {str(a): copy.deepcopy(self._LP['default_val'])} )
                if _DEV: _L.debug('{{"deep-copied": {{"{ARG}": "{VAL}"}}}}'.format(ARG=a, VAL=self._LP['default_val']))
            for k, v in kwargs.items():
                new_log[k] = copy.deepcopy(v)
                if _DEV: _L.debug('{{"deep-copied": {{"{KEY}": "{VAL}"}}}}'.format(KEY=k, VAL=v))
        else:
            new_log = self._LP['base_form']
            if _DEV: _L.debug('{"message":"copied base_form to new_log"}')
            for a in args:
                new_log.update( {a: self._LP['default_val']} )
                if _DEV: _L.debug('{{"copied": {{"{ARG}": "{VAL}"}}}}'.format(ARG=a, VAL=self._LP['default_val']))
            for k, v in kwargs.items():
                new_log[k] = v
                if _DEV: _L.debug('{{"copied": {{"{KEY}": "{VAL}"}}}}'.format(KEY=k, VAL=v))

        if self._LP['redaction']:
            new_log = self.redact(new_log)

        return new_log


    ''' Built Ins '''
    def __iter__(self):
        """
        Change iterator to return dictionary base_form only
        """
        if self._LP['deepcopy']:
            for k in self._LP['base_form']: yield {copy.deepcopy(k): copy.deepcopy(self._LP['base_form'][k])}
        else:
            for k in self._LP['base_form']: yield {k: self._LP['base_form'][k]}

    def __str__(self):
        return str(self.logObj())


    ''' MODIFIERS '''
    def setDefaultVal(self, default_val=None):
        """
        Value to be used by all attributes defined via *args route (ie, with just a name str)
        """
        self._LP['default_val'] = default_val
        if _DEV: _L.debug('{{"message":"set default_val", "default_val":"{}"}}'.format(default_val))

    def setDeepcopy(self, deepcopy=False):
        self._LP['deepcopy'] = deepcopy
        if _DEV: _L.debug('{{"message":"set deepcopy","deepcopy": "{}"}}'.format(str(deepcopy)))

    def setBaseForm(self, *args, **kwargs):
        self._LP['base_form'] = {}
        if _DEV: _L.debug('{"message":"reset base_form"}')
        self.addBase(*args, **kwargs) # Honors deepcopy

    def addBase(self, *args, **kwargs):
        """
        Add to the base_form

        args are expected to be strings.
        kwargs are expected to be dict-like
        """
        if self._LP['deepcopy']:
            for a in args:
                self._LP['base_form'].update( {str(a): copy.deepcopy(self._LP['default_val'])} )
                if _DEV: _L.debug('{{"added_base_form": {{"{}": "{}"}}}}'.format(a,self._LP['default_val']))
            for k, v in kwargs.items():
                self._LP['base_form'].update( {k: copy.deepcopy(v)} )
                if _DEV: _L.debug('{{"added_base_form": {{"{}": "{}"}}}}'.format(k, v))
        else:
            for a in args:
                self._LP['base_form'].update( {str(a): self._LP['default_val']} )
                if _DEV: _L.debug('{{"added_base_form": {{"{}": "{}"}}}}'.format(a,self._LP['default_val']))
            for k, v in kwargs.items():
                self._LP['base_form'].update( {k: v} )
                if _DEV: _L.debug('{{"added_base_form": {{"{}": "{}"}}}}'.format(k, v))

    def removeBase(self, *args, **kwargs):
        """
        Remove from the base_form

        args are expected to be strings
        kwargs are expected to be dict-like
        """
        for a in args:
            self._LP['base_form'].pop(str(a), None)
            if _DEV: _L.debug('{{"removed_base_form": "{}"}}'.format(a))
        for k in kwargs:
            self._LP['base_form'].pop(k, None)
            if _DEV: _L.debug('{{"removed_base_form": "{}"}}'.format(k))

    def setRedaction(self, redaction={}):
        """
        Sets the redaction patterns to use
        """
        self._LP['redaction'] = {}

        self.addRedaction(redaction)

    def addRedaction(self, redaction={}):
        """
        Adds redaction patterns to use.

        Key "which" overwrites val when a key is matched.
        Val "which" replaces matched patterns in values with the v

        Assumes redaciton is of the form
            { 'key': { # key is arbitrary but must be unique
                      'which': 'key' OR 'val'
                    , 'replace_val': 'value to use as the replacement'
                    , 're': 'regex pattern'
                }
                , ...
            }
        """
        for k, v in redaction.items():
            new_redact = {
                k: {
                      'which': v['which']
                    , 'replace_val': v['replace_val']
                    , 're': v['re']
                }
            }
            self._LP['redaction'].update(new_redact)

            if _DEV: _L.debug('''{{"added_redaction":{NEW_REDACT}}}'''.format(NEW_REDACT=json.dumps(new_redact)))

    def redactMatchingKey(self, logObj, regex, replace_val):
        """
        Only handles dictionary objects
        """
        redacted_log = {}

        for k, v in logObj.items():
            if re.search(regex,k): # Found a match
                if _DEV: _L.debug('{{"redaction_match_key":"{}"}}'.format(k))
                new_v = replace_val
            elif type(v) is dict:
                new_v = self.redactMatchingKey(logObj=v, regex=regex, replace_val=replace_val)
            else:
                new_v = v if not self._LP['deepcopy'] else copy.deepcopy(v)
            redacted_log.update({k:new_v})
        return redacted_log

    def redactMatchingVal(self, logObj, regex, replace_val):
        """
        Only handles dictionary objects
        """
        redacted_log = {}

        for k, v in logObj.items():
            if type(v) is dict:
                new_v = self.redactMatchingVal(logObj=v, regex=regex, replace_val=replace_val)
            else:
                try:
                    if re.search(regex,str(v)):
                        new_v = re.sub(regex,replace_val,str(v))
                        if _DEV and new_v != v: _L.debug('{{"redaction_match_val":"{}"}}'.format(k))
                    else:
                        new_v = v if not self._LP['deepcopy'] else copy.deepcopy(v)
                except:
                    new_v = v if not self._LP['deepcopy'] else copy.deepcopy(v)
            redacted_log.update({k:new_v})

        return redacted_log

    def redact(self, logObj):
        """
        Takes in a log object and returns a redacted version using patterns defined

        This works by matching ANY (even sub keys) using the defined regex pattern.  If a match is found, redact it
        """
        redacted_log = logObj if not self._LP['deepcopy'] else copy.deepcopy(logObj)

        for k, v in self._LP['redaction'].items():
            if v['which'] == 'key':
                redacted_log = self.redactMatchingKey(logObj=redacted_log, regex=v['re'], replace_val=v['replace_val'])
            elif v['which'] == 'val':
                redacted_log = self.redactMatchingVal(logObj=redacted_log, regex=v['re'], replace_val=v['replace_val'])
            else:
                if _DEV: _L.warning('{"message":"bad redaction type passed","redaction_type_given":"{}"}}'.format(v['which']))

        return redacted_log


    ''' SAMPLING '''
    def sendCheck(self):
        """
        Decide if a log should be sent using a random selection over some distribution defined in the sampling class

        Basically, if this returns true the log should be sent.  If not, forget about it.
        """
        return self.sampling_instance.sendCheck()
