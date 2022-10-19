#
# modules/motando_utils.py
#

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