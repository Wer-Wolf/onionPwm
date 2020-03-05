# **onionPwm**



## **Description:**

Since Omega firmware build 195, the Omega2 family supports up to 4 oboard PWM channels through the linux /sys interface.
However, unlike the PWM Expansion Board, there was no Python 3 compatible library for interfacing with these channels.
The onionPwm library does fix this problem by providing easy access to the PWM channels.

## **Features:**

* Change the frequency and duty cycle of each PWM channel (*See* **Usage**)

* Provides methods to enable/disable each PWM channel (*See* **Usage**)

* Context manager support

* Python 3 compatible

## **Usage:**

### Initialize a PWM channel:**

```channel = onionPwm.OnionPwm( channel , chip = 0 , force = False)```

* If the PWM channel specified with ```channel``` does not exist, you will get ```ValueError('Channel unknown')```

* If the PWM chip specified with ```chip``` does not exist, you will get ```ValueError('Chip unknown')```

* ```force = True``` ignores if the corresponding PWM chnnel is busy. Good if the previeous user forgot to call release(), but may lead to random crashes if the channel is still in use.

* When not using a context manager, call ```release()``` at the end to release the PWM channel 

### Change the frequency of a PWM channel:**

```channel.setFrequency( frequency in Hz )```

* Negative values or the value 0 for ```frequency``` will raise ```ValueError('frequency needs to be greater than 0')```

* Values for ```frequency``` which are too small will raise ```ValueError('Frequency too low')```

* If the choosen frequency is not supported by the PWM chip, you will get ```Permission Error: [Errno 1] Operation not permitted```

```channel.getFrequency()``` --> frequency in Hz

***The result may slightly vary from the value set with setFrequency() due to rounding***

### Change the period of a PWM channel: ###

```channel.setPeriod( period in ns )```

* Similar to ```setFrequency()```, but instead accepts values in ns

* If ```period``` is zero or negative, you will get ```ValueError('Invalid value for period')```

```channel.getPeriod()``` --> Period in ns

* Similar to ```getFrequency()```, but instead returns values in ns

### Change the duty cycle of a PWM channel:**

```channel.setDutyCycle( dutyCycle in percent )```

* Values above 100 or under 0 for ```dutyCycle``` will raise ```ValueError('dutyCycle exceeds value range')```

* When no frequency is set, ```setDutyCycle``` and ```getDutyCycle()``` will always set/report 0

```channel.getDutyCycle()``` --> duty cycle in percend

```channel.setCycle( cycle in ns )```

* Similar to ```setDutyCycle()```, but instead accepts values in ns

* When ```cycle``` is negative, you will get ```ValueError('Duty cycle is negative')```

```channel.getCycle()``` --> duty cycle in ns

* Similar to ```getDutyCycle()```, but instead returns values in ns

***The result may slightly vary from the value set with setDutyCycle() due to rounding***

### Enable/disable a PWM channel:**

```channel.enable()```

* Please do ```setFrequency()``` before enabling a PWM channel, else you will get ```OSError: [Errno 22] Invalid argument```

```channel.disable()```

* Please do ```enable()``` before disabling a PWM channel, else you will get ```OSError: [Errno 22] Invalid argument```

### Hint: ###

* ```onionPwm.toNsec( frequency in Hz )``` converts a frequency in Hz into the corresponding period in ns

* ```onionPwm.toHz( period in ns )``` converts a period in ns into the corresponding frequency in Hz

## **Supports:**

* Python 3

## **License:**
This project is licensed under the LGPL License - see the [LICENSE](LICENSE) file for details

## **Authors:**

* **Armin W.** [Wer-Wolf](https://github.com/Wer-Wolf)

## **Acknowledgments:**

* Read the [Article](https://docs.onion.io/omega2-docs/generating-pwm-signals.html) about the PWM on how to enabling the corresponding PWM pins