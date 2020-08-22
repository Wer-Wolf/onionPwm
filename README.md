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

* If the PWM channel specified with ```channel``` does not exist, you will get ```ValueError('Channel unknown')```

* If the PWM chip specified with ```chip``` does not exist, you will get ```ValueError('Chip unknown')```

* ```force = True``` ignores if the corresponding PWM chnnel is busy. Useful if the previeous user forgot to call release(), but may lead to random crashes if the channel is still in use.

* When not using a context manager, call ```release()``` at the end to release the PWM channel 

### Change the frequency of a PWM channel: ###

```channel.setFrequency( frequency in Hz )```

* Negative values or the value 0 for ```frequency``` will raise ```ValueError('frequency needs to be greater than 0')```

* Values for ```frequency``` which are too high will raise ```ValueError('Frequency too high')```

* If the choosen frequency is not supported by the PWM chip, you will get ```Permission Error: [Errno 1] Operation not permitted```

```channel.getFrequency()``` --> frequency in Hz

***The result may slightly vary from the value set with setFrequency() due to rounding***

### Change the period of a PWM channel: ###

```channel.setPeriod( period in ns )```

* Similar to ```setFrequency()```, but instead accepts values in ns

* If ```period``` is zero or negative, you will get ```ValueError('Invalid value for period')```

* When ```period``` is smaller than the current channel duty cycle, you will get ```OSError: [Errno 22] Invalid argument```

***Please use setFrequency() instead of setPeriod() for normal operation***

```channel.getPeriod()``` --> Period in ns

* Similar to ```getFrequency()```, but instead returns values in ns

### Change the duty cycle of a PWM channel: ###

```channel.setDutyCycle( dutyCycle in percent )```

* Values above 100 or under 0 for ```dutyCycle``` will raise ```ValueError('dutyCycle exceeds value range')```

* When no frequency is set, ```setDutyCycle``` and ```getDutyCycle()``` will always set/report 0

```channel.getDutyCycle()``` --> duty cycle in percend

```channel.setCycle( cycle in ns )```

* Similar to ```setDutyCycle()```, but instead accepts values in ns

* When ```cycle``` is negative, you will get ```ValueError('Duty cycle is negative')```

* When ```cycle``` is greater than the current channel period, you will get ```OSError: [Errno 22] Invalid argument```

***Please use setDutyCycle() instead of setCycle() for normal operation***

```channel.getCycle()``` --> duty cycle in ns

* Similar to ```getDutyCycle()```, but instead returns values in ns

***The result may slightly vary from the value set with setDutyCycle() due to rounding***

### Enable/disable a PWM channel: ###

```channel.enable()```

```channel.disable()```

* When the corresponding PWM channel is already enabled/disabled, this methods wont have any function

```getStatus()``` --> 'enabled' or 'disabled'

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