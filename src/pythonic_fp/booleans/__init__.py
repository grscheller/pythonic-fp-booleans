# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Subtypable Boolean like classes
===============================

While still compatible with Python shortcut logic, these classes can
be non-shortcut logically composed with Python's bitwise operators.
These classes are implemented with the Singleton Pattern.

Covariant class hierarchy
-------------------------

.. graphviz::

    digraph Booleans {
        int -> bool;
        int -> SBool;
        SBool -> FBool;
        SBool -> TF_Bool;
        TF_Bool -> T_Bool;
        TF_Bool -> F_Bool;
    }

Contravariant non-shortcut operators
------------------------------------

    +------------+--------+------------+-------------+
    | Boolean op | symbol | dunder     | Python name |
    +============+========+============+=============+
    | not        | ``~``  | __invert__ | bitwise not |
    +------------+--------+------------+-------------+
    | and        | ``&``  | __and__    | bitwise and |
    +------------+--------+------------+-------------+
    | or         | ``|``  | __or__     | bitwise or  |
    +------------+--------+------------+-------------+
    | xor        | ``^``  | __xor__    | bitwise xor |
    +------------+--------+------------+-------------+

    .. warning::

       These "bitwise" operators could raise ``TypeError`` exceptions
       when applied against an ``SBool`` and objects not descended
       from ``SBool``.

Classes
-------

Class SBool
~~~~~~~~~~~

- base of the hierarchy

  - like Python's built-in ``bool``, ``SBool`` is a subclass of ``int``
  - unlike ``bool``, class ``SBool`` can be further subclassed

Class FBool
~~~~~~~~~~~~~~~~~~~

- for when you need to deal with different "flavors" of the truth

  - each "flavor" corresponds to a hashable value
  - ``FBool`` instances are invariant in their flavor

Class TF_Bool
~~~~~~~~~~~~~

  - ``TF_Bool`` consists of just two disjoint subtypes, each a singleton

    - class ``T_Bool`` is the  always truthy ``TF_Bool`` subtype
    - class ``F_Bool`` is the  always falsy ``TF_Bool`` subtype

"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
