import cv2
import os
import datetime
from config import parse

vid = cv2.VideoCapture(0)
config = parse()


def clear_directory():
	print(f"Cleaning {len(os.listdir(config.images_folder))} files")
	if os.system(f"rm {config.images_folder}/*.png") == 32512:
		os.system(fr"del /S {config.images_folder}\*")
	print("Done!")


def record_video(t: float = 15):
	cv2.imshow('frame', vid.read()[1])
	amount = len(os.listdir(config.images_folder))
	while(amount <= t * config.target_fps):
		_, frame = vid.read()

		cv2.imwrite(f'{config.images_folder}{os.sep}frame_{amount}.png', frame)
		print(f"Captured frame {amount}")
		cv2.imshow('frame', frame)
		amount += 1

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	print(f"Captured {amount - 1} frames")


def generate_video(): 
	image_folder = f'{os.pardir}{os.sep}{config.images_folder}'
	os.chdir(config.output_folder)
	video_name = f'{str(datetime.datetime.now())}.avi'

	images = sorted([img for img in os.listdir(image_folder) if img.endswith(".png")], 
					key=lambda x: int(x[6:-4]))

	print(images)  

	frame = cv2.imread(os.path.join(image_folder, images[0])) 

	height, width, _ = frame.shape   

	video = cv2.VideoWriter(video_name, 0, config.target_fps, (width, height))  

	# Appending the images to the video one by one 
	for image in images:  
		video.write(cv2.imread(os.path.join(image_folder, image)))

	video.release()  # releasing the video generated
	os.chdir(f"{os.pardir}")


try:
	while True:
		clear_directory()
		record_video(config.time)
		generate_video()
except KeyboardInterrupt:
	vid.release()
	cv2.destroyAllWindows()
