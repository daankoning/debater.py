debater.py
==========
.. image:: https://badge.fury.io/py/debaterpy.svg?
    :target: https://pypi.org/project/debaterpy/

.. image:: https://badgen.net/github/license/daankoning/debater.py?
    :target: https://github.com/daankoning/debater.py/blob/main/LICENSE


A simple library to keep track of your progress and history in competitive debating.

The library is largely meant to interface with `DebaterJSON <https://github.com/daankoning/DebaterJSON>`_ and as such
provides a significant number of functions and classes to analyse and manipulate these records.

Installation
************
Because the package is available on PyPi simply run the following command to install it: ::

    pip install debaterpy

Usage
*****
Instantiating objects is really simple, assuming you have a valid DebaterJSON string loaded in ``data`` it only takes two
lines of code to generate an object from them.

>>> import debaterpy
>>> record = debaterpy.Record.from_json(data)

In fact, this method should cover the vast majority of use cases for generating records. In case more control over
record creation (e.g. for generating test data or fetching a record from an external source) most classes are standard
python dataclasses and as such offer fine programmatic control.

Having a ``Record`` object in memory it is incredibly simple to do even relatively complex manipulations. For example,
in order to get a speaker's average speaks in rounds where their team won, do:

>>> winning_rounds = debaterpy.get_all_rounds(record, function=lambda x, y: y.result == 3)
>>> winning_speaks = [round.speeches[0].speak for round in winning_rounds]
>>> sum(winning_speaks)/len(winning_speaks)
78.88888888888889

Documentation
*************
The documentation lives in the ``docs`` directory as well as on `ReadTheDocs <https://debaterpy.readthedocs.io/en/latest/>`_.