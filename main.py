from website import create_app
from flask import Flask,render_template,request
import pickle
from keras.models import load_model
import os.path
import h5py
import os
import numpy as np
from PIL import Image
import cv2 as cv
from keras.preprocessing.image import img_to_array, load_img

app=create_app()

def preprocess_image(image, target_size):
    image = img_to_array(image)
    image = image.resize(target_size)
    image = np.expand_dims(image, axis=0)
    print("YES yes YEs YES YEs YES ")
    return image

model=load_model("Diabeitc_model_new.h5")
@app.route('/predict',methods=['POST'])
def predict():
    img1=request.files['img1']
    print(img1)
    image_path="C:/Users/Bobby/Desktop/Diabetic Ratinopathy Website - Version2/website/testimage/"+img1.filename
    img1.save(image_path)
    print(type(img1))
    image=load_img(image_path,target_size=(266,400))
    image=img_to_array(image)
    print(image)
    print(image.shape)
    image = np.expand_dims(image, axis=0)
    #processed_image=image.reshape((1,image.shape[0],image.shape[1],image.shape[2]))
    #processed_image = preprocess_image(img1, target_size=(224, 224))
    prediction = model.predict(image)
    print(prediction)
    response=[]
    response.append( {
        'prediction': {
            'No_DR': (prediction[0][2])*100,
            'Mild': prediction[0][1]*100,
            'Moderate':prediction[0][4]*100,
            'Severe':prediction[0][3]*100,
            'Proliferate_DR':prediction[0][0]*100
        }
    })

    img2=request.files['img2']
    print(img2)
    image_path2="C:/Users/Bobby/Desktop/Diabetic Ratinopathy Website - Version2/website/testimage/"+img2.filename
    img2.save(image_path2)
    print(type(img2))
    image2=load_img(image_path2,target_size=(266,400))
    image2=img_to_array(image2)
    print(image2)
    print(image2.shape)
    image2 = np.expand_dims(image2, axis=0)
    #processed_image=image.reshape((1,image.shape[0],image.shape[1],image.shape[2]))
    #processed_image = preprocess_image(img1, target_size=(224, 224))
    prediction = model.predict(image2)
    print(prediction)
    response.append( {
        'prediction': {
            'No_DR': prediction[0][2]*100,
            'Mild': prediction[0][1]*100,
            'Moderate':prediction[0][4]*100,
            'Severe':prediction[0][3]*100,
            'Proliferate_DR':prediction[0][0]*100
        }
    })
    print(response)
    return render_template('predict.html',pred1=response[0]['prediction']['No_DR'],
    pred2=response[0]['prediction']['Mild'],
    pred3=response[0]['prediction']['Moderate'],
    pred4=response[0]['prediction']['Severe'],
    pred5=response[0]['prediction']['Proliferate_DR'],
    pred6=response[1]['prediction']['No_DR'],
    pred7=response[1]['prediction']['Mild'],
    pred8=response[1]['prediction']['Moderate'],
    pred9=response[1]['prediction']['Severe'],
    pred10=response[1]['prediction']['Proliferate_DR'])
    # return render_template('test.html')
if __name__=='__main__':
    app.run(debug=True)
