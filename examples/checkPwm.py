import onionPwm as pwm

# Dont forget enabling the pwm0 pin!
# (docs.onion.io/omega2-docs/generating-pwm-signals.html -> Enabling PWM Pins)

with pwm.OnionPwm(channel=0) as led:  # Initialize PWM channel 0 (GPIO 18)
    led.set_frequency(1000)  # Set the Frequency of PWM channel 0 to 1000 Hz
    led.set_duty_cycle(0)    # Set the duty cycle of PWM channel 0 to 0%
    led.enable()    # Enables PWM channel 0 --> LED stays off
    try:
        while 1:
            newCycle = input('Enter duty cycle (0 - 100) or EXIT: ')
            if newCycle == 'EXIT':
                break
            else:
                led.set_duty_cycle(float(newCycle))   # Changes the duty cycle of PWM channel 0
                print('Current duty cycle: %3.10f' % led.get_duty_cycle())
                print('As you can see, there might be some slight difference due to rounding')
    finally:
        led.disable()
