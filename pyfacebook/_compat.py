import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver.major == 2)

#: Python 3.x?
is_py3 = (_ver.major == 3)

if is_py2:
    str = unicode  # pragma: no cover # noqa

elif is_py3:
    str = str  # pragma: no cover
