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

"""**module booleans**

Boolean like classes. Compatible with Python shortcut logic.

- module subtypable_boolean

  - like Python's built in bool, class SBool is a subclass of int
  - unlike bool, this class can be further subclassed

- module flavored_booleans

  - When you need different flavors of the truth

- module true_and_false_subtyped_booleans

  - contains two final subclasses of SBool

    - TSBool instances are always truthy
    - FSBool instances are always falsy


"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
