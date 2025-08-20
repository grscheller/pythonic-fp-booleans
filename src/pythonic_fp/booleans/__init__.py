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

"""Boolean like class. Compatible with Python shortcut logic.

- module subtypable

  - class ``subtypable``

    - like Python's built-in ``bool``, class ``SBool`` is a subclass of ``int``
    - unlike ``bool``, class ``SBool`` can be further subclassed

- module ``subtypes``

  - module ``flavored`` 

    - class ``FBool`` is a subclass of ``SBool``

      - for when you need to deal with different "flavors" of the truth
      - each "flavor" corresponds to a hashable value

    - module ``true_false``

      - class ``TSBool`` is an ``SBool`` which is always truthy
      - class ``FSBool`` is ``SBool`` which is always falsy

"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
