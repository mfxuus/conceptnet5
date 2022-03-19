import os
from config import (
    LOCAL_DATA_DIR, VALID_RELATIONS
)


def build_gml_filename(all_languages, include_custom):
    output = 'conceptnet'
    if all_languages:
        output += '_full'
    else:
        output += '_en'
    if include_custom:
        output += '_custom'
    else:
        output += '_original'
    output += '.gml'
    OUT_PATH = os.path.join(LOCAL_DATA_DIR, output)
    return OUT_PATH


def rel_is_valid(rel_str):
    return rel_str in VALID_RELATIONS