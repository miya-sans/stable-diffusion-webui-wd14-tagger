"""Install requirements for WD14-tagger."""
import os
import sys
from importlib.util import find_spec

from launch import run  # pylint: disable=import-error

NAME = "WD14-tagger"
req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        "requirements.txt")
print(f"loading {NAME} reqs from {req_file}")
run(f'"{sys.executable}" -m pip install -q -r "{req_file}"',
    f"Checking {NAME} requirements.",
    f"Couldn't install {NAME} requirements.")

# use the OpenCV the WebUI comes with. Changing it fails while cv2 is in use
# and could break the WebUI, e.g. Forge Neo pins opencv-python 5.x. Without
# one, <4.12 keeps numpy 1.x for WebUIs on gradio 3.x.
if find_spec("cv2") is None:
    run(f'"{sys.executable}" -m pip install -q "opencv_python<4.12"',
        f"Installing OpenCV for {NAME}.",
        f"Couldn't install OpenCV for {NAME}.")
