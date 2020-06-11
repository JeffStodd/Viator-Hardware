import cv2

def main():
	cam = cv2.VideoCapture("http://192.168.1.176:8081/")
	r,f = cam.read()
	cv2.imwrite("snapshot.jpg",f)

def snapshot():
	cam = cv2.VideoCapture("http://192.168.1.176:8081/")
	r,f = cam.read()
        cv2.imwrite("snapshot.jpg",f)
	return f

if __name__ == "__main__":
	main()
