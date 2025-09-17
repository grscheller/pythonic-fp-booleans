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

PyPI 2.0.0 - TBD
~~~~~~~~~~~~~~~~

- PyPI documentation link now goes to root, not releases
- decided to flatten directory structure

  - will help Sphinx docs be more homogeneous across repos

PyPI 1.1.3 - 2025-09-09
~~~~~~~~~~~~~~~~~~~~~~~

Updated docstrings for Sphinx documentation.

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
