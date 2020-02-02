import time
import numpy as np

from PIL import Image
from io import BytesIO
from datetime import datetime
from collections import defaultdict
from click import style

IMAGE_PIXEL_ORDERS = ('CHW', 'HWC')


def make_experiment_id():
    return time.strftime('%b%d_%H:%M:%S')


def is_pil_image(image):
    return isinstance(image, Image.Image)


def encode_pil_image(image, format='JPEG'):
    buffer = BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()


def numpy_image_to_pil_image(image, pixel_order=None):

    # remove empty dimensions
    image = np.squeeze(image)
    shape = image.shape
    ndim = image.ndim

    # grayscale image
    if ndim == 2:
        return Image.fromarray(image, mode='L')

    # RGB image
    elif ndim == 3:

        # if 3/4 channels in first dimension, assume CHW
        if (pixel_order == 'CHW' or
                (pixel_order is None and shape[0] in (3, 4))):
            image = image.transpose(1, 2, 0)

        if shape[2] not in (3, 4):
            raise ValueError(f'invalid number of channels: {shape[2]}')

        return Image.fromarray(image)

    raise ValueError(f'invalid dimension: {ndim}')


def encode_numpy_image(image, pixel_order=None):
    image = numpy_image_to_pil_image(image, pixel_order)
    return encode_pil_image(image)


def encode_image(image, pixel_order=None):
    if is_pil_image(image):
        return encode_pil_image(image)
    elif isinstance(image, np.ndarray):
        return encode_numpy_image(image, pixel_order)
    else:
        raise ValueError(f'unknown image type {type(image)}')


def decode_image(image_bytes):
    io = BytesIO(image_bytes)
    return Image.open(io)


def timestamp():
    return datetime.isoformat(datetime.now())


level_colors = defaultdict(lambda: 'white', {
    'CRITICAL': 'red',
    'ERROR': 'red',
    'WARNING': 'yellow',
    'INFO': 'green'
})


def style_level(level):
    return style(level, fg=level_colors[level], bold=True)


def make_epoch_summary(epoch, metrics):
    summary = [f'[{epoch:03d}]']
    for k, v in metrics.items():
        s = f'{k}: {v:.04f}'
        summary.append(s)
    summary = '  '.join(summary)
    return summary
