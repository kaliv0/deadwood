from resources.util import fizz, buzz, jazz

used = 3
distractor = 2
not_used = used + distractor

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

def has_unused(param):
    used = 3 * param
    not_used = 2 * param
    distractor = "distraction"
    return used

def has_unused_param(param, var, **kwargs):
    return [v * 2 for k, v in kwargs if k != var]

def has_unused_kwarg(param, var, **kwargs):
    return var * 2


class Foo:
    def bar(self):
        pass

print(fizz())