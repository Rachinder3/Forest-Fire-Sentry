# Wildfire-Smoke-Object-Detction
Goal: Develop an object detection model capable of identifying areas where forest fire may have started

[Dataset can be found here](https://universe.roboflow.com/rachinder-singh-mnody/smoke-detection-l0mxg)



# Project Setup

1) Creating environment: conda create -p venv python==3.8 -y
2) Activate environment: conda activate ./venv
3) Install requirements: pip install -r requirements.txt




## Updations to yolov5.detect script

Have updated --exist ok to not auto increment.

Default: parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')

Modified: parser.add_argument('--exist-ok', action='store_false', help='existing project/name ok, do not increment')

### Build Docker image
docker build -t <image-name><tag-name>
Image Name must be in lower case

#### List Docker images
docker images

### Run Docker Image
docker run -p 5000:5000 -e PORT=5000 image-id



#### To check running containers: 
docker ps

#### To stop docker container
docker stop container_id

#### Running setup.py
python setup.py install


Checking