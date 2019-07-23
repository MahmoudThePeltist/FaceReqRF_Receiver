import cv2
import time
import os
import sys
import numpy as np
from SQLiteDBClass import *
from PIL import Image

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
        self.takeValue = 250
        self.prototxt = "training-data/deepDetection/deploy.prototxt.txt"
        self.model = "training-data/deepDetection/res10_300x300_ssd_iter_140000.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        
    def detect_face(self, image):
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #get grayscale image
        #face detection using lbp cascade classifier
        if self.faceDetector == 0:
            trainerLocation = self.localDir + '/training-data/haarcascades/haarcascade_frontalface_alt.xml'
        elif self.faceDetector == 1:
            trainerLocation = self.localDir + '/training-data/lbpcascades/lbpcascade_frontalface_improved.xml'
        elif self.faceDetector == 2:
            startX, startY, endX, endY = self.deepDetect(image)
            if startX + startY + endX + endY == 0:
                return None, None
            return grayscale_image[startY:endY, startX:endX], [startX,startY,endX - startX,endY - startY]
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
                try:
                    cv2.imshow("Editing image...", image)
                except:
                    print "Could not show image: ", image_name
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
                image = cv2.imread(image_path)
                #cv2.waitKey(10)
                try:
                    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                except:
                    grayscale_image = image
                print "Adding: " + image_path + " @ " + str(label)
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
            face_recognizer = cv2.face.EigenFaceRecognizer_create()
            self.takeValue = 25000
        elif self.faceRecognizer == 1:
            face_recognizer = cv2.face.FisherFaceRecognizer_create()
            self.takeValue = 2500
        elif self.faceRecognizer == 2:
            face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.takeValue = 250
        print "Training..."
        startTimeB = time.time()
        face_recognizer.train(faces, np.array(labels))
        #find location to save appropriate XML recognizer file
        save_location = self.localDir + "/training-data/trained_" + str(self.faceRecognizer) + "_recognizer.xml"        
        print "Saving file at: " + save_location        
        face_recognizer.save(save_location)
        endTimeB = time.time()
        print "Fininished training!"
        #return the trained recognizer
        print "Training time: " + str(endTimeB - startTimeB)  
        return face_recognizer
    
    def draw_rectangle(self, image, rect):
        #adds a rectangle to an image (around the face)
        (x, y, w, h) = rect
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    def load_recognizer(self, faceRecognizer):
        #set the recognizer
        if faceRecognizer == 0:
            face_recognizer = cv2.face.EigenFaceRecognizer_create()
            self.takeValue = 15000
        elif faceRecognizer == 1:
            face_recognizer = cv2.face.FisherFaceRecognizer_create()
            self.takeValue = 1500
        elif faceRecognizer == 2:
            face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.takeValue = 150
        #find the location of the saved file and return it if it exists
        save_location = self.localDir + "/training-data/trained_" + str(faceRecognizer) + "_recognizer.xml"                
        print "Searching for saved XML training file at " + save_location
        if os.path.exists(save_location):
            print "..file found: " + save_location
            face_recognizer.read(save_location)
            return face_recognizer
        else:
            print "..file not found"
            return None 
 
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
            #try to print the user's data if they exist in the database
            try:
                first_name = db.get_value('"First Name"','Employees','ID', label[0])
                last_name = db.get_value('"Last Name"','Employees','ID', label[0])
                label_text = first_name[0][0] + " " + last_name[0][0] + " %" + str(self.takeValue - int(label[1]))
            except:
                label_text = "Error ID" + str(label[0]) + " not in database!"
            #Draw the rectangle and text on the image
            self.draw_rectangle(image, rect)
            self.draw_text(image, label_text, rect[0], rect[1]-5)      
            #return the image and the label
            return image, label
        else:
            #return the image and a zero if it was not returned already
            return image, (0,0)
            
    def justDetect(self, image):
        #face detection using lbp cascade classifier
        if self.faceDetector == 0:
            trainerLocation = self.localDir + '/training-data/haarcascades/haarcascade_frontalface_alt.xml'
        elif self.faceDetector == 1:
            trainerLocation = self.localDir + '/training-data/lbpcascades/lbpcascade_frontalface_improved.xml'
        elif self.faceDetector == 2:
            image = self.deepJustDetect(image)
            return image
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #get grayscale image
        cascade_classifier = cv2.CascadeClassifier(trainerLocation)
        faces = cascade_classifier.detectMultiScale(grayscale_image, scaleFactor=1.2, minNeighbors=5);     
        #check if there are any faces
        if not faces is None:
            for face in faces:#go over the faces in the image
                #Draw the rectangle and text on the face
                self.draw_rectangle(image, face)
                self.draw_text(image, " ", face[0], face[1]-5)
            return image
        else:
            #return the image if there are no faces
            return image
            
    def deepDetect(self, image):
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        # pass the blob through the network and obtain the detections and predictions
        self.net.setInput(blob)
        detections = self.net.forward()
        confidence = detections[0, 0, 0, 2]
        if confidence > 0.5:
            box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            #return the face only
            return startX, startY, endX, endY
        else:
            return 0,0,0,0
        
    def deepJustDetect(self, image):
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
         
        # pass the blob through the network and obtain the detections and predictions
        self.net.setInput(blob)
        detections = self.net.forward()
        
        # loop over the detections
        for i in range(0, detections.shape[2]):
        	# extract the confidence (i.e., probability) associated with the prediction
        	confidence = detections[0, 0, i, 2]
         
        	# filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
        	if confidence > 0.5:
        		# compute the (x, y)-coordinates of the bounding box for the object
        		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        		(startX, startY, endX, endY) = box.astype("int")
         
        		# draw the bounding box of the face along with the associated probability
        		text = "{:.2f}%".format(confidence * 100)
        		y = startY - 10 if startY - 10 > 10 else startY + 10
        		cv2.rectangle(image, (startX, startY), (endX, endY),
        			(0, 0, 255), 2)
        		cv2.putText(image, text, (startX, y),
        			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        return image