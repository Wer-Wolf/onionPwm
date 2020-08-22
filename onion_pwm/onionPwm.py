import os.path

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


def toNsec(inHz: float) -> int:
    if inHz <= 0:
        raise ValueError('frequency is zero or negative')
    inNsec = int((1 / inHz) * 1e+9)  # Period in nanoseconds (1000000000ns = 1s)
    # Rounding is necessary since float numbers are not supported
    if inNsec == 0:
        raise ValueError('Frequency too high')
    return inNsec


def toHz(inNsec: float) -> float:
    if inNsec != 0:  # To avoid division exception
        inHz = 1 / (inNsec / 1e+9)  # Frequency in Hz
    else:
        inHz = 0.0
    return inHz


class OnionPwm:
    def __init__(self, channel: int, chip: int = 0, force: bool = False) -> None:
        self.path = PWM_PATH % chip
        if not os.path.isdir(self.path):
            raise ValueError('Chip unknown')
        if (self.getMaxChannels() - 1) < channel:
            raise ValueError('Channel unknown')  # Channel exceeds max. channel number
        self.channelPath = self.path + '/' + PWM_CHANNEL_PATH % channel
        self.channelNumber = channel   # Necessary for export/unexport
        if os.path.isdir(self.channelPath):
            if force is False:  # Only use force = True if the corresponding PWM channel is not in use!
                raise RuntimeError('Device busy')   # PWM channel is already exported (in use)
                # Not using a context manager and not calling release() may also cause this
                # If this is the case, use force = True to force release the channel
        else:
            self._exportChannel()   # Do release() or use a context manager!
        self.periodFile = self.channelPath + '/' + PWM_CHANNEL_PERIOD_FILE
        self.cycleFile = self.channelPath + '/' + PWM_CHANNEL_DUTY_CYCLE_FILE
        self.enableFile = self.channelPath + '/' + PWM_CHANNEL_ENABLE_FILE

    def __enter__(self):
        return self

    def __exit__(self, exceptionType, exceptionValue, traceback) -> bool:
        self._unexportChannel()
        return False

    def _exportChannel(self) -> None:
        with open(self.path + '/' + PWM_EXPORT_FILE, 'w') as fd:
            fd.write(str(self.channelNumber))

    def _unexportChannel(self) -> None:
        with open(self.path + '/' + PWM_UNEXPORT_FILE, 'w') as fd:
            fd.write(str(self.channelNumber))

    def getMaxChannels(self) -> int:
        with open(self.path + '/' + PWM_CHANNELS_FILE, 'r') as fd:
            maxChannels = int(fd.read())
        return maxChannels

    def setPeriod(self, period: int):
        if period <= 0:
            raise ValueError('Invalid value for period')
        with open(self.periodFile, 'w') as fd:
            fd.write(str(period))

    def getPeriod(self) -> int:
        with open(self.periodFile, 'r') as fd:
            period = int(fd.read())
        return period

    def setCycle(self, cycle: int):
        if cycle < 0:
            raise ValueError('Duty cycle is negative')
        with open(self.cycleFile, 'w') as fd:
            fd.write(str(cycle))

    def getCycle(self) -> int:
        with open(self.cycleFile, 'r') as fd:
            cycle = int(fd.read())
        return cycle

    def setFrequency(self, frequency: float):  # Frequency in Hz
        channelPeriod = toNsec(frequency)
        currentPeriod = self.getPeriod()
        if currentPeriod != 0:  # Not first access after reset
            with open(self.cycleFile, 'r+') as fd:
                currentCycle = int(fd.read())
                fd.write('0')   # To avoid OsError later due duty_cycle > period
            newCycle = int((channelPeriod / currentPeriod) * currentCycle)  # Necessary to adjust duty cycle to new period
            self.setPeriod(channelPeriod)
            self.setCycle(newCycle)
        else:   # Do not adjust duty_cycle
            self.setPeriod(channelPeriod)

    def getFrequency(self) -> float:  # Result may slightly vary from the value set with setFrequency() due to rounding
        channelPeriod = self.getPeriod()
        frequency = toHz(channelPeriod)
        return frequency

    def setDutyCycle(self, dutyCycle: float):  # Value between 0 and 100 (75.5 -> 75.5 %)
        if dutyCycle > 100 or dutyCycle < 0:
            raise ValueError('dutyCycle exceeds value range')
        channelPeriod = self.getPeriod()
        if channelPeriod != 0:   # Period set
            channelCycle = int(channelPeriod * (dutyCycle / 100))    # Duty cyle in nanoseconds, rounding is necessary
            self.setCycle(channelCycle)
        # Else the new duty cycle whould equal 0

    def getDutyCycle(self) -> float:
        channelPeriod = self.getPeriod()
        channelCycle = self.getCycle()
        if channelPeriod != 0:  # Period set
            dutyCycle = (channelCycle / channelPeriod) * 100    # Result may slight vary from the value set with setDutyCycle() due to rounding
        else:
            dutyCycle = 0.0
        return dutyCycle

    def getStatus(self) -> str:
        with open(self.enableFile, 'r') as fd:
            status = fd.read()
        if status.strip() == '1':
            return 'enabled'
        else:
            return 'disabled'

    def enable(self):
        if self.getPeriod() == 0:
            raise RuntimeError('No frequency set')
        if self.getStatus() != 'enabled':
            with open(self.enableFile, 'w') as fd:
                fd.write('1')

    def disable(self):
        if self.getStatus() != 'disabled':
            with open(self.enableFile, 'w') as fd:
                fd.write('0')

    def release(self):  # Dont use with a context manager!
        self._unexportChannel()
