import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('watch.jpg')[...,::-1]/255.0
noise =  np.random.normal(loc=0, scale=1, size=img.shape)

# noise overlaid over image
noisy = np.clip((img + noise*0.075),0,1)
noisy2 = np.clip((img + noise*0.095),0,1)

# noise multiplied by image:
# whites can go to black but blacks cannot go to white
noisy1mul = np.clip((img*(1 + noise*0.28)),0,1)
noisy2mul = np.clip((img*(1 + noise*0.32)),0,1)

# noise multiplied by bottom and top half images,
# whites stay white blacks black, noise is added to center
img2 = img*2
n1 = np.clip(np.where(img2 <= 1, (img2*(1 + noise*0.25)), (1-img2+1)*(1 + noise*0.25)*-1 + 2)/2, 0,1)
n2 = np.clip(np.where(img2 <= 1, (img2*(1 + noise*0.35)), (1-img2+1)*(1 + noise*0.35)*-1 + 2)/2, 0,1)


# norm noise for viz only
noise2 = (noise - noise.min())/(noise.max()-noise.min())
plt.figure(figsize=(20,20))
plt.imshow(np.vstack((np.hstack((img, noise2)),
                      np.hstack((noisy, noisy2)),
                      np.hstack((noisy1mul, noisy2mul)),
                      np.hstack((n1, n2)))))
plt.show()
#plt.hist(noise.ravel(), bins=100)
#plt.show()
plt.close()