from AIDetector_pytorch import Detector
import imutils
import cv2
import argparse


capture_width = 1280
capture_height = 720
display_width = 1280
display_height = 720
framerate = 60
flip_method = 0

#设置gstreamer管道参数
def gstreamer_pipeline(
    capture_width=1280, #摄像头预捕获的图像宽度
    capture_height=720, #摄像头预捕获的图像高度
    display_width=1280, #窗口显示的图像宽度
    display_height=720, #窗口显示的图像高度
    framerate=60,       #捕获帧率
    flip_method=0,      #是否旋转图像
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def main():
    parser = argparse.ArgumentParser(description='yolov5 head detect')

    parser.add_argument('--source', type=str,default="csi",
                        help='input csi or usb or video')
    parser.add_argument('--device',type=int, default=0,
                        help='if you choose usb, please input 0, 1 or n device number you want use')
    parser.add_argument('--thresh',type=int, default=30,
                        help='detect num warning thresh hold')
    args = parser.parse_args()
    func_status = {}
    func_status['headpose'] = None
    
    name = 'demo'

    det = Detector()
    if args.source=="csi":
        cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    elif args.source == "usb":
        cap = cv2.VideoCapture(args.device)
    else:
        # use video , args.source is video path
        cap = cv2.VideoCapture(args.source)
    fps = int(cap.get(5))
    print('fps:', fps)
    t = int(1000/fps)

    size = None
    videoWriter = None

    while True:

        # try:
        _, im = cap.read()
        if im is None:
            break
        
        result = det.feedCap(im, func_status)
        detect_num = result["faces"]
        result = result['frame']
        result = imutils.resize(result, height=500)
        if detect_num>=args.thresh:
            text = "detect num :{}".format(detect_num)
            color = (0,255,0)
            size = (result.shape[1]-200,20)
        else:
            text = "detect num :{},warning,Below threshold".format(detect_num)
            color = (0,0,255)
            size = (result.shape[1]-500,30)
        cv2.putText(result,text,size,cv2.FONT_HERSHEY_COMPLEX,0.7,color,1)
        # if videoWriter is None:
        #     fourcc = cv2.VideoWriter_fourcc(
        #         'm', 'p', '4', 'v')  # opencv3.0
        #     videoWriter = cv2.VideoWriter(
        #         'result.mp4', fourcc, fps, (result.shape[1], result.shape[0]))

        # videoWriter.write(result)
        # cv2.imwrite("",im)
        cv2.imshow(name, result)
        cv2.waitKey(t)

        if cv2.getWindowProperty(name, cv2.WND_PROP_AUTOSIZE) < 1:
            # 点x退出
            break
        # except Exception as e:
        #     print(e)
        #     break

    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    main()