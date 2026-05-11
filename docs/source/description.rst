Description
===========

.. automodule:: pythonic_fp.booleans
    :no-members:
    :ignore-module-all:
    :no-index:

**Boolean type hierarchy**

.. graphviz::

    digraph Booleans {
        bgcolor="#957fb8";
        node [style=filled, fillcolor="#181616", fontcolor="#dcd7ba"];
        edge [color="#181616", fontcolor="#dcd7ba"];
        int -> bool;
        int -> SBool;
        SBool -> "FBool[H1]";
        SBool -> "FBool[H2]";
        SBool -> "FBool[H3]";
        SBool -> TF_Bool;
        TF_Bool -> T_Bool;
        TF_Bool -> F_Bool;
    }
