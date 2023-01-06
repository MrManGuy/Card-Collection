import os, time
import cv2

def main():
    current_path = os.getcwd() + "\\Card-Collection"
    card_sets_path = os.path.dirname(current_path) + '\\Pokemon'
    
    os.chdir(card_sets_path + "\\imgs")
    img_files = os.listdir()
    cam = cv2.VideoCapture(0)
    result, cam_image = cam.read()

    if not result:
        print("Failed to get image")
    cv2.imshow("Card", cam_image)
    cv2.waitKey(0)
    cv2.destroyWindow("Card")

    #for image in img_files:
        

if __name__ == "__main__":
    startTime = time.time()
    main()
    print(time.time() - startTime)