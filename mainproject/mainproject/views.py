from django.shortcuts import render
from django.http.response import  HttpResponse 

import os
import shutil

import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

def home(request):
    #os.system("python mainproject/yolov5/detect.py --weights mainproject/yolov5/runs/train/exp/weights/best1.pt --img 416 --conf 0.4 --source D:/projects/projectws/YOLO-License-Plate-Detection-Web-App-main/dataset/images")
    return render(request,'home.html')
def upload(request):
    if request.method=="POST":
        file=request.FILES
        files=file['file']
        filess=open('D:/projects/projectws/mainproject-django/mainproject/mainproject/static/save.jpg','wb')
        filess.write(files.read())
        filess.close()
        return render(request,'home.html')
    
    
def detect_person_and_bike(request):
    if request.method=="POST":
        path = "mainproject/yolov5/runs/detect/exp"
        try:
            shutil.rmtree(path)
            print("% s removed successfully" % path)
        except OSError as error:
            print(error)
        os.system("python mainproject/yolov5/detect.py --weights mainproject/yolov5/runs/train/exp/weights/best4.pt --img 416 --conf 0.4 --source D:/projects/projectws/mainproject-django/mainproject/mainproject/static/save.jpg")
        files=open(path+'/save.jpg','rb')
        filess=open('D:/projects/projectws/mainproject-django/mainproject/mainproject/static/save2.jpg','wb')
        filess.write(files.read())
        filess.close()
        #os.system("python mainproject/yolov5/detect.py --weights mainproject/yolov5/runs/train/exp/weights/best1.pt --img 416 --conf 0.4 --source save.jpg")
        return render(request,'home.html')
    
    
def helmet_and_numberplate(request):
    if request.method=="POST":
        path = "mainproject/yolov5/runs/detect/exp2"
        try:
            shutil.rmtree(path)
            print("% s removed successfully" % path)
        except OSError as error:
            print(error)
        os.system("python mainproject/yolov5/detect.py --weights mainproject/yolov5/runs/train/exp/weights/best1.pt --img 416 --conf 0.4 --source D:/projects/projectws/mainproject-django/mainproject/mainproject/static/save.jpg")
        files=open(path+'/save.jpg','rb')
        filess=open('D:/projects/projectws/mainproject-django/mainproject/mainproject/static/save3.jpg','wb')
        filess.write(files.read())
        filess.close()
        result1=False
        try:
            path="D:/projects/projectws/mainproject-django/mainproject/mainproject/yolov5/runs/detect/exp/crops/"
            for i in os.listdir(path):
                if i=='Numberplate':
                    results='Numberplate Detected'
                if i=='No-helmet':
                    results='No Helmet Detected'
                if 'Numberplate' in os.listdir(path) and 'No-helmet' in os.listdir(path):
                    results="Helmet Not Dected and Number Plate Detected"
                else:
                    results='No Helmet Detected'

            files=open("D:/projects/projectws/mainproject-django/mainproject/mainproject/yolov5/runs/detect/exp/crops/Numberplate/save.jpg",'rb')
            filess=open('D:/projects/projectws/mainproject-django/mainproject/mainproject/static/numberplate.jpg','wb')
            filess.write(files.read())
            filess.close()
            reader = easyocr.Reader(['en'])
            result1 = reader.readtext('D:/projects/projectws/mainproject-django/mainproject/mainproject/yolov5/runs/detect/exp/crops/Numberplate/save.jpg')
            
        except:
            pass
            
        result=False
        try:
            
            files=open("D:/projects/projectws/mainproject-django/mainproject/mainproject/yolov5/runs/detect/exp2/crops/license_plate/save.jpg",'rb')
            filess=open('D:/projects/projectws/mainproject-django/mainproject/mainproject/static/numberplate.jpg','wb')
            filess.write(files.read())
            filess.close()
            reader = easyocr.Reader(['en'])
            result = reader.readtext('D:/projects/projectws/mainproject-django/mainproject/mainproject/yolov5/runs/detect/exp2/crops/license_plate/save.jpg')
        except:
            pass
        if result and result1:
            results1=results+"<br>Number plate: "
            for i in range(len(result)):
                results1+=result[i][1]
                
            results1 +="   Or    "
            for i in range(len(result1)):
                results1+=result1[i][1]
        
        elif result:
            results1=results+"<br>Number plate: "
            for i in range(len(result)):
                results1+=result[i][1]+" "
        
        elif result1:
            results1=results+"<br>Number plate: "
            for i in range(len(result1)):
                results1+=result1[i][1]+" "
        else:
            results1='Sorry'
        return HttpResponse(results1)

