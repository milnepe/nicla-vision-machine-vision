# rock_detect.py - By: Pete Milne - Wed Nov 9 2022

import sensor, image, time, os, tf, pyb

redLED = pyb.LED(1) # built-in red LED
greenLED = pyb.LED(2) # built-in green LED

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

labels, net = tf.load_builtin_model('rock_detection')
found = False

def flashLED(led): # Indicate with LED when target is detected
    found = True
    led.on()
    pyb.delay(3000)
    led.off()
    found = False

clock = time.clock()

while not found:
    clock.tick()

    img = sensor.snapshot()

    # default settings just do one detection... change them to search the image...
    for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
        img.draw_rectangle(obj.rect())
        # This combines the labels and confidence values into a list of tuples
        predictions_list = list(zip(labels, obj.output()))

        for i in range(len(predictions_list)):
            confidence = predictions_list[i][1]
            label = predictions_list[i][0]
            print("%s = %f" % (label, confidence))

            if confidence > 0.8:
                if label == "rock":
                    print("It's a ROCK-4SE")
                    flashLED(greenLED)
                if label == "rock-5":
                    print("It's a ROCK-5B")
                    flashLED(redLED)

    print(clock.fps(), "fps")
