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
Module subtypes
===============

Top level modules.

Module flavored
---------------

Class FBool
~~~~~~~~~~~

For when you need to deal with different "flavors" of the truth.

Each "flavor" corresponds to a hashable value. Instances of ``FBool``
are invariant in their flavor. Best to think of the "flavor" as a
sort of label, not an index.

Module truthy_falsy
-------------------

Class TF_Bool
~~~~~~~~~~~~~

Class whose truthy and falsy instances are typeable.

Class T_Bool
~~~~~~~~~~~~

The truthy instance of a ``TF_Bool``.

Class F_Bool
~~~~~~~~~~~~

The falsy instance of a ``TF_Bool``.

"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
