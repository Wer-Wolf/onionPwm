#!/usr/bin/python3
from errno import EBUSY

# Path definitions
PWM_BASE_PATH = '/sys/class/pwm'
PWM_PATH = PWM_BASE_PATH + '/pwmchip%d'  # Add number of pwm chip (pwmchip0)

# Files and directorys found inside PWM_PATH
PWM_EXPORT_FILE = 'export'
PWM_UNEXPORT_FILE = 'unexport'
PWM_CHANNELS_FILE = 'npwm'
PWM_CHANNEL_PATH = 'pwm%d'  # Add number of pwm channel (pwm0)

# Files found inside of PWM_CHANNEL_PATH
PWM_CHANNEL_ENABLE_FILE = 'enable'  # Write 0 to disable PWM output, 1 to enable
PWM_CHANNEL_DUTY_CYCLE_FILE = 'duty_cycle'   # The time in nanoseconds when the PWM signal is asserted
PWM_CHANNEL_PERIOD_FILE = 'period'  # The time in nanoseconds of the entire PWM signal
# Write normal or inversed to control whether the asserted portion of the PWM signal is a logical high vs. a local low (not supported)
# PWM_CHANNEL_POLARITY_FILE = 'polarity'

# Before using this library, make sure to enable the corresponding PWM pins
# (docs.onion.io/omega2-docs/generating-pwm-signals.html -> Enabling PWM Pins)

__version__ = '2.1'
__author__ = 'Wer-Wolf'
__maintainer__ = 'Wer-Wolf'


def toNsec(inHz: float) -> int:
    if inHz <= 0:
        raise ValueError('frequency is zero or negative')
    inNsec = int((1 / inHz) * 1e+9)  # Period in nanoseconds (1000000000ns = 1s)
    # Rounding is necessary since float numbers are not supported
    if inNsec == 0:
        raise ValueError('Frequency too high')
    return inNsec


def toHz(inNsec: float) -> float:
    try:  # To avoid division exception
        inHz = 1 / (inNsec / 1e+9)  # Frequency in Hz
    except ZeroDivisionError:
        inHz = 0.0
    return inHz


class OnionPwm:     # https://www.kernel.org/doc/Documentation/pwm.txt
    def __init__(self, channel: int, chip: int = 0, force: bool = False) -> None:
        self.channel_number = channel   # Necessary for export/unexport
        path = PWM_PATH % chip
        self.export_file = '/'.join((path, PWM_EXPORT_FILE))
        self.unexport_file = '/'.join((path, PWM_UNEXPORT_FILE))
        self.channels_file = '/'.join((path, PWM_CHANNELS_FILE))
        channel_path = '/'.join((path, PWM_CHANNEL_PATH % channel))
        self.period_file = '/'.join((channel_path, PWM_CHANNEL_PERIOD_FILE))
        self.cycle_file = '/'.join((channel_path, PWM_CHANNEL_DUTY_CYCLE_FILE))
        self.enable_file = '/'.join((channel_path, PWM_CHANNEL_ENABLE_FILE))
        try:
            self._exportChannel()
        except OSError as err:
            if not (err.errno == EBUSY and force):  # hide exception if device is busy and force == True
                raise
            # Not using a context manager and not calling release() may also cause this
            # If this is the case, use force = True to force release the channel

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback) -> bool:
        self._unexportChannel()
        return False

    def _exportChannel(self) -> None:
        with open(self.export_file, 'w') as fd:
            fd.write(str(self.channel_number))

    def _unexportChannel(self) -> None:
        with open(self.unexport_file, 'w') as fd:
            fd.write(str(self.channel_number))

    def get_max_channels(self) -> int:
        with open(self.channels_file, 'r') as fd:
            return int(fd.read())

    def set_period(self, period: int) -> None:
        if period <= 0:
            raise ValueError('Invalid value for period')
        with open(self.period_file, 'w') as fd:
            fd.write(str(period))

    def get_period(self) -> int:
        with open(self.period_file, 'r') as fd:
            return int(fd.read())

    def set_cycle(self, cycle: int) -> None:
        with open(self.cycle_file, 'w') as fd:
            fd.write(str(cycle))

    def get_cycle(self) -> int:
        with open(self.cycle_file, 'r') as fd:
            return int(fd.read())

    def set_frequency(self, frequency: float) -> None:  # Frequency in Hz
        channelPeriod = toNsec(frequency)
        currentPeriod = self.get_period()
        if currentPeriod != 0:  # Not first access after reset
            with open(self.cycle_file, 'r+') as fd:
                currentCycle = int(fd.read())
                fd.write('0')   # To avoid OsError later due duty_cycle > period
            newCycle = int((channelPeriod / currentPeriod) * currentCycle)  # Necessary to adjust duty cycle to new period
            self.set_period(channelPeriod)
            self.set_cycle(newCycle)
        else:   # Do not adjust duty_cycle
            self.set_period(channelPeriod)

    def get_frequency(self) -> float:  # Result may slightly vary from the value set with setFrequency() due to rounding
        return toHz(self.get_period())

    def set_duty_cycle(self, dutyCycle: float) -> None:  # Value between 0 and 100 (75.5 -> 75.5 %)
        if dutyCycle > 100 or dutyCycle < 0:
            raise ValueError('dutyCycle exceeds value range')
        channelPeriod = self.get_period()
        if channelPeriod != 0:   # Period set
            self.set_cycle(int(channelPeriod * (dutyCycle / 100)))    # Duty cyle in nanoseconds, rounding is necessary
        # Else the new duty cycle whould equal 0

    def get_duty_cycle(self) -> float:
        channelPeriod = self.get_period()
        if channelPeriod != 0:  # Period set
            dutyCycle = self.get_cycle() / channelPeriod * 100    # Result may slight vary from the value set with setDutyCycle() due to rounding
        else:
            dutyCycle = 0.0
        return dutyCycle

    def is_enabled(self) -> bool:
        with open(self.enable_file, 'r') as fd:
            return fd.read().rstrip() == '1'

    def enable(self) -> None:
        with open(self.enable_file, 'w') as fd:
            fd.write('1')

    def disable(self) -> None:
        with open(self.enable_file, 'w') as fd:
            fd.write('0')

    def release(self) -> None:  # Dont use with a context manager!
        self._unexportChannel()
