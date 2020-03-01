import os.path

# Path definitions
PWM_BASE_PATH = '/sys/class/pwm'
PWM_PATH = PWM_BASE_PATH + '/pwmchip%d' # Add number of pwm chip (pwmchip0)

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
#PWM_CHANNEL_POLARITY_FILE = 'polarity'

__version__ = '1.1'

# Before using this library, make sure to enable the corresponding PWM pins
# (docs.onion.io/omega2-docs/generating-pwm-signals.html -> Enabling PWM Pins)

class OnionPwm:
    def __init__(self, channel, chip = 0):    # Accepts a pwm channel-number and a pwm chip-number as integer
            if not os.path.isdir(PWM_PATH % chip):
                raise ValueError('Chip unknown')
            self.path = PWM_PATH % chip
            if (self.getMaxChannels() - 1) < channel:
                raise ValueError('Channel unknown') # Channel exceeds max. channel number
            self.channelNumber = channel   # Necessary for export/unexport
            self.channelPath = self.path + '/' + PWM_CHANNEL_PATH % channel
            self.periodFile = self.channelPath + '/' + PWM_CHANNEL_PERIOD_FILE
            self.cycleFile = self.channelPath + '/' + PWM_CHANNEL_DUTY_CYCLE_FILE
            self.enableFile = self.channelPath + '/' + PWM_CHANNEL_ENABLE_FILE

    def _exportChannel(self):
        with open(self.path + '/' + PWM_EXPORT_FILE, 'w') as fd:
            fd.write(str(self.channelNumber))

    def _unexportChannel(self):
        with open(self.path + '/' + PWM_UNEXPORT_FILE, 'w') as fd:
            fd.write(str(self.channelNumber))

    def getMaxChannels(self):
        with open(self.path + '/' + PWM_CHANNELS_FILE, 'r') as fd:
            maxChannels = int(fd.read())
        return maxChannels

    def setFrequency(self, frequency):  # Frequency in Hz
        if frequency <= 0:
            raise ValueError('frequency needs to be greater than 0')
        channelPeriod = int((1 / frequency) * 1e+9)  # Period in nanoseconds (1000000000ns = 1s)
        # Rounding is necessary since point numbers are not supported
        if channelPeriod == 0:
            raise ValueError('Frequency too low')
        self._exportChannel()
        try:
            with open(self.periodFile, 'r') as fd:
                currentPeriod = int(fd.read())
            if currentPeriod != 0:  # Not first access after reset
                with open(self.cycleFile, 'r+') as fd:
                    currentCycle = int(fd.read())
                    fd.write('0')   # To avoid OsError later due duty_cycle > period
                newCycle = int((channelPeriod / currentPeriod) * currentCycle)  # Necessary to adjust duty cycle to new period
                with open(self.periodFile, 'w') as fd:
                    fd.write(str(channelPeriod))
                with open(self.cycleFile, 'w') as fd:
                    fd.write(str(newCycle))
            else:   # Do not adjust duty_cycle
                with open(self.periodFile, 'w') as fd:
                    fd.write(str(channelPeriod))
        finally:
            self._unexportChannel() # Unexports channel even if an exception occurs

    def getFrequency(self): # Result may slightly vary from the value set with setFrequency() due to rounding
        self._exportChannel()
        try:
            with open(self.periodFile, 'r') as fd:
                channelPeriod = int(fd.read())
        finally:
            self._unexportChannel() # Unexports channel even if an exception occurs
        if channelPeriod != 0:  # Period set
            frequency = 1 / (channelPeriod / 1e+9)  # Frequency in Hz
        else:
            frequency = 0
        return frequency

    def setDutyCycle(self, dutyCycle):  # Value between 0 and 100 as float (75.5 -> 75.5 %)
        if dutyCycle > 100 or dutyCycle < 0:
            raise ValueError('dutyCycle exceeds max. of 100 or min. of 0(%)')
        self._exportChannel()
        try:
            with open(self.periodFile, 'r') as fd:
                channelPeriod = int(fd.read())  # Read period first
            if channelPeriod != 0:   # Period set
                channelCycle = int(channelPeriod * (dutyCycle / 100))    # Duty cyle in nanoseconds, rounding is necessary
                with open(self.cycleFile, 'w') as fd:
                    fd.write(str(channelCycle))
            # Else the new duty cycle whould equal 0

        finally:
            self._unexportChannel() # Unexports channel even if an exception occurs

    def getDutyCycle(self):
        self._exportChannel()
        try:
            with open(self.periodFile, 'r') as fd:
                channelPeriod = int(fd.read())
            with open(self.cycleFile, 'r') as fd:
                channelCycle = int(fd.read())
        finally:
            self._unexportChannel() # Unexports channel even if an exception occurs
        if channelPeriod != 0:  # Period set
            dutyCycle = (channelCycle / channelPeriod) * 100    # Result may slight vary from the value set with setDutyCycle() due to rounding
        else:
            dutyCycle = 0
        return dutyCycle

    def enable(self):
        self._exportChannel()
        try:
            with open(self.enableFile, 'w') as fd:
                fd.write('1')
        finally:
            self._unexportChannel() # Unexports channel even if an exception occurs

    def disable(self):
        self._exportChannel()
        try:
            with open(self.enableFile, 'w') as fd:
                fd.write('0')
        finally:
            self._unexportChannel() # Unexports channel even if an exception occurs
