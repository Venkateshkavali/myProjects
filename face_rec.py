# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 23:13:03 2021

@author: venka
"""

import cv2 as cv
import dlib
import numpy as np
import xlsxwriter
import face_recognition

def faceCompare(l1,l2,image):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(l1, face_encoding)
        face_distances = face_recognition.face_distance(l1, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            return [True,best_match_index]
    return [False,0]
if __name__ == "__main__":
    workbook = xlsxwriter.Workbook('images.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 30)

    detector = dlib.get_frontal_face_detector()
    
    l1=[]
    l2=[]

    cap = cv.VideoCapture("E:/Sprng 2021/New folder/Programming-assignment/video/test1.mp4")
    i=1;
    j=0;
    while True:
        ret, frame = cap.read()
        if not ret:
            print("noframe.")
            break
        gray_image=cv.cvtColor(src=frame,code=cv.COLOR_BGR2GRAY)
        faces = detector(gray_image)
        print(np.shape(faces)[0],i)
        k=np.shape(faces)[0]
        for face in faces:
            x1 = face.left() # left point
            y1 = face.top() # top point
            x2 = face.right() # right point
            y2 = face.bottom() # bottom point
            cv.rectangle(img=frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=4)
            image=frame[y1:y2,x1:x2]
            c=face_recognition.face_encodings(image)
            if len(l1)==0:
                l1.append(c[0])
                l2.append(len(l1))
                cv.putText(frame,"person"+str(len(l1)),(x1,y1),cv.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
                cv.imwrite("E:/Sprng 2021/New folder/Programming-assignment/unique_images/proj_images"+str(j)+".jpg",frame)
                worksheet.insert_image('B'+str(j+10),"E:/Sprng 2021/New folder/Programming-assignment/unique_images/proj_images"+str(j)+".jpg" ,{'x_scale': 0.1, 'y_scale': 0.1})
                j=j+1
            else:
                [a,b]=faceCompare(l1,l2,image)
                if a==True:
                    cv.putText(frame,"person"+str(l2[b]),(x1,y1),cv.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
                else:
                    if len(c)>0:
                        l1.append(c[0])
                        l2.append(len(l1))
                        cv.putText(frame,"person"+str(len(l1)),(x1,y1),cv.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
                        cv.imwrite("E:/Sprng 2021/New folder/Programming-assignment/unique_images/proj_images"+str(j)+".jpg",frame)
                        worksheet.insert_image('B'+str(j+10),"E:/Sprng 2021/New folder/Programming-assignment/unique_images/proj_images"+str(j)+".jpg" ,{'x_scale': 0.1, 'y_scale': 0.1})
                        j=j+1
        cv.putText(frame,"number of people="+str(k),(50,50),cv.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
        cv.imwrite("E:/Sprng 2021/New folder/Programming-assignment/frames/frame"+str(i)+".jpg",frame)
        i=i+1;
    workbook.close()