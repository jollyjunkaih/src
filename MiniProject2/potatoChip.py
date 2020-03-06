
import usb.core
import time

class Potato:

    def __init__(self):
        self.SET_DUTY_VAL = 1
        self.GET_DUTY_VAL = 2
        self.GET_DUTY_MAX = 3
        self.ENC_READ_REG = 4
        self.TURN_OFF_PWM = 5
        self.TURN_ON_PWM = 6
        self.TURN_LEFT_DIR = 7
        self.TURN_RIGHT_DIR = 8
        self.TURN_OFF_EN = 9
        self.TURN_ON_EN = 10
        self.dev = usb.core.find(idVendor = 0x6666, idProduct = 0x0003)
        if self.dev is None:
            raise ValueError('no USB device found matching idVendor = 0x6666 and idProduct = 0x0003')
        self.dev.set_configuration()

# AS5048A Register Map
        self.ENC_NOP = 0x0000
        self.ENC_CLEAR_ERROR_FLAG = 0x0001
        self.ENC_PROGRAMMING_CTRL = 0x0003
        self.ENC_OTP_ZERO_POS_HI = 0x0016
        self.ENC_OTP_ZERO_POS_LO = 0x0017
        self.ENC_DIAG_AND_AUTO_GAIN_CTRL = 0x3FFD
        self.ENC_MAGNITUDE = 0x3FFE
        self.ENC_ANGLE_AFTER_ZERO_POS_ADDER = 0x3FFF

    def close(self):
        self.dev = None

    def get_angle(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.ENC_READ_REG, 0x3FFF, 0, 2)
        except usb.core.USBError:
            print("Could not send ENC_READ_REG vendor request.")
        else:
            return (int(ret[0]) + 256 * int(ret[1])) & 0x3FFF

    def turn_on_pwm(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TURN_ON_PWM) #this is the function that tells us to send
        except usb.core.USBError:                            #the type of mode we want to send it and also
            print("Could not send TOGGLE_D5_PWM vendor request.") # the command we want to send

    def turn_off_pwm(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TURN_OFF_PWM) #this is the function that tells us to send
        except usb.core.USBError:                            #the type of mode we want to send it and also
            print("Could not send TOGGLE_D5_PWM vendor request.") # the command we want to send

    def turn_left_dir(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TURN_LEFT_DIR)
        except usb.core.USBError:
            print("Could not send TOGGLE_D6_DIR vendor request.")

    def turn_right_dir(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TURN_RIGHT_DIR)
        except usb.core.USBError:
            print("Could not send TOGGLE_D6_DIR vendor request.")

    def turn_on_en(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TURN_ON_EN)
        except usb.core.USBError:
            print("Could not send TOGGLE_D7_EN vendor request.")
    def turn_off_en(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TURN_OFF_EN)
        except usb.core.USBError:
            print("Could not send TOGGLE_D7_EN vendor request.")

    def set_duty_val(self, val):
        try:
            self.dev.ctrl_transfer(0x40, self.SET_DUTY_VAL, val)
        except usb.core.USBError:
            print("Could not send SET_DUTY_VAL vendor request.")

    def get_duty_val(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.GET_DUTY_VAL, 0, 0, 2)
        except usb.core.USBError:
            print("Could not send GET_DUTY_VAL vendor request.")
        else:
            return int(ret[0]) + 256 * int(ret[1])

    def get_duty_max(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.GET_DUTY_MAX, 0, 0, 2)
        except usb.core.USBError:
            print("Could not send GET_DUTY_MAX vendor request.")
        else:
            return int(ret[0]) + 256 * int(ret[1])

    def set_duty(self, duty_cycle):
        val = int(round(duty_cycle * self.get_duty_max() / 100.))
        self.set_duty_val(val)

    def get_duty(self):
        return 100. * self.get_duty_val() / self.get_duty_max()
