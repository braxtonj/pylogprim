# [Python Log Primitive Factory](https://github.com/braxtonj/pylogprim)

## Overview

***WIP***

Simple factory classes to create log object primitives with redaction, set default values and whatever else you'd like.

Useful when you are trying to standardize your structured logs across a Python project.  Save a common `base_form` for reuse, don't set a default `base_form` OR just extend the `LogPrimFactory` (the base) class to be what you want :)

i.e. with a base of `{'id': 42}`
```python
logPrimFactory.logObj(log = 'it')
```
outputs
```python
{ 'id': 42, 'log': 'it' }
```
Check out <a href="https://github.com/hynek/structlog" target="_blank">structlog</a> if you want more than just a log primitive factory.

##### Table of Contents
* [Overview](#overview)
* [Example Usage](#example-usage)
* [Dependencies: None](#dependencies-none)
* [API](#api)
  + [`LogPrimFactory`](#logprimfactory)
  + [`JSONLogPrimFactory`](#jsonlogprimfactory)
* [License](#license)
* [Contribution](#contribution)

## Example Usage
1. Copy the repo to your project using the folder pylogprim
2. Copy the following code above pylogprim folder and run
```python
# This shows JSON output to logger.
#    Use LogPrimFactory to get a dictionary instead.

import logging
from pylogprim.Factories import JSONLogPrimFactory as JLF

logger = logging.getLogger('pylogprim_test')

jlf = JLF(
      base_form = {'field1':100,'key2':{'well':'just','log':'it'}}
    , default_val = 42
    , deepcopy = True
)

logger.info(
    jlf.logObj(
          message = 'This is just a test'
        , why_not_add_more = 'it will get added to this created log only'
        , field1 = -13 # Overwrite default values for this log only
    )
)

jlf.setDeepcopy(False) # Set deepcopy to False

logger.debug(jlf.logObj(well = 'hello'))

# Do a bit of redaction using regex
jlf.setRedaction({
    'redaction_val_01':{'which':'val','replace_val':'***','re':'drop it'} # redact within the value
  , 'redaction_key_01':{'which':'key','replace_val':'---','re':'bad_key'} # redact the whole value, matching the key
  , 'redaction_val_cc':{'which':'val','replace_val':'################','re':'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$'} # basic cc redaction. https://stackoverflow.com/a/9315696
})

logger.info(
  jlf.logObj(
      key1='hey pal'
    , key2='i said drop it.'
    , bad_key='farewell'
    , transaction_details={
        'amount': 55.30
      , 'cc': '4485293941311976'
    }
  )
)
```
The prior code will output a stringified JSON log to `logger.info` of the form
```JSON
{
      "message": "This is just a test"
    , "why_not_add_more": "it will get added to this created log only"
    , "field1": -13
    , "key2": {
          "well": "just"
        , "log": "it"
    }
}
```
and another to `logger.debug` of the form
```JSON
{
      "well": "hello"
    , "field1": 100
    , "key2": {
          "well": "just"
        , "log": "it"
    }
}
```
and lastly a redacted log to `logger.info` of the form
```JSON
{
      "key1": "hey pal"
    , "key2": "i said ***."
    , "bad_key": "---"
    , "transaction_details": {
        "amount": 55.30
      , "cc": "################"
    }
    , "field1": 100
    , "key2": {
          "well": "just"
        , "log": "it"
    }
}
```

## Dependencies: None

## API

### [`LogPrimFactory`](./LogPrimFactory.py)

#### `LogPrimFactory( base_form={}, default_val=None, redaction={}, deepcopy=False )`

Creates the log factory with a log of form `base_form` with default values, `default_val` to be used when encountering `*args`, and whether or not to `deepcopy` it all (useful for odd cases)

* Parameters:
  * `base_form`: dict - Defines the form of the log to be generated (with given values by default)
  * `default_val`: val - Default when `*args` are used (which then define the "key")
  * `redaction`: dict - Patterns to redact.  See [`LogPrimFactory.setRedaction( redaction={} )`](#logprimfactorysetredaction-redaction-) for more details.
  * `deepcopy`: bool - Whether or not to use deepcopy all the time
* Returns:
  * `LogPrimFactory`: object - generate log objects with .logObj()

#### `LogPrimFactory.logObj( *args, **kwargs )`

Creates the log object.  `**kwargs` are here to define additionals.  IE `logObj( 'key0', key1=42, key2='blah' )`

* Parameters:
  * `*args`: strings, parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names used in in the log with `default_value` assigned.
  * `**kwargs`: keyword arguments.  Each define another aspect of your generated log.  Any key that is in `base_form` will be superceded by the value defined here.
* Returns
  * `logObject`: dict - a new log object with all your things

#### `LogPrimFactory.setDefaultVal( defaul_val=None )`

Set the default value to be used when `*args` is encountered

* Parameters:
  * `default_val`: you choose
* Returns
  * nada

#### `LogPrimFactory.setDeepcopy( deppcopy=False )`

Switch deepcopy on or off.  Sometimes dictionaries and references can get weird in python.  This let's you avoid that if you run in to it.  Generally you can gow with the default (`False`).

* Parameters:
  * `deepcopy`: bool - `True`: do the deepcopy
* Returns
  * nada

#### `LogPrimFactory.setBaseForm( *args, **kwargs )`

Set the base form for this log factory.

* Parameters:
  * `*args`: strings - parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names used in `base_form` with `default_value` assigned.
    * ex - `.setBaseForm('key1','key2')` ~~> `base_form = {'key1': DEFAULT_VAL, 'key2': DEFAULT_VAL}`
  * `**kwargs`: keyword arguments - key-values to be added to the `base_form`
    * ex - `.setBaseForm(key1=42, key2=10)` ~~> `base_form = {'key1':42, 'key2':10}`
* Returns
  * nada

#### `LogPrimFactory.addBase( *args, **kwargs )`

Add to the base form for this log factory.

* Parameters:
  * `*args`: strings - parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names used in `base_form` with `default_value` assigned.
    * ex - `.addBase('key1','key2')` ~~> `base_form.update({'key1': DEFAULT_VAL, 'key2': DEFAULT_VAL})`
  * `**kwargs`: keyword arguments - key-values to be added to the `base_form`
    * ex - `.addBase(key1=42, key2=10)` ~~> `base_form.update({'key1':42, 'key2':10})`
* Returns
  * nada

#### `LogPrimFactory.removeBase( *args, **kwargs )`

Remove from the base form for this log factory.

* Parameters:
  * `*args`: strings - parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names removed from `base_form`.
    * ex - `.removeBase('key1','key2')` ~~> `base_form.pop('key1'); base_form.pop('key2')`
  * `**kwargs`: keyword arguments - key-values to be removed from the `base_form` (VAL is really unnecessary and isn't used in the logic)
    * ex - `.removeBase(key1=42, key2=10)` ~~> `base_form.pop('key1'); base_form.pop('key2')`
* Returns
  * nada

#### `LogPrimFactory.setRedaction( redaction={} )`

Sets the redaction patterns to use to `redaction`.  `'which': 'key'` redacts entire value when a key is matched.   `'which': 'val'` replaces matching patterns within vals with `replace_val`, leaving the rest of the val intact.

* Paremeters:
  * `redaction`: dictionary - all the patterns you want.  Use the following form
```python
{
  'some_id': {
    'which': 'key' # or 'val'
    , 'replace_val': WHAT_TO_REPLACE_WITH
    , 're': REGEX_PATTERN_TO_USE
  }
  , ...
}
```

#### `LogPrimFactory.redact( logObj )`

Automatically called within `.logObj()` if redaction patterns have been defined.

Use predefined redaction patterns to redact data from the log object.

* Parameters:
  * `logObj`: logObj - the log object to be redacted. 
* Returns
  * `redactedLog`: logObj - 

### [`JSONLogPrimFactory`](./JSONLogPrimFactory.py)

Inherits from `LogPrimFactory` but returns stringified JSON for `logObj`

## License
pylogprim is a MIT licensed project.  See [license](./LICENSE)

## Contribution
Contributions are welcome.  See the [contribution doc](./CONTRIBUTING.md)
