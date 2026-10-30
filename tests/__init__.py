# Makes tests/ a package so test_sbool_pickle.py can use a relative
# import for its sbool_pickle_helper module. Without this, Python
# raises "attempted relative import with no known parent package".
#
# Side effect: test modules are named tests.test_* rather than test_*,
# which is the module path pickle records for classes defined here.
# The sub-process test in test_sbool_pickle.py depends on that name.
