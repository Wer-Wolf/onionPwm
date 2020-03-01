# **onionPwm**



## **Description:**

Since Omega firmware build 195, the Omega2 family supports up to 4 oboard PWM channels through the linux /sys interface.
However, unlike the PWM Expansion Board, there was no Python 3 compatible library for interfacing with these channels.
The onionPwm library does fix this problem by providing easy access to the PWM channels.

## **Features:**

* Change the frequency and duty cycle of each PWM channel (*See* **Usage**)

* Provides methods to enable/disable each PWM channel (*See* **Usage**)

* Python 3 compatible

## **Usage:**

### Initialize a PWM channel:**

```channel = onionPwm.OnionPwm( channel , chip = 0 )```

* If the PWM chip specified with ```chip``` does not exist, you will get ```ValueError('Chip unknown')```

* If the PWM channel specified with ```channel``` does not exist, you will get ```ValueError('Channel unknown')```

### Change the frequency of a PWM channel:**

```channel.setFrequency( frequency in Hz )```

* Negative values or the value 0 for ```frequency``` will raise ```ValueError('frequency needs to be greater than 0')```

* Values for ```frequency``` which are too small will raise ```ValueError('Frequency too low')```

* When the corresponding PWM channel is already exported, you will get ```OSError: [Errno 16] Resource busy```. Call ```channel._unexportChannel()``` and try again

* If the choosen frequency is not supported by the PWM chip, you will get ```Permission Error: [Errno 1] Operation not permitted```

```channel.getFrequency()``` --> frequency in Hz

*** The result may slightly vary from the value set with setFrequency() due to rounding ***

* When the corresponding PWM channel is already exported, you will get ```OSError: [Errno 16] Resource busy```. Call ```channel._unexportChannel()``` and try again

### Change the duty cycle of a PWM channel:**

```channel.setDutyCycle( dutyCycle in percent )```

* Values above 100 or under 0 for ```dutyCycle``` will raise ```ValueError('dutyCycle exceeds max. of 100 or min. of 0(%)')```

* When the corresponding PWM channel is already exported, you will get ```OSError: [Errno 16] Resource busy```. Call ```channel._unexportChannel()``` and try againc

```channel.getDutyCycle()``` --> duty cycle in percend

*** The result may slightly vary from the value set with setDutyCycle() due to rounding ***

* When the corresponding PWM channel is already exported, you will get ```OSError: [Errno 16] Resource busy```. Call ```channel._unexportChannel()``` and try again

### Enable/disable a PWM channel:**

```channel.enable()```

* When the corresponding PWM channel is already exported, you will get ```OSError: [Errno 16] Resource busy```. Call ```channel._unexportChannel()``` and try againc

```channel.disable()```

* When the corresponding PWM channel is already exported, you will get ```OSError: [Errno 16] Resource busy```. Call ```channel._unexportChannel()``` and try again

## **Supports:**

* Python 3

## **License:**
This project is licensed under the LGPL License - see the [LICENSE](LICENSE) file for details

## **Authors:**

* **Armin W.** [Wer-Wolf](https://github.com/Wer-Wolf)

## **Acknowledgments:**

* Read the [Article](https://docs.onion.io/omega2-docs/generating-pwm-signals.html) about the PWM on how to enabling the corresponding PWM pins