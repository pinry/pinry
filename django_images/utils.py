from contextlib import contextmanager
from io import BytesIO
import PIL
from PIL import Image


@contextmanager
def open_django_file(field_file):
    field_file.open()
    try:
        yield field_file
    finally:
        field_file.close()


def scale_and_crop_iter(image, options):
    """
    Generator which will yield several variations on the input image.
    Resize, crop and/or change quality of image.

    :param image: Source image file
    :type image : :class:`django.core.files.images.ImageFile

    :param options: List of option dictionaries, See scale_and_crop_single
    argument names for available keys.
    :type options: list of dict
    """
    with open_django_file(image) as img:
        im = Image.open(img)
        im.load()
        for opts in options:
            # Use already-loaded file when cropping.
            yield scale_and_crop_single(im, **opts)


# this neat function is based on easy-thumbnails
def scale_and_crop_single(image, size, crop=False, upscale=False, quality=None):
    """
    Resize, crop and/or change quality of an image.

    :param image: Source image file
    :type image: :class:`PIL.Image`

    :param size: Size as width & height, zero as either means unrestricted
    :type size: tuple of two int

    :param crop: Truncate image or not
    :type crop: bool

    :param upscale: Enable scale up
    :type upscale: bool

    :param quality: Value between 1 to 95, or None for keep the same
    :type quality: int or NoneType

    :return: Handled image
    :rtype: class:`PIL.Image`
    """
    im = image

    source_x, source_y = [float(v) for v in im.size]
    target_x, target_y = [float(v) for v in size]

    if crop or not target_x or not target_y:
        scale = max(target_x / source_x, target_y / source_y)
    else:
        scale = min(target_x / source_x, target_y / source_y)

    # Handle one-dimensional targets.
    if not target_x:
        target_x = source_x * scale
    elif not target_y:
        target_y = source_y * scale

    if scale < 1.0 or (scale > 1.0 and upscale):
        im = im.resize((int(source_x * scale), int(source_y * scale)),
                       resample=Image.ANTIALIAS)

    if crop:
        # Use integer values now.
        source_x, source_y = im.size
        # Difference between new image size and requested size.
        diff_x = int(source_x - min(source_x, target_x))
        diff_y = int(source_y - min(source_y, target_y))
        if diff_x or diff_y:
            # Center cropping (default).
            half_diff_x, half_diff_y = diff_x // 2, diff_y // 2
            box = [half_diff_x, half_diff_y,
                   min(source_x, int(target_x) + half_diff_x),
                   min(source_y, int(target_y) + half_diff_y)]
            # Finally, crop the image!
            im = im.crop(box)

    # Close image and replace format/metadata, as PIL blows this away.
    # We mutate the quality, but needs to passed into save() to actually
    # do anything.
    info = image.info
    if quality is not None:
        info['quality'] = quality
    im.format, im.info = image.format, info
    return im


def write_image_in_memory(img):
    # save to memory
    buf = BytesIO()
    try:
        img.save(buf, img.format, **img.info)
    except IOError:
        if img.info.get('progression'):
            orig_MAXBLOCK = PIL.ImageFile.MAXBLOCK
            temp_MAXBLOCK = 1048576
            if orig_MAXBLOCK >= temp_MAXBLOCK:
                raise
            PIL.ImageFile.MAXBLOCK = temp_MAXBLOCK
            try:
                img.save(buf, img.format, **img.info)
            finally:
                PIL.ImageFile.MAXBLOCK = orig_MAXBLOCK
        else:
            raise
    return buf
