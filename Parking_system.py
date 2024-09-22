import RPi.GPIO as gpio
import time
import LCD1602 as lcd

IRpin = 22 
LCDpin = 23 
ECHO = 17
TRIG = 18

def setup():
    gpio.setmode(gpio.BCM)
    gpio.setup(IRpin, gpio.IN)
    gpio.setup(LCDpin, gpio.OUT)
    gpio.setup(ECHO, gpio.IN)
    gpio.setup(TRIG, gpio.OUT)

def distance():
    gpio.output(TRIG, gpio.LOW) 
    time.sleep(0.000002)
    gpio.output(TRIG, gpio.HIGH)  
    time.sleep(0.00001)
    gpio.output(TRIG, gpio.LOW)
    while gpio.input(ECHO) == 0:
        pass
    time1 = time.time()
    while gpio.input(ECHO) == 1:
        pass
    time2 = time.time()
    value = time2 - time1 
    return value * 340 / 2 * 100 

def lcd_show(distance, detected):
    lcd.init(0x27, 1) 
    lcd.write(0, 0, f"Rastojanje:{distance:.1f}")
    lcd.write(0, 1, str(detected))
    time.sleep(0.5)

def detected():
    ir_value = gpio.input(IRpin) 
    if ir_value == 1:
        gpio.output(LCDpin, gpio.LOW)
        return 'Bezbedno' 
    else:
        gpio.output(LCDpin, gpio.HIGH)
        return 'Stop' 

def main():
    while True:
        dis = distance()
        detec = detected()
        lcd_show(dis,detec)
        print(f'Rastojanje: {dis:.3f}')
        print(f'Prepreka: {detec:}')

def destroy():
    gpio.cleanup()

if __name__ == '__main__':
    try:
        setup()
        main()
    except KeyboardInterrupt:
        destroy()