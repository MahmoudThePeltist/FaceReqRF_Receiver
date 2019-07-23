import cv2
import time
import os
import sys
import numpy as np
from SQLiteDBClass import *

class facial_recognition():

    def __init__(self, parent = None):
        #set window title and icon
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        self.faceDetector = 1
        self.faceRecognizer = 2        
        
    def detect_face(self, image):
        #face detection using lbp cascade classifier
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #get grayscale image
        if self.faceDetector == 0:
            trainerLocation = self.localDir + '/training-data/haarcascades/haarcascade_frontalface_alt.xml'
        elif self.faceDetector == 1:
            trainerLocation = self.localDir + '/training-data/lbpcascades/lbpcascade_frontalface.xml'
        elif self.faceDetector == 2:
            trainerLocation = self.localDir + '/training-data/lbpcascades/lbpcascade_frontalface_improved.xml'
        cascade_classifier = cv2.CascadeClassifier(trainerLocation)
        faces = cascade_classifier.detectMultiScale(grayscale_image, scaleFactor=1.2, minNeighbors=5);
        #skip all faces exept the fist one
        if(len(faces) == 0):
            return None, None     
        x, y, w, h = faces[0]
        #return the face only
        return grayscale_image[y:y+w, x:x+h], faces[0]

    def prepare_training_images(self, data_folder_path):
        #go through the directory and find folders
        dirs = os.listdir(data_folder_path)
        #go through the folders
        startTimeA = time.time()
        for dir_name in dirs:
            #if folder does not have j prefix, skip
            if not dir_name.startswith("j"):
                continue;
            #create the name for the face folder and get the path for it
            face_folder_name = dir_name.replace("j", "s")
            #if it exists skip, if it doesn't create it
            if os.path.exists(data_folder_path + "/" + face_folder_name):  
                print "folder: ", (data_folder_path + "/" + face_folder_name), " exists, skipping..."
                continue;
            if not os.path.exists(data_folder_path + "/" + face_folder_name):
                print "Directory: ", (data_folder_path + "/" + face_folder_name), " does not exist, creating..."
                os.makedirs(data_folder_path + "/" + face_folder_name)
            #get the path to the images
            subject_dir_path = data_folder_path + "/" + dir_name
            subject_images_names = os.listdir(subject_dir_path)
            #go through the images in the 'j' folders one by one
            for image_name in subject_images_names:
                if image_name.startswith("."):
                    continue; 
                image_path = subject_dir_path + "/" + image_name
                image = cv2.imread(image_path)
                cv2.imshow("Editing image...", image)
                #cv2.waitKey(10)
                #detect face
                face, rect = self.detect_face(image)
                #if face is real edit and add to face folder           
                if face is not None:
                    resized_face = cv2.resize(face,(350,350))
                    print "Face from image: ", image_name, " being added to ", (data_folder_path + "/" + face_folder_name)
                    cv2.imwrite(os.path.join((data_folder_path + "/" + face_folder_name),image_name),resized_face)
                    cv2.destroyAllWindows()
                cv2.waitKey(1)
            cv2.destroyAllWindows()            
        endTimeA = time.time()
        print "Preperation time: " + str(endTimeA - startTimeA)        
        return 0
   
    
    def prepare_training_data(self, data_folder_path):
        #go through the directory and find folders
        dirs = os.listdir(data_folder_path)
        faces_list = []
        labels_list = []
        #go through the folders
        for dir_name in dirs:
            #if folder does not have s prefix, skip
            if not dir_name.startswith("s"):
                continue;
            #get the label by removing folder prefix (in accordance with our naming scheme)
            label = int(dir_name.replace("s", ""))
            subject_dir_path = data_folder_path + "/" + dir_name
            subject_images_names = os.listdir(subject_dir_path)
            #go through the images in the 's' folders one by one
            for image_name in subject_images_names:
                #skip files . prefix because they are system files
                if image_name.startswith("."):
                    continue; 
                #get path to image then read the image and show it, delay 100ms
                image_path = subject_dir_path + "/" + image_name
                print 'looking for:', (subject_dir_path + "/" + image_name)
                image = cv2.imread(image_path)
                cv2.imshow("Training on image...", image)
                #cv2.waitKey(10)
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces_list.append(grayscale_image)
                labels_list.append(label)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
            cv2.destroyAllWindows()
        #return the list of faces and the list of lables for training
        return faces_list, labels_list
    
    
    def train(self, data_folder_path):
        #calls the prepare function and trains, self explanitory
        print "Preparing data..."
        faces, labels = self.prepare_training_data(data_folder_path)
        print "Data prepared"
        print "Number of faces: ", len(faces), "\nNumber of labels: ", len(labels)
        print "Creating recognizer..."
        if self.faceRecognizer == 0:
            face_recognizer = cv2.createEigenFaceRecognizer()
        elif self.faceRecognizer == 1:
            face_recognizer = cv2.createFisherFaceRecognizer()
        elif self.faceRecognizer == 2:
            face_recognizer = cv2.createLBPHFaceRecognizer()
        print "Training..."
        startTimeB = time.time()
        face_recognizer.train(faces, np.array(labels))
        endTimeB = time.time()
        print "Fininished training!"
        #return the trained recognizer
        print "Training time: " + str(endTimeB - startTimeB)  
        return face_recognizer
    
    def draw_rectangle(self, image, rect):
        #adds a rectangle to an image (around the face)
        (x, y, w, h) = rect
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
    def draw_text(self, image, text, x, y):
        #adds text to an image (hopefully over the face)
        cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    def predict(self, face_recognizer, the_image):
        image = the_image
        face, rect = self.detect_face(image)
        #Predict then get the name of the person
        if not face is None:
            resized_face = cv2.resize(face,(350,350))
            label = face_recognizer.predict(resized_face)
            db = database_manager() #access the database, to get the personal info
            first_name = db.get_value('"First Name"','Employees','ID', label[0])
            last_name = db.get_value('"Last Name"','Employees','ID', label[0])
            label_text = first_name[0][0] + " " + last_name[0][0]
            #Draw the rectangle and text on the image
            self.draw_rectangle(image, rect)
            self.draw_text(image, label_text, rect[0], rect[1]-5)      
            #return the image and the label
            return image, label
        else:
            #return the image and a zero if it was not returned already
            return image, [0]
            
    def justDetect(self, the_image):
        image = the_image
        face, rect = self.detect_face(image)
        #Predict then get the name of the person
        if not face is None:#Draw the rectangle and text on the image
            #Draw the rectangle and text on the image
            self.draw_rectangle(image, rect)
            self.draw_text(image, " ", rect[0], rect[1]-5)  
            #return the image and a zero if it was not returned already
            return image
        else:
            #return the image and a zero if it was not returned already
            return image