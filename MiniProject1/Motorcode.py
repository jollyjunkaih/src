
import Spindown as spin
import time
import matplotlib.pyplot as plt

class Motor:

     def __init__(self):
        self.dev = spin.Spindown();

     def get_angle(self):
        angle = self.dev.get_angle();
        print(angle);

     def turn_motor_on(self):
        self.dev.toggle_d7_en();

     def spinmotor(self):
        self.dev.toggle_d5_pwm();
        self.dev.toggle_d6_dir();
        time.sleep(3);

        step = 0;
        time_axis = [];
        anglelist = [];
        start_time = time.time();

        while step < 10000:
            step += 1;
            current_time = time.time();
            relative_time = current_time-start_time;
            relative_time = round(y,2);
            list.append(relative_time);
            angle = self.dev.get_angle();
            angle_degrees = (angle/43.9);
            angle_degrees_rounded = round(angle_degrees, 2);
            anglelist.append(angle_degrees_rounded)

        plt.plot(time_axis, anglelist);
        plt.title('Angle vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Angle(degrees)')
        plt.show();
