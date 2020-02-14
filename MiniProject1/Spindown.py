
import usb.core
import time

class Spindown:

    def __init__(self):
        self.TOGGLE_LED1 = 0
        self.TOGGLE_LED2 = 1
        self.TOGGLE_LED3 = 2
        self.READ_SW1 = 3
        self.READ_SW2 = 4
        self.READ_SW3 = 5
        self.ENC_READ_REG = 6
        self.TOGGLE_D5_PWM = 7
        self.TOGGLE_D6_DIR = 8
        self.TOGGLE_D7_EN = 9
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

    def toggle_d5_pwm(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_D5_PWM)
        except usb.core.USBError:
            print("Could not send TOGGLE_D5_PWM vendor request.")

    def toggle_d6_dir(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_D6_DIR)
        except usb.core.USBError:
            print("Could not send TOGGLE_D6_DIR vendor request.")

    def toggle_d7_en(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_D7_EN)
        except usb.core.USBError:
            print("Could not send TOGGLE_D7_EN vendor request.")
