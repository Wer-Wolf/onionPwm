import onionPwm as pwm
import time

# Dont forget enabling the pwm0 pin!
# (docs.onion.io/omega2-docs/generating-pwm-signals.html -> Enabling PWM Pins)

led = pwm.OnionPwm(0)   # Initialize PWM channel 0 (GPIO 18)
led.setFrequency(1000)  # Set the Frequency of PWM channel 0 to 1000 Hz
led.setDutyCycle(50)    # Set the duty cycle of PWM channel 0 to 50%
led.enable()    # Enables PWM channel 0 --> LED turns on
print('Wait 5 seconds, look at the LED')
time.sleep(5)

led.setDutyCycle(100)   # Set the duty cycle of PWM channel 0 to 100%
print('Wait 5 seconds, look at the LED again')
time.sleep(5)

led.disable()   # Disables PWM channel 0 --> LED turns off
