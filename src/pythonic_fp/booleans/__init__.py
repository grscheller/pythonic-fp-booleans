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
also be non-shortcut logically composed with Python's bitwise operators.

Covariant class hierarchy
-------------------------

.. graphviz::

    digraph Booleans {
        bgcolor="#957fb8";
        node [style=filled, fillcolor="#181616", fontcolor="#dcd7ba"];
        edge [color="#181616", fontcolor="#dcd7ba"];
        int -> bool;
        int -> SBool;
        SBool -> "FBool(h1)";
        SBool -> "FBool(h2)";
        SBool -> "FBool(h3)";
        SBool -> TF_Bool;
        TF_Bool -> T_Bool;
        TF_Bool -> F_Bool;
    }
"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
