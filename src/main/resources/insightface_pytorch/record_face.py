import argparse
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from config import get_config
from mtcnn import MTCNN
from utils import draw_box_name


# 为图片添加文本
def image_text(image, count):
    # 转换为RGB格式并使用PIL处理
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    # 添加中文文本
    font = ImageFont.truetype('simsun.ttc', 36)
    draw.text((0, 0),
              '按T键拍照,拍照三次后自动退出或按Q键退出,已拍'
              + str(count) + '张照片',
              font=font, fill=(0, 255, 0))
    # 转换回OpenCV格式并显示
    return cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)


# 录入人脸
def record():
    parser = argparse.ArgumentParser(description='take a picture')
    parser.add_argument('--name', '-n', default='unknown', type=str,
                        help='input the user_id of the recording person')
    args = parser.parse_args()

    # 人脸保存路径
    data_path = Path('data')
    save_path = data_path / 'facebank' / args.name
    if not save_path.exists():
        save_path.mkdir()

    conf = get_config(False)

    mtcnn = MTCNN()

    # initialize camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)

    count = 0

    # 检测人脸
    while cap.isOpened():
        is_success, frame = cap.read()

        if is_success:
            # 检测显示的这一帧中的人脸
            image = Image.fromarray(frame[..., ::-1])
            bboxes, faces = mtcnn.align_multi(image, conf.face_limit,
                                              conf.min_face_size)
            if len(bboxes) & len(faces):
                bboxes = bboxes[:1, :-1]
                bboxes = bboxes.astype(int)
                bboxes = bboxes + [-1, -1, 1, 1]
                # 将一张可能性最高的人脸框出来
                frame = draw_box_name(bboxes[0], name=args.name, frame=frame)

            cv2.imshow("camera", image_text(frame, count))

        # 实现按下“T”键拍照
        if cv2.waitKey(1) & 0xFF == ord('T'):
            try:
                warped_face = np.array(mtcnn.align(faces[0]))[..., ::-1]
                cv2.imwrite(
                    str(save_path / '{}.jpg'.format(str(datetime.now())[:-7]
                                                    .replace(":", "-")
                                                    .replace(" ", "-"))),
                    warped_face)
                count += 1
            except:
                print('没有捕捉到人脸')
            if count >= 3:
                return 0
        # 按下“Q”键退出
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            return -1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    result = record()
    print(result)
