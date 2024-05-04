from flask import Flask, render_template, Response
import cv2
import RPi.GPIO as GPIO
import time
from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
from pygame import mixer


app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
in1_pin=10
in2_pin=9
in3_pin = 27
in4_pin = 22
GPIO.setwarnings(False)

GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)


# Set up PWM for the motor control pins
pwm1 = GPIO.PWM(in1_pin, 100)  # 100 Hz frequency
pwm2 = GPIO.PWM(in3_pin, 100)  # 100 Hz frequency

def turn_on_motor():
    pwm1.start(25)  # 50% duty cycle (adjust as needed)
    pwm2.start(25)  # 50% duty cycle (adjust as needed)

def turn_off_motor():
    pwm1.stop()
    pwm2.stop()

# Specify your preferred resolution and framerate here
resolution = (256,144)
framerate = 60


# Initialize the OpenCV video capture
cap = cv2.VideoCapture(0)

# Initialize the camera with specified resolution and framerate
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
cap.set(cv2.CAP_PROP_FPS, framerate)

mixer.init()

illusion_sound = mixer.Sound("/home/admin/illusion.wav")
sleep_sound = mixer.Sound("/home/admin/sleep.wav")

thresh = 0.25
frame_check = 20
closed_eyes_timer = 0  
open_eyes_timer = 0 
illusion_sound_playing = False 
sleep_sound_playing = False 

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def gen():
    closed_eyes_timer = 0  
    open_eyes_timer = 0 

    while True:
        # Capture frame-by-frame
        success, frame = cap.read()
        if not success:
            break

        # Resize the frame
        frame = imutils.resize(frame, width=256
                           )
        frame = cv2.flip(frame,1
                         )

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)

        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear >= thresh:
                flag = 0
                open_eyes_timer += 1
                closed_eyes_timer = 0
            else:
                flag = 0
                closed_eyes_timer += 1
                open_eyes_timer = 0

        # Decision for "illusion" based on open eyes
        if open_eyes_timer > 1 * frame_check and not illusion_sound_playing:
            illusion_sound.play(-1) 
            illusion_sound_playing = True
            turn_on_motor()
        elif open_eyes_timer <= 1 * frame_check:
            illusion_sound.stop()
            illusion_sound_playing = False

        # Decision for "sleep" based on closed eyes
        if closed_eyes_timer > 1 * frame_check and not sleep_sound_playing:
            sleep_sound.play(-1)
            sleep_sound_playing = True
            turn_on_motor()
        elif closed_eyes_timer <= 1 * frame_check:
            sleep_sound.stop()  
            sleep_sound_playing = False

        if not illusion_sound_playing and not sleep_sound_playing:
            turn_off_motor()

        # Encode the frame in JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)

        # Convert the frame to bytes
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index.html')  # you can customize index.html here

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    detect = dlib.get_frontal_face_detector()
    predictor_path = "/home/admin/shape_predictor_68_face_landmarks.dat"
    predict = dlib.shape_predictor(predictor_path)

    app.run(host='0.0.0.0', debug=False)

    # Release the video capture object when the app is closed
    cap.release()
