#
# modules/motando_utils.py
#

import unicodedata


def return_img_mimetype(img_filename: str = None) -> str:
    """Return image MIME TYPE.

    """
    if img_filename.endswith('.jpg') or img_filename.endswith('.jpeg'):
        return 'image/jpeg'
    elif img_filename.endswith('.png'):
        return 'image/png'
    elif img_filename.endswith('.webp'):
        return 'image/webp'
    else:
        return None


def remove_ctr_chars(s: str = None) -> str:
    """Remove control characters from a string.

    https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
    
    """
    return ''.join(ch for ch in s if unicodedata.category(ch)[0]!='C')