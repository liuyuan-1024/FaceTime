import argparse

from PIL import Image

from Learner import face_learner
from config import get_config
from mtcnn import MTCNN
from utils import prepare_facebank


def sign2():
    parser = argparse.ArgumentParser(description='for face verification')
    parser.add_argument('-th', '--threshold',
                        help='threshold to decide identical faces',
                        default=1.54, type=float)
    parser.add_argument("-i", "--image", help="path to input image",
                        required=True, type=str)
    args = parser.parse_args()

    image = Image.open(args.image)

    conf = get_config(False)
    mtcnn = MTCNN()

    learner = face_learner(conf, True)
    learner.threshold = args.threshold
    learner.load_state(conf, 'mobilefacenet.pth', True, True)
    learner.model.eval()

    # 更新 facebank模型
    targets, names = prepare_facebank(conf, learner.model, mtcnn)

    # 使用MTCNN算法检测图像中的人脸，
    # 并返回每个检测到的人脸的边界框和对齐后的人脸图像。
    bboxes, faces = mtcnn.align_multi(image, conf.face_limit,
                                      conf.min_face_size)

    # 未在图片中检测到人脸
    if not (len(bboxes) & len(faces)):
        return -1

    # 使用预先训练好的人脸识别模型对检测到的人脸进行识别，
    results, score = learner.infer(conf, faces, targets)

    face = faces[0]

    if score[0] >= 1:
        return -1
    else:
        return names[results[0] + 1]


if __name__ == '__main__':
    result = sign2()
    print(result)
