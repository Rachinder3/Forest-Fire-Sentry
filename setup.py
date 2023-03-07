from setuptools import setup, find_packages


PROJECT_NAME = "wildfire-smoke-object-detection"
PROJECT_VERSION = "0.0.1"
PROJECT_AUTHOR = "Rachinder Singh"
PROJECT_AUTHOR_EMAIL = "rachindersingh@gmail.com"
PROJECT_DESCRIPTION = "Build an object detection solution to detect wildfire smoke"
REQUIREMENTS_FILE_NAME = "requirements.txt"




setup(
    name = PROJECT_NAME,
    version= PROJECT_VERSION,
    author= PROJECT_AUTHOR,
    author_email=PROJECT_AUTHOR_EMAIL,
    description=PROJECT_DESCRIPTION, 
    packages=find_packages()
)

