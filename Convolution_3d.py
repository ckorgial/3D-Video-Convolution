# 3D VIDEO CONVOLUTION FROM SCRATCH 

# AUTHOR: CHRISTOS KORGIALAS

import numpy as np
import cv2
import skvideo.io

def myConv3D(A, B, param):
	# Parameters
	stride = param['stride']
	pad = param['pad']

	# Size of A and B arrays
	xA = A.shape[1]
	yA = A.shape[2]
	zA = A.shape[0]
    
	xB = B.shape[1]
	yB = B.shape[2] 
	zB = B.shape[0]
    
	# Shape of output convolution
	xOutput = int(((xA - xB + 2 * pad) / stride) + 1)
	yOutput = int(((yA - yB + 2 * pad) / stride) + 1)
	zOutput = int(((zA - zB + 2 * pad) / stride) + 1)
	output = np.zeros((zOutput, xOutput, yOutput), np.uint8)

	for z in range(zA):
# 		if z > zA - zB: # Step size is the same with the stride
# 			break
		if z % stride == 0: # End of z dimension
			for y in range(yA):
# 				if y > yA - yB:  # End of y dimension
# 					break
				if y % stride == 0:  # Step size is the same with the stride
					for x in range(xA):
# 						if x > xA - xB:  # End of x dimension
# 							break
						try:
							if x % stride == 0:  # Step size is the same with the stride
								output[z, x, y] = (B * A[z:z + zB, x:x + xB, y:y + yB]).sum()  # Convolution
						except:
							break
	print(output.shape)
	print(output)
	return output  # Return the output of the convolution

def create_smooth_kernel(size):
	kernel = np.zeros((size, size, size))
	kernel.fill(1 / (size ** 3))
	print(kernel.shape)
	print(kernel)
	return kernel  # Kernel (B)

def pad_image(A, size):
	padded_A = np.zeros((A.shape[0] + (size - 1), A.shape[1] + (size - 1), A.shape[2] + (size - 1)), np.uint8)  # Array of zeros
	padded_A[(size // 2):-(size // 2), (size // 2):-(size // 2), (size // 2):-(size // 2)] = A  # Replace the zeros with video elements
	print(padded_A.shape)
	print(padded_A)
	return padded_A  # Padded (A)

def videogray(video):
	cap = cv2.VideoCapture(video)  # Load video file
	total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in the video
	fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per Second
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Width of video frames
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Height of video frames
	codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # Codec for the output video
	output_video = cv2.VideoWriter('video_gray.mp4', codec, fps, (width, height), 0)  # Create the output video
	for f in range(0, total_frames):  # Iterate through all video frames
		ret, frame = cap.read()  # Read frame
		if ret == False:
			break
		# Make it Gray
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# Write output video
		output_video.write(frame_gray)

def main():
	videogray('video.mp4')
	video = skvideo.io.vread('video_gray.mp4')
	print(video.shape)
	video = video[:, :, :, 0]
	video = video.reshape((video.shape[0], video.shape[1], video.shape[2]))
	print(video.shape)
	kernel_size = 3  # Size of the kernel
	kernel = create_smooth_kernel(kernel_size)  # Create the kernel
	param = {'stride': 1, 'pad': 1}  # Parameters
	# Apply zero padding to all sides
	padded_video = pad_image(video, kernel_size)
	# Apply convolution
	convolution_video = myConv3D(padded_video, kernel, param)
	# Write output video
	skvideo.io.vwrite('outputvideo.mp4', convolution_video)



if __name__ == "__main__":
    main()
