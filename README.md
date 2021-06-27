# [Python Log Primitive Factory](https://github.com/braxtonj/pylogprim)

##### Table of Contents
* [Overview](#overview)
* [Dependencies: None](#dependencies--none)
* [Example Usage](#example-usage)
* [API](#api)
  + [`LogPrimFactory`](#--logprimfactory----logprimfactorypy-)
  + [`JSONLogPrimFactory`](#--jsonlogprimfactory----jsonlogprimfactorypy-)
* [License](#license)
* [Contribution](#contribution)


## Overview

WIP

Simple way to create log object primitives with set default values using a factory.

Useful when you are trying to standardize your structured logs across a Python project.  Save a common `base_form` for reuse, don't set a default `base_form` OR just extend the `LogPrimFactory` (the base) class to be what you want :)

## Dependencies: None

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
      base_form = {'field1':100,'key2':{'well':'just','log':'it'}}
    , default_val = 42
    , deepcopy = True
)

logger.info(
    _jlf.logObj(
          message = 'This is just a test'
        , why_not_add_more = 'it will get added to this created log only'
        , field1 = -13 # Overwrite default values for this log only
    )
)

_jlf.setDeepcopy(False) # Set deepcopy to False

logger.debug(_jlf.logObj(well = 'hello'))
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

## API

### [`LogPrimFactory`](./LogPrimFactory.py)

#### `LogPrimFactory( base_form={}, default_val=None, deepcopy=False )`

Creates the log factory with a log of form `base_form` with default values, `default_val` to be used when encountering `*args`, and whether or not to `deepcopy` it all (useful for odd cases)

* Parameters:
  * `base_form`: dict - Defines the form of the log to be generated (with given values by default)
  * `default_val`: val - Default when `*args` are used (which then define the "key")
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
  * `*args`: strings, parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names used in `base_form` with `default_value` assigned.
    * ex - `.setBaseForm('key1','key2')` --> `base_form.update({'key1': DEFAULT_VAL, 'key2': DEFAULT_VAL})`
  * `**kwargs`: keyword arguments - key-values to be added to the `base_form`
    * ex - `.setBaseForm(key1=42, key2=10)` --> `base_form.update({'key1':42, 'key2':10})`
* Returns
  * nada

#### `LogPrimFactory.addBase( *args, **kwargs )`

Add to the base form for this log factory.

* Parameters:
  * `*args`: strings, parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names used in `base_form` with `default_value` assigned.
    * ex - `.addBase('key1','key2')` --> `base_form.update({'key1': DEFAULT_VAL, 'key2': DEFAULT_VAL})`
  * `**kwargs`: keyword arguments - key-values to be added to the `base_form`
    * ex - `.addBase(key1=42, key2=10)` --> `base_form.update({'key1':42, 'key2':10})`
* Returns
  * nada

#### `LogPrimFactory.removeBase( *args, **kwargs )`

Remove from the base form for this log factory.

* Parameters:
  * `*args`: strings, parameters not given in the KEY=VALUE style should be given as strings.  These will be the key names removed from `base_form`.
    * ex - `.removeBase('key1','key2')` --> `base_form.pop('key1'); base_form.pop('key2')`
  * `**kwargs`: keyword arguments - key-values to be removed from the `base_form` (VAL is really unnecessary and isn't used in the logic)
    * ex - `.removeBase(key1=42, key2=10)` --> `base_form.pop('key1'); base_form.pop('key2')`
* Returns
  * nada

### [`JSONLogPrimFactory`](./JSONLogPrimFactory.py)

Inherits from `LogPrimFactory` but returns stringified JSON for `logObj`

## License
pylogprim is a MIT licensed project.  See [license](./LICENSE)

## Contribution
Contributions are welcome.  See the [contribution doc](./CONTRIBUTING.md)
