import argparse

import cv2
from PIL import Image

from Learner import face_learner
from config import get_config
from mtcnn import MTCNN
from utils import load_facebank, draw_box_name, prepare_facebank


def indentify():
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
    print('mtcnn loaded')

    learner = face_learner(conf, True)
    learner.threshold = args.threshold
    learner.load_state(conf, 'mobilefacenet.pth', True, True)
    learner.model.eval()
    print('learner loaded')

    if args.update:
        targets, names = prepare_facebank(conf, learner.model, mtcnn, args.tta)
        print('facebank updated')
    else:
        targets, names = load_facebank(conf)
        print('facebank loaded')

    # initialize camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)
    video_writer = None
    if args.save:
        video_writer = cv2.VideoWriter(conf.data_path / 'recording.avi',
                                       cv2.VideoWriter_fourcc(*'XVID'), 6,
                                       (1280, 720))
    while cap.isOpened():
        is_success, frame = cap.read()
        if is_success:
            # 从视频流读取的当前帧图像数据
            image = Image.fromarray(frame[..., ::-1])  # bgr to rgb

            # 使用MTCNN算法检测图像中的人脸，
            # 并返回每个检测到的人脸的边界框和对齐后的人脸图像。
            bboxes, faces = mtcnn.align_multi(image, conf.face_limit,
                                              conf.min_face_size)

            '''
            bounding_boxes的形状是(10,5)，
                其中第一维表示检测到的人脸数量，第二维表示每个人脸边界框的四个角的坐标
                和置信度信息。
            bboxes[:i, :j]表示保留第一维的前i个元素、第二维的前j个元素;
            bboxes[:-i, :-j]表示去除第一维的后i个元素、第二维的后j个元素, 
                保留其他元素;
            '''
            # 保留10个可信度最高的人脸(10个就是全保留), 剔除置信度
            bboxes = bboxes[:, :-1]
            # 将bboxes数组中所有元素转换为整数类型,绘制矩形要求边界框的坐标必须为整数
            bboxes = bboxes.astype(int)
            # 对bboxes中的每个边界框进行微调，使其能够完全包含人脸。
            # 左上角横纵坐标各减1，右下角横纵坐标各加1。
            bboxes = bboxes + [-1, -1, 1, 1]

            # 使用预先训练好的人脸识别模型对检测到的人脸进行识别，
            # 返回每个人脸的识别结果和相应的置信度得分。
            results, score = learner.infer(conf, faces, targets, args.tta)

            # 循环遍历每个检测到的人脸，借用utils.py的函数并在图像中绘制一个矩形框，
            # 将其与已知的人脸进行比较，以确定它是否属于某个已知的人脸。
            for idx, bbox in enumerate(bboxes):
                if score[idx] >= 1:
                    frame = draw_box_name(bbox, "unknown", frame)
                elif args.score:
                    # 如果args.score参数设置为True，则会在矩形框旁边显示置信度得分
                    frame = draw_box_name(
                        bbox,
                        names[results[idx] + 1]
                        + '_{:.2f}'.format(score[idx]),
                        frame
                    )
                else:
                    # 否则只显示人名
                    frame = draw_box_name(bbox, names[results[idx] + 1], frame)

            cv2.imshow('face Capture', frame)

        if args.save:
            video_writer.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('Q'):
            break

    cap.release()
    if args.save:
        video_writer.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    indentify()
