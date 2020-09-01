# **onionPwm**



## **Description:**

```import onionPwm```

Since Omega firmware build 195, the Omega2 family supports up to 4 oboard PWM channels through the linux /sys interface.
However, unlike the PWM Expansion Board, there was no Python 3 compatible library for interfacing with these channels.
The onionPwm library does fix this problem by providing easy access to the PWM channels.

## **Features:**

* Change the frequency and duty cycle of each PWM channel (*See* **Usage**)

* Provides methods to enable/disable each PWM channel (*See* **Usage**)

* Context manager support

* Python 3 compatible

## **Usage:**

### Initialize a PWM channel: ###

```channel = onionPwm.OnionPwm( channel , chip=0 , force=False )```

* If the PWM channel specified with ```channel``` does not exist, you will get ```OSError: [Errno 19] No such device```

* If the PWM chip specified with ```chip``` does not exist, you will get ```FileNotFoundError```

* ```force = True``` ignores if the corresponding PWM chnnel is busy. Useful if the previous user forgot to call release(), but may lead to errors if the channel is still in use.

* When not using a context manager, call ```release()``` at the end to release the PWM channel 

### Change the frequency of a PWM channel: ###

```channel.set_frequency( frequency in Hz )```

* If the choosen frequency is not supported by the PWM chip, you will get ```Permission Error: [Errno 1] Operation not permitted```

```channel.get_frequency()``` --> frequency in Hz

***The result may slightly vary from the value set with setFrequency() due to rounding***

### Change the period of a PWM channel: ###

```channel.set_period( period in ns )```

* Similar to ```set_frequency()```, but instead accepts values in ns

* If ```period``` is zero or negative, you will get ```OSError: [Errno 22] Invalid argument```

* When ```period``` is smaller than the current channel duty cycle, you will get ```OSError: [Errno 22] Invalid argument```

***Please use setFrequency() instead of setPeriod() for normal operation***

```channel.get_period()``` --> Period in ns

* Similar to ```get_frequency()```, but instead returns values in ns

### Change the duty cycle of a PWM channel: ###

```channel.set_duty_cycle( dutyCycle in percent )```

* When no frequency is set, ```set_cycle``` and ```get_duty_cycle()``` will always set/report
```channel.get_duty_cycle()``` --> duty cycle in percent

```channel.set_cycle( cycle in ns )```

* Similar to ```set_duty_cycle()```, but instead accepts values in ns

* When ```cycle``` is negative, you will get ```OSError: [Errno 22] Invalid argument```

* When ```cycle``` is greater than the current channel period, you will get ```OSError: [Errno 22] Invalid argument```

***Please use setDutyCycle() instead of setCycle() for normal operation***

```channel.get_cycle()``` --> duty cycle in ns

* Similar to ```get_duty_cycle()```, but instead returns values in ns

***The result may slightly vary from the value set with setDutyCycle() due to rounding***

### Enable/disable a PWM channel: ###

```channel.enable()```

```channel.disable()```

* enable / disable the channel

```is_enabled()``` --> True or False

### Hint: ###

* ```onionPwm.toNsec( frequency in Hz )``` converts a frequency in Hz into the corresponding period in ns

* ```onionPwm.toHz( period in ns )``` converts a period in ns into the corresponding frequency in Hz

## **Supports:**

* Python 3.5+

## **License:**
This project is licensed under the LGPL License - see the [LICENSE](LICENSE) file for details

## **Authors:**

* **Armin W.** [Wer-Wolf](https://github.com/Wer-Wolf)

## **Acknowledgments:**

* Read the [Article](https://docs.onion.io/omega2-docs/generating-pwm-signals.html) about the PWM on how to enabling the corresponding PWM pins