import argparse

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from Learner import face_learner
from config import get_config
from mtcnn import MTCNN
from utils import draw_box_name, prepare_facebank


# 为图片添加文本
def image_text(image):
    # 转换为RGB格式并使用PIL处理
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    # 添加中文文本
    font = ImageFont.truetype('simsun.ttc', 36)
    draw.text((0, 0), '请按S键进行签到', font=font, fill=(0, 255, 0))
    # 转换回OpenCV格式并显示
    return cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)


def sign():
    parser = argparse.ArgumentParser(description='for face verification')
    parser.add_argument("-s", "--save", help="whether save",
                        action="store_true")
    parser.add_argument('-th', '--threshold',
                        help='threshold to decide identical faces',
                        default=1.54, type=float)
    parser.add_argument("-u", "--update",
                        help="whether perform update the facebank",
                        action="store_true")
    parser.add_argument("-tta", "--tta", help="whether test time augmentation",
                        action="store_true")
    parser.add_argument("-c", "--score",
                        help="whether show the confidence score",
                        action="store_true")
    args = parser.parse_args()

    conf = get_config(False)

    mtcnn = MTCNN()

    learner = face_learner(conf, True)
    learner.threshold = args.threshold
    learner.load_state(conf, 'mobilefacenet.pth', True, True)
    learner.model.eval()

    # 更新 facebank模型
    targets, names = prepare_facebank(conf, learner.model, mtcnn, args.tta)

    # initialize camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)

    user_id = None

    while cap.isOpened():
        is_success, frame = cap.read()
        if is_success:
            # 从视频流读取的当前帧图像数据
            image = Image.fromarray(frame[..., ::-1])  # bgr to rgb

            # 使用MTCNN算法检测图像中的人脸，
            # 并返回每个检测到的人脸的边界框和对齐后的人脸图像。
            bboxes, faces = mtcnn.align_multi(image, conf.face_limit,
                                              conf.min_face_size)

            # 检测到人脸后, 才进行识别
            if len(bboxes) & len(faces):
                # 保留1个可信度最高的人脸, 剔除置信度
                bboxes = bboxes[:1, :-1]
                bboxes = bboxes.astype(int)
                bboxes = bboxes + [-1, -1, 1, 1]

                # 使用预先训练好的人脸识别模型对检测到的人脸进行识别，
                results, score = learner.infer(conf, faces, targets, args.tta)

                bbox = bboxes[0]
                face = faces[0]

                if score[0] >= 1:
                    frame = draw_box_name(bbox, "unknown", frame)
                else:
                    # 检测到用户人脸
                    user_id = names[results[0] + 1]
                    frame = draw_box_name(bbox, user_id, frame)

            cv2.imshow("camera", image_text(frame))

        if cv2.waitKey(1) & 0xFF == ord('S'):
            try:
                np.array(mtcnn.align(face))[..., ::-1]
                return user_id
            except:
                return -1
        # 按下“Q”键退出
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    result = sign()
    print(result)
