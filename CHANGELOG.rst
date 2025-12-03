CHANGELOG
=========

PyPI pythonic-fp-booleans project.

Semantic Versioning
-------------------

Strict 3 digit semantic versioning adopted 2025-05-19.

- **MAJOR** version incremented for incompatible API changes
- **MINOR** version incremented for backward compatible added functionality
- **PATCH** version incremented for backward compatible bug fixes

See `Semantic Versioning 2.0.0 <https://semver.org>`_.

Releases and Important Milestones
---------------------------------

PyPI 2.1.0 - 2025-12-02
~~~~~~~~~~~~~~~~~~~~~~~

Now requires pythonic-fp-gadgets 4.0.1 to be installed.


PyPI 2.0.0 - 2025-09-27
~~~~~~~~~~~~~~~~~~~~~~~

Released to get the next consistent set of Pythonic FP out (v3.2.0) out.

- PyPI documentation link now goes to root, not releases
- decided to flatten directory structure

  - makes more sense from an end user perspective
  - will help Sphinx docs be more homogeneous across repos

Warning: API not fully locked down, major version number change may be needed.

TODO:

- bitwise operators not symmetric when used with ``SBool`` types and ``int`` or ``bool``

  - may need to define reversed bit-wise operators

- ``TS_Boolean`` has a code smell to it

  - may be just a hack to get get around sub-optimal type usage
  - Using ``TS_Bool`` as a variable type may be enough 

PyPI 1.1.2 - 2025-09-09
~~~~~~~~~~~~~~~~~~~~~~~

Fixed pyproject.toml dependency issues.

PyPI 1.1.1 - 2025-09-03
~~~~~~~~~~~~~~~~~~~~~~~

Only change was to give README.rst a final edit. Missed this on
the v1.1.0 release.


PyPI 1.1.0 - 2025-09-02
~~~~~~~~~~~~~~~~~~~~~~~

First PyPI release as pythonic-fp-booleans.

- module booleans.subtypable
- package booleans.subtypes

  - module booleans.subtypes.flavored
  - module booleans.subtypes.truthy_falsy

Needs

-  "pythonic-fp>=3.0.0" for gadgets
-  "pythonic-fp-sentinels>=2.1.0",

Created pythonic-fp-boolean repo - 2025-08-06
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- created grscheller/pythonic-fp-boolean GitHub repo
- moved pythonic_fp.singletons.sbool to pythonic_fp.booleans.sbool
