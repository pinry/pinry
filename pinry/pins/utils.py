import PIL
import mimetypes

mimetypes.init()


# this neat function is based on django-images and easy-thumbnails
def scale_and_crop(image, size, crop=False, upscale=False, quality=None):
    # Open image and store format/metadata.
    image.open()
    im = PIL.Image.open(image)
    im_format, im_info = im.format, im.info
    if quality:
        im_info['quality'] = quality

    # Force PIL to load image data.
    im.load()

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
                       resample=PIL.Image.ANTIALIAS)

    if crop:
        # Use integer values now.
        source_x, source_y = im.size
        # Difference between new image size and requested size.
        diff_x = int(source_x - min(source_x, target_x))
        diff_y = int(source_y - min(source_y, target_y))
        if diff_x or diff_y:
            # Center cropping (default).
            halfdiff_x, halfdiff_y = diff_x // 2, diff_y // 2
            box = [halfdiff_x, halfdiff_y,
                   min(source_x, int(target_x) + halfdiff_x),
                   min(source_y, int(target_y) + halfdiff_y)]
            # Finally, crop the image!
            im = im.crop(box)

    # Close image and replace format/metadata, as PIL blows this away.
    im.format, im.info = im_format, im_info
    image.close()
    return im

