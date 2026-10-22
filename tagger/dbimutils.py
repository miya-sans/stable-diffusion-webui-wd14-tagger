"""DanBooru IMage Utility functions"""

import cv2
import numpy as np
from PIL import Image


def fill_transparent(image: Image.Image, color='WHITE'):
    image = image.convert('RGBA')
    new_image = Image.new('RGBA', image.size, color)
    new_image.paste(image, mask=image)
    image = new_image.convert('RGB')
    return image


def resize(pic: Image.Image, size: int, keep_ratio=True) -> Image.Image:
    if not keep_ratio:
        target_size = (size, size)
    else:
        min_edge = min(pic.size)
        target_size = (
            int(pic.size[0] / min_edge * size),
            int(pic.size[1] / min_edge * size),
        )

    target_size = (target_size[0] & ~3, target_size[1] & ~3)

    return pic.resize(target_size, resample=Image.Resampling.LANCZOS)


def smart_imread(img, flag=cv2.IMREAD_UNCHANGED):
    """ Read an image, convert to 24-bit if necessary """
    if img.endswith(".gif"):
        img = Image.open(img)
        img = img.convert("RGB")
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(img, flag)
    return img


def smart_24bit(img):
    """ Convert an image to 24-bit if necessary """
    if img.dtype is np.dtype(np.uint16):
        img = (img / 257).astype(np.uint8)

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        trans_mask = img[:, :, 3] == 0
        img[trans_mask] = [255, 255, 255, 255]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img


def make_square(img, target_size):
    """ Make an image square """
    old_size = img.shape[:2]
    desired_size = max(old_size)
    desired_size = max(desired_size, target_size)

    delta_w = desired_size - old_size[1]
    delta_h = desired_size - old_size[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    color = [255, 255, 255]
    new_im = cv2.copyMakeBorder(
        img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
    )
    return new_im


def smart_resize(img, size):
    """ Resize an image """
    # Assumes the image has already gone through make_square
    if img.shape[0] > size:
        img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)
    elif img.shape[0] < size:
        img = cv2.resize(img, (size, size), interpolation=cv2.INTER_CUBIC)
    return img


# Pillow/numpy equivalents of the transforms in an animetimm preprocess.json,
# matching imgutils.preprocess (create_pillow_transforms) of deepghs/imgutils
RESAMPLE = {
    'nearest': Image.Resampling.NEAREST,
    'bilinear': Image.Resampling.BILINEAR,
    'bicubic': Image.Resampling.BICUBIC,
    'box': Image.Resampling.BOX,
    'hamming': Image.Resampling.HAMMING,
    'lanczos': Image.Resampling.LANCZOS,
}


def _hw(size):
    """ size as (height, width), as torchvision interprets it """
    if isinstance(size, int):
        return size, size
    if len(size) == 1:
        return size[0], size[0]
    return size[0], size[1]


def pad_to_size(pic: Image.Image, size, background_color='white',
                interpolation='bilinear') -> Image.Image:
    """ Fit the image into size keeping aspect ratio, pad the remainder """
    # imgutils parses a pad size as (width, height)
    target_w, target_h = (size, size) if isinstance(size, int) else size
    ratio = min(target_w / pic.width, target_h / pic.height)
    new_w, new_h = round(pic.width * ratio), round(pic.height * ratio)

    resized = pic.resize((new_w, new_h), RESAMPLE[interpolation])
    canvas = Image.new(pic.mode, (target_w, target_h),
                       tuple(background_color)
                       if isinstance(background_color, list)
                       else background_color)
    canvas.paste(resized, ((target_w - new_w) // 2, (target_h - new_h) // 2))
    return canvas


def resize_to(pic: Image.Image, size, interpolation='bilinear',
              max_size=None, antialias=True) -> Image.Image:
    """ torchvision style Resize, an int size resizes the shortest edge """
    if isinstance(size, int) or len(size) == 1:
        size = size if isinstance(size, int) else size[0]
        if pic.width < pic.height:
            new_w, new_h = size, int(size * pic.height / pic.width)
        else:
            new_w, new_h = int(size * pic.width / pic.height), size
        if max_size is not None and max(new_w, new_h) > max_size:
            if new_h > new_w:
                new_w, new_h = int(max_size * new_w / new_h), max_size
            else:
                new_w, new_h = max_size, int(max_size * new_h / new_w)
    else:
        new_h, new_w = size

    if (new_w, new_h) == pic.size:
        return pic
    resample = RESAMPLE[interpolation]
    if resample in (Image.Resampling.BILINEAR, Image.Resampling.BICUBIC):
        return pic.resize((new_w, new_h), resample,
                          reducing_gap=None if antialias else 1.0)
    return pic.resize((new_w, new_h), resample)


def center_crop(pic: Image.Image, size) -> Image.Image:
    """ Crop the center, pad with black if the image is too small """
    crop_h, crop_w = _hw(size)
    if pic.width < crop_w or pic.height < crop_h:
        pad_w = max(crop_w - pic.width, 0)
        pad_h = max(crop_h - pic.height, 0)
        padded = Image.new(pic.mode, (pic.width + pad_w, pic.height + pad_h))
        padded.paste(pic, (pad_w // 2, pad_h // 2))
        pic = padded

    left = (pic.width - crop_w) // 2
    top = (pic.height - crop_h) // 2
    return pic.crop((left, top, left + crop_w, top + crop_h))


def to_chw_array(pic) -> np.ndarray:
    """ PIL RGB image to a float32 CHW array in [0, 1] """
    if isinstance(pic, np.ndarray):
        return pic
    return np.asarray(pic.convert('RGB'), dtype=np.float32) \
             .transpose((2, 0, 1)) / 255


def normalize(array: np.ndarray, mean, std) -> np.ndarray:
    mean = np.array(mean, dtype=np.float32).reshape(-1, 1, 1)
    std = np.array(std, dtype=np.float32).reshape(-1, 1, 1)
    return (array - mean) / std


def make_transforms(steps: list):
    """ Compose the transforms listed in an animetimm preprocess.json """
    creators = {
        'pad_to_size': lambda **kw: lambda x: pad_to_size(x, **kw),
        'resize': lambda **kw: lambda x: resize_to(x, **kw),
        'center_crop': lambda size: lambda x: center_crop(x, size),
        'convert_rgb': lambda force_background='white':
            lambda x: x.convert('RGB') if force_background is None
            else fill_transparent(x, force_background),
        'to_tensor': lambda: to_chw_array,
        'maybe_to_tensor': lambda: to_chw_array,
        'normalize': lambda mean, std, inplace=False:
            lambda x: normalize(x, mean, std),
        'rescale': lambda rescale_factor=1 / 255:
            lambda x: x * np.float32(rescale_factor),
    }
    transforms = []
    for step in steps:
        step = dict(step)
        kind = step.pop('type')
        if kind not in creators:
            raise NotImplementedError(f'Unsupported preprocess step: {kind}')
        transforms.append(creators[kind](**step))

    def apply(pic):
        for transform in transforms:
            pic = transform(pic)
        return pic
    return apply
