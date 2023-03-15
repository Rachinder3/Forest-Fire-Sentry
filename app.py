from flask import Flask, request, jsonify, render_template, send_file
import os
from werkzeug.utils import secure_filename

from app_utils import *

from yolov5.detect import *

def play_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)

        # cap = cv2.VideoCapture(0)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))



        if cap.isOpened() == False:
            print("Error file not found")


        while cap.isOpened():
            ret, frame = cap.read()
    
            if ret == True:
                time.sleep(1/5)
        
        
      
        
        
                img = cv2.resize(frame,(1024,640))
        
        
        
        
                cv2.imshow('Camera feed', img)
        
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        
            
        
    
    except Exception as e:
        print(str(e))

## initializations#########################################################
app = Flask(__name__)
ROOT_DIR = os.getcwd()

static_dir = "static"
model_dir = "model"
model_file_name = "best.pt"
model_path = os.path.join(model_dir,model_file_name)
yolov5_dir = "yolov5"
detect_script = "detect.py"
detect_script_path = os.path.join(yolov5_dir,detect_script)
input_store_dir = "inputs"
output_store_dir = "outputs"


image_file_name = "input.jpg"


os.makedirs(input_store_dir,exist_ok=True)
# os.makedirs(output_store_dir, exist_ok=True)

###########  APIs  ###########################################################3

app = Flask(__name__)


#### views ########################################################
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



@app.route("/",methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/image_inference", methods=['GET','POST'])
def predictions_on_image():
    try:
        
        context = {}
            
        context["state"] = 0
        context["output"] = ""
        
        
        if request.method == 'POST' or request.method== 'GET':
            
           #### save file
           
            
            try:
                ###### Ingesting the File
                
                
                
                f = request.files['file']
                
                image_file_name = f.filename
                
                print(f.content_type)
                
                image_file_path = os.path.join(input_store_dir,image_file_name)
                f.save(image_file_path)
                ## enctype is multipart/form-data hence hence reques.form["confidence"] doesn't work. Hence using this approach
                confidence_threshold = int(request.form.to_dict()['confidence'])/100
                #print("file saved at: ", image_file_path , "confidence",confidence)
                
                
                #### Performing Detection
                result_dir = os.path.join(static_dir,output_store_dir)
                detection = run(weights=model_path,source=image_file_path,project=result_dir,name=current_time_stamp, exist_ok=True, conf_thres=confidence_threshold)
                
                output_file_path = os.path.join(result_dir, current_time_stamp, image_file_name)
                
                print(os.path.exists(output_file_path))
                print(output_file_path)
                
                
                if 'image' in f.content_type:
                    
                
                    context["state"] = 1
                    context["output"] = output_file_path
                    
                    print("here image")
                    # return send_file(output_file_path, as_attachment=True)
                    #return send_file(output_file_path)
                
                    return render_template("image_inference.html", context=context)
            
                elif 'video' in f.content_type:
                    context["state"] = 2
                    context["output"] = output_file_path
                    
                    
                    # return send_file(output_file_path, as_attachment=True)
                    #return send_file(output_file_path)
                
                    #return render_template("image_inference.html", context=context)
                    
                    play_video(video_path=output_file_path)
                    return send_file(path_or_file=output_file_path,mimetype="video/mp4", as_attachment=True)
                
                    
                return render_template("image_inference.html", context=context)
            
            except Exception as e:
                
                print(str(e))
                
                context = {}
            
                context["state"] = 0
                context["output"] = ""
                
                return render_template("image_inference.html", context=context)
                #return f"test exception {context}"
            
            
            
            
    
    except Exception as e:
        print(str(e))
        
        





###############################################################################

#### main method

if __name__ == '__main__':
    #app.run(debug=True)
    app.run()
    





