from flask import Flask, request, jsonify
import os

from app_utils import *

from yolov5.detect import *



## initializations#########################################################
app = Flask(__name__)
ROOT_DIR = os.getcwd()
model_dir = "model"
model_file_name = "best.pt"
model_path = os.path.join(model_dir,model_file_name)
yolov5_dir = "yolov5"
detect_script = "detect.py"
detect_script_path = os.path.join(yolov5_dir,detect_script)
input_store_dir = "inputs"
output_store_dir = "outputs"
image_file_name = "image.jpg"
video_file_name = "video.mp4"
os.makedirs(input_store_dir,exist_ok=True)
os.makedirs(output_store_dir, exist_ok=True)

############################################################################3

app = Flask(__name__)

#### api definitions ########################################################
@app.route('/predictions_via_api', methods = ['GET','POST'])
def predictions_via_api():
    '''
        operates on a single image

        input: image in base64 format
        
        output: image in base64 format
    
    
    '''
    
    
    try:
        if request.method == 'POST':
            #### Reading the image in base 64 format
            image_base64 = request.json["image"]
            
            # converting image from base64 to actual image
            image_path = os.path.join(input_store_dir, image_file_name)
            base64_2_img(image_base64, image_path)
            
            
            #### object detection on the image
            detection = run(weights=model_path,source=image_path,project=output_store_dir,name=current_time_stamp, exist_ok=True)
            
            
            #### getting detection image
            detected_image_path = os.path.join(output_store_dir,current_time_stamp,image_file_name)
            
            
            ### converting image to base64
            image64 = image_2_base64(detected_image_path)
            return image64            
            
            
            
            
            
        
            
            
    except Exception as e:
        print(str(e))







###############################################################################

#### main method

if __name__ == '__main__':
    app.run()
    
    





