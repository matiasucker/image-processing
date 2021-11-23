import cv2
import numpy as np

NCLUSTERS = 8
NROUNDS = 1

image = cv2.imread("resources/img4.png", cv2.IMREAD_COLOR)
height, width, channels = image.shape
samples = np.zeros([height * width, 3], dtype=np.float32)
count = 0

for x in range(height):
    for y in range(width):
        samples[count] = image[x][y]
        count += 1

compact, labels, centers = cv2.kmeans(samples,
                                      NCLUSTERS,
                                      None,
                                      (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 10000, 0.0001),
                                      NROUNDS,
                                      cv2.KMEANS_RANDOM_CENTERS)
print(centers)
centers = np.uint8(centers)
print(centers)
print(labels)
res = centers[labels.flatten()]
print(res)
image2 = res.reshape(image.shape)
print(image2)

cv2.imshow("k-means", image2)
cv2.imwrite("output/k-means.jpg", image2)

cv2.waitKey(0)
cv2.destroyAllWindows()
