# Python Log Primitive Factory

## Overview

WIP

Simple way to create log object primitives with set default values.

Useful when you are trying to standardize your structured logs across a Python project.  Save a common base_form for reuse, don't set a default base_form OR just extend the LogPrimFactory (the base) class to be what you want :)

## Dependencies:
* None

## Dev Dependencies (set environment variable DEV to just exist):
* logdna (if environment variable LOGDNA_API_KEY is set)

## Example Usage
1. Copy the repo to your project using the folder pylogprim
2. Copy the following code above pylogprim folder and run
```python
# This shows JSON output to logger.
#    Use LogPrimFactory to get a dictionary instead.

import logging
from pylogprim.Factories import JSONLogPrimFactory as JLF

logger = logging.getLogger('pylogprim_test')

_jlf = JLF(
      base_form = {'field1':100,'key2':{'subkey1':'just','log':'it'}}
    , default_val = 42
    , deepcopy = True
)

logger.info(
    _jlf.logObj(
          message = 'This is just a test'
        , why_not_add_more = 'it will get added to this created log only'
        , field1 = -13 # Overwrite defaults with ease
    )
)

logger.debug(_jlf.logObj(well = 'hello'))
```
The prior code will output a log to logger.info of the form (JSON)
```JSON
{
      "message": "This is just a test"
    , "why_not_add_more": "it will get added to this created log only"
    , "field1": -13
    , "key2": {
          "subkey1": "just"
        , "log": "it"
    }
}
```
and a log to logger.debug of the form (JSON)
```JSON
{
      "well": "hello"
    , "field1": 100
    , "key2": {
          "subkey1": "just"
        , "log": "it"
    }
}
```

## API

### LogPrimFactory

#### LogPrimFactory( base_form={}, default_val=None, deepcopy=False )

Creates the log factory with a log of form base_form with default values (for *args) and whether or not to deepcopy it all (useful for odd cases)

* Parameters:
  * base_form: dict - Defines the form of the log to be generated (with values by default)
  * default_val: val - Default when *args are used (which then define the "key")
  * deepcopy: bool - Whether or not to use deepcopy all the time
* Returns:
  * logFactory: object - generate log objects with .logObj()

#### LogPrimFactory.logObj( *args, \*\*kwargs )

Creates the log object.  **kwargs are here to define additionals.  IE `logObj( 'key0', key1=42, key2='blah' )`

* Parameters:
  * *args: strings, parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names used in in the log with default_value assigned.
  * **kwargs: keyword arguments.  Each define another aspect of your generated log.  Any key that is in base_form will be superceded by the value defined here.
* Returns
  * logObject: dict - a new log object with all your things

#### LogPrimFactory.setDefaultVal( defaul_val=None )

Set the default value to be used when *args is encountered

* Parameters:
  * default_val: you choose
* Returns
  * nada

#### LogPrimFactory.setDeepcopy( deppcopy=False )

Switch deepcopy on or off.  Sometimes dictionaries and references can get weird in python.  This let's you avoid that if you run in to it.  Generally you can leave it at.

* Parameters:
  * deepcopy: bool - True: do the deepcopy
* Returns
  * nada

#### LogPrimFactory.setBaseForm( *args, \*\*kwargs )

Set the base form for this log factory.  Can sometimes be useful.

* Parameters:
  * *args: strings, parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names used in base_form with default_value assigned.
    * ex - `.setBaseForm('key1','key2')` --> `base_form.update({'key1': DEFAULT_VAL, 'key2': DEFAULT_VAL})`
  * \*\*kwargs: keyword arguments - key-values to be added to the base_form
    * ex - `.setBaseForm(key1=42, key2=10)` --> `base_form.update({'key1':42, 'key2':10})`
* Returns
  * nada

#### LogPrimFactory.addBase( *args, \*\*kwargs )

Add to the base form for this log factory.

* Parameters:
  * *args: strings, parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names used in base_form with default_value assigned.
    * ex - `.addBase('key1','key2')` --> `base_form.update({'key1': DEFAULT_VAL, 'key2': DEFAULT_VAL})`
  * \*\*kwargs: keyword arguments - key-values to be added to the base_form
    * ex - `.addBase(key1=42, key2=10)` --> `base_form.update({'key1':42, 'key2':10})`
* Returns
  * nada

#### LogPrimFactory.removeBase( *args, \*\*kwargs )

Remove from the base form for this log factory.  Can sometimes be useful.

* Parameters:
  * *args: strings, parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names removed from base_form.
    * ex - `.removeBase('key1','key2')` --> `base_form.pop('key1'); base_form.pop('key2')`
  * \*\*kwargs: keyword arguments - key-values to be removed from the base_form (VAL is really unnecessary and isn't used in the logic)
    * ex - `.removeBase(key1=42, key2=10)` --> `base_form.pop('key1'); base_form.pop('key2')`
* Returns
  * nada

### JSONLogPrimFactory

Inherits from LogPrimFactory but returns stringified JSON for logObj

## License
These Factories are MIT Licensed.  See [license](./LICENSE)

## Contribution
Contributions are welcome.  See the [contribution doc](./CONTRIBUTING.md)
