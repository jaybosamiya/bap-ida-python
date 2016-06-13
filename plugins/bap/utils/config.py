"""Module for reading from and writing to the bap.cfg config file."""

import os

cfg_dir = idaapi.idadir('cfg')
cfg_path = os.path.join(cfg_dir, 'bap.cfg')

def get(key, default=None):
    """Get value from key:value in the config file."""
    from bap.utils import bap_comment
    if not os.path.exists(cfg_path):
        return default
    with open(cfg_path, 'r') as f:
        return bap_comment.get_value(f.read(), key, default)

def set(key, value):
    """Set key:value in the config file."""
    from bap.utils import bap_comment
    try:
        with open(cfg_path, 'r') as f:
            s = f.read()
    except IOError:
        s = ''
    s = bap_comment.add_to_comment_string(s, key, value)
    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)
    with open(cfg_path, 'w') as f:
        f.write(s)
