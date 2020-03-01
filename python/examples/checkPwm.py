import onionPwm as pwm

# Dont forget enabling the pwm0 pin!
# (docs.onion.io/omega2-docs/generating-pwm-signals.html -> Enabling PWM Pins)

led = pwm.OnionPwm(0)   # Initialize PWM channel 0 (GPIO 18)
led.setFrequency(1000)  # Set the Frequency of PWM channel 0 to 1000 Hz
led.setDutyCycle(0)    # Set the duty cycle of PWM channel 0 to 0%
led.enable()    # Enables PWM channel 0 --> LED stays off
while 1:
    newCycle = input('Enter duty cycle (0 - 100) or EXIT')
    if newCycle  is 'EXIT':
        break
    else:
        led.setDutyCycle(float(newCycle))   # Changes the duty cycle of PWM channel 0
        print('Current duty cycle: %3.10f', led.getDutyCycle())
        print('As you can see, there is some slight difference due to rounding')
led.disable()
