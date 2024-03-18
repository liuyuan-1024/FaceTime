import argparse
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from config import get_config
from mtcnn import MTCNN


# 录入人脸
def record():
    parser = argparse.ArgumentParser(description='take a picture')
    parser.add_argument('--name', '-n', required=True, type=str,
                        help='input the user_id of the recording person')
    parser.add_argument("-i", "--image", help="path to input image",
                        required=True, type=str)
    args = parser.parse_args()

    image = Image.open(args.image)

    # 人脸保存路径
    data_path = Path('data')
    save_path = data_path / 'facebank' / args.name
    if not save_path.exists():
        save_path.mkdir()

    conf = get_config(False)
    mtcnn = MTCNN()

    # 检测这一帧图片中的人脸
    bboxes, faces = mtcnn.align_multi(image, conf.face_limit,
                                      conf.min_face_size)

    # 未在图片中检测到人脸
    if not (len(bboxes) & len(faces)):
        return -1

    face = faces[0]

    try:
        warped_face = np.array(mtcnn.align(face))[..., ::-1]
        cv2.imwrite(
            str(save_path / '{}.jpg'.format(str(datetime.now())[:-7]
                                            .replace(":", "-")
                                            .replace(" ", "-"))),
            warped_face)
        return 0
    except:
        return -1


if __name__ == '__main__':
    result = record()
    print(result)
