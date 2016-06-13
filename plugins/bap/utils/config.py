import os

"""Package all configuration related methods together."""

_dir = os.path.join(os.getenv('HOME'), '.bap')
_file_path = os.path.join(_dir, 'config')

def get(key, default=None):
    """Get value from key:value in the config file."""
    from bap.utils import bap_comment
    if not os.path.exists(_file_path):
        return default
    with open(_file_path, 'r') as f:
        return bap_comment.get_value(f.read(), key, default)

def set(key, value):
    """Set key:value in the config file."""
    from bap.utils import bap_comment
    try:
        with open(_file_path, 'r') as f:
            s = f.read()
    except IOError:
        s = ''
    s = bap_comment.add_to_comment_string(s, key, value)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    with open(_file_path, 'w') as f:
        f.write(s)
