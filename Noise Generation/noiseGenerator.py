import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

def add_gaussian_noise(img):
    mean=28
    var=100
    sigma=var**0.5
    gaussian=np.random.normal(mean,sigma,(img.shape[0],img.shape[1]))
    noise_img=np.zeros(img.shape,dtype=np.float32)
    
    noise_img[:,:,0]=img[:,:,0]+gaussian
    noise_img[:,:,1]=img[:,:,1]+gaussian
    noise_img[:,:,2]=img[:,:,2]+gaussian
    cv2.normalize(noise_img,noise_img,0,255,cv2.NORM_MINMAX,dtype=-1)
    noise_img=noise_img.astype(np.uint8)
    return noise_img

img=cv2.imread('watch.jpg',cv2.IMREAD_COLOR)

print(img.shape,img.dtype)

noise=add_gaussian_noise(img)

plt.figure(figsize=(8,10))
plt.imshow(np.hstack((img,noise)))
plt.savefig('E:/Denoising/Results/noiseGenerator.pdf')
plt.show()
plt.close()
