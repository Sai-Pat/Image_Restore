import cv2
from django.http import StreamingHttpResponse

def gen_frames():
    camera = cv2.VideoCapture(0)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (ex, ey, ew, eh) in eyes:
                # Draw magic glowing circle around eyes
                center = (ex + ew//2, ey + eh//2)
                radius = int(round((ew + eh)*0.25))
                cv2.circle(frame, center, radius, (255, 183, 178), 3) # Pastel pink
                cv2.circle(frame, center, radius+5, (199, 206, 234), 1) # Pastel purple glow
                
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def eye_tracking_stream(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
