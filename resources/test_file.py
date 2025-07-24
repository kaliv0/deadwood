# unused imports
import resources.constants
from resources.util import fizz, buzz, jazz, Django

# unused global vars
used = 3
distractor = 2
not_used = used + distractor

# duplicate keys in dict literal + nesting
has_duplicates = {
    "third": 3,
    "fourth": 4,
    "inner": {
        "eleven": 11,
        "twelve": 12,
        "eleven": 11,
    },
    "fourth": 5,
    "third": 6,
}

def regular(param):
    result = 2 * param
    return result

# unused vars inside function
def has_unused(param):
    used = 3 * param
    not_used = 2 * param
    distractor = "distraction"
    return used

# unused parameter inside function
def has_unused_param(param, var, **kwargs):
    return [v * 2 for k, v in kwargs if k != var]

# unused kwarg inside function
def has_unused_kwarg(param, var, **kwargs):
    return var * 2

# unused class
class Foo:
    # duplicate attribute assignment in class
    def __init__(self):
        self.doodoo = 42
        self.snoopy = 33
        self.doodoo = 88

    # unused class method
    def _bar(self):
        pass

print(fizz())
