#!/usr/bin/env python3

import copy

from . import _DEV
if _DEV: from . import _L

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
        * __iter__ - Just loops the base_form
        * __str__ - returns base_form wrapped as a string
    """
    def __init__(self, base_form={}, default_val=None, deepcopy=False):
        """
        base_form: the base form of the log.  This is essentially the
                   structure that will be your log.  Overwrite at creation
                   or use the default val you provide.
        default_val: Value to place for a parameter if defined via *args
        deepcopy: Whether or not to "deepcopy" things.
        """
        self._LP = {
              'base_form': {}
            , 'default_val': default_val
            , 'deepcopy': deepcopy
        }
        if isinstance(base_form,set) or isinstance(base_form,frozenset):
            for k in base_form:
                self._LP['base_form'][k] = self._LP['default_val']
        else:
            self.setBaseForm(**base_form) # Safer just in case.  Honors deepcopy

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
            if _DEV: _L.debug('deep-copied base_form to new_log')
            for a in args:
                new_log.update( {str(a): copy.deepcopy(self._LP['default_val'])} )
                if _DEV: _L.debug('copied {}: {}'.format(a, self._LP['default_val']))
            for k, v in kwargs.items():
                new_log[k] = copy.deepcopy(v)
                if _DEV: _L.debug('deep-copied {}: {}'.format(k, v))
        else:
            new_log = self._LP['base_form']
            if _DEV: _L.debug('copied base_form to new_log')
            for a in args:
                new_log.update( {a: self._LP['default_val']} )
                if _DEV: _L.debug('copied {}: {}'.format(a, self._LP['default_val']))
            for k, v in kwargs.items():
                new_log[k] = v
                if _DEV: _L.debug('copied {}: {}'.format(k, v))
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
        if _DEV: _L.debug('set default_value to {}'.format(default_val))

    def setDeepcopy(self, deepcopy=False):
        self._LP['deepcopy'] = deepcopy
        if _DEV: _L.debug('set deepcopy to {}'.format(str(deepcopy)))

    def setBaseForm(self, *args, **kwargs):
        self._LP['base_form'] = {}
        if _DEV: _L.debug('reset base_form')
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
                if _DEV: _L.debug('added: {}: {}'.format(a,self._LP['default_val']))
            for k, v in kwargs.items():
                self._LP['base_form'].update( {k: copy.deepcopy(v)} )
                if _DEV: _L.debug('added: {}: {}'.format(k, v))
        else:
            for a in args:
                self._LP['base_form'].update( {str(a): self._LP['default_val']} )
                if _DEV: _L.debug('added: {}: {}'.format(a,self._LP['default_val']))
            for k, v in kwargs.items():
                self._LP['base_form'].update( {k: v} )
                if _DEV: _L.debug('added: {}: {}'.format(k, v))

    def removeBase(self, *args, **kwargs):
        """
        Remove from the base_form

        args are expected to be strings
        kwargs are expected to be dict-like
        """
        for a in args:
            self._LP['base_form'].pop(str(a), None)
            if _DEV: _L.debug('removed: {}'.format(a))
        for k in kwargs:
            self._LP['base_form'].pop(k, None)
            if _DEV: _L.debug('removed: {}'.format(k))
