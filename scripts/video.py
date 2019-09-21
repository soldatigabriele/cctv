import cv2

class Helper:
    def extractFrames(self, video_path, output_path, frames_interval = 24):
        vc = cv2.VideoCapture(video_path)
        c=1
        name = 1

        if vc.isOpened():
            rval , frame = vc.read()
        else:
            rval = False

        while rval:
            rval, frame = vc.read()
            if c%(frames_interval) == 0 :
                cv2.imwrite(output_path +'/'+ str(name) + '.jpg',frame)
                cv2.waitKey(1)
                name = name + 1
            c = c + 1
        vc.release()
