import potatoChip as ptt
import time
import matplotlib.pyplot as plt
import numpy as np

class abby: #in memorial of Abigail Nordwall who persisted through hours of MiniProject2
    def __init__(self):
        self.dev=ptt.Potato()
        self.cycles=20
        self.AC=18
        self.c=0
        self.angle=0

    def damper(self):
        time_axis = [];
        anglelist = [];
        angle=0
        angle2=0
        force=0
        diff=0
        t=0
        self.dev.turn_on_en();
        angle2=self.dev.get_angle()
        self.dev.set_duty(0);
        while(t<80000):
            angle=self.dev.get_angle()
            diff=angle-angle2
            angle2=angle
            diff=abs(diff)
            force=np.interp(diff,[10,15000],[0,100])
            if (diff<15000 and diff>10):
                if(dir()):
                    self.dev.turn_right_dir();
                    self.dev.set_duty(force);
                elif(not dir()):
                    self.dev.turn_left_dir();
                    self.dev.set_duty(force);
            t=t+1
            time_axis.append(diff/6);
            anglelist.append(force);
        self.dev.turn_off_en()
        plt.plot(time_axis, anglelist);
        plt.title('Angular Velocity vs Friction');
        plt.xlabel('Friction (pwm)');
        plt.ylabel('Angular velocity (rad/s)');
        plt.show();

    def spring(self):
        #initialising variables
        time_axis = [];
        anglelist = [];
        start_time = time.time();
        current_time=0;
        t=0
        loading=True
        release=0
        force=0
        angle2=0
        angle1=0
        prev_angle1=0
        diff=0
        first= True;
        offset=self.dev.get_angle()/16354*self.AC; #makes the starting position always 0
        while(t<15000):     #roughly 15sec
            if (first):     #just for the first instance to get the first prev_angle1
                angle1=self.dev.get_angle()/16354*self.AC
                angle2=self.dev.get_angle()/16354*self.AC
                diff =angle2-angle1
                if (self.dir()):
                    if(diff<-(self.AC-4)):
                        self.c=self.c+1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                else:
                    if(diff>(self.AC-4)):
                        self.c=self.c-1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                first=False
                prev_angle1=angle1;
            else:
                angle1=self.dev.get_angle()/16354*self.AC
                diff =angle1-prev_angle1
                if (self.dir()):
                    if(diff<-(self.AC-4)):
                        self.c=self.c+1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                else:
                    if(diff>(self.AC-4)):
                        self.c=self.c-1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                prev_angle1=angle1;
            print(self.angle) #we want to make sure the friction drive aint slipping
            if(loading==True): #creates the opposing force during the extension of a spring
                if(self.angle<180 and self.angle>2):
                    self.dev.turn_on_en()
                    self.dev.turn_right_dir()
                    force=np.interp(self.angle,[2,180],[1,80])
                    self.dev.set_duty(force)
                    print('loading')
                if(prev_angle1-angle1>1):
                    loading=False
                    release=self.angle #saves the release angle
                    print('release')
            elif(abs(self.angle)>abs(release*0.5)and self.angle*release<0):
                self.dev.turn_off_pwm()
                if (abs(self.angle)>abs(release*0.7) and self.angle*release<0):
                    self.dev.turn_on_en()
                    force=force*0.7 #damping factor of 0.7 can be changed
                    release=release*0.7
                    if (dir()):
                        self.dev.turn_right_dir()
                        self.dev.set_duty(force)
                    elif(not dir()):
                        self.dev.turn_left_dir()
                        self.dev.set_duty(force)
            current_time = time.time();
            relative_time = current_time-start_time;
            relative_time = round(relative_time,2);
            time_axis.append(relative_time);
            anglelist.append(self.angle);
            t=t+1
        plt.plot(time_axis, anglelist);
        plt.title('Angle vs Time');
        plt.xlabel('Time (s)');
        plt.ylabel('Angle(degrees)');
        plt.show();

    def texture(self,friction,slip): #from 0 to 100
        time_axis = [];
        anglelist = [];
        start_time = time.time();
        current_time=0;
        t=0
        angle2=0
        angle1=0
        prev_angle1=0
        diff=0
        first= True;
        offset=self.dev.get_angle()/16354*self.AC;
        while(t<15000):
            if (first):
                angle1=self.dev.get_angle()/16354*self.AC
                angle2=self.dev.get_angle()/16354*self.AC
                diff =angle2-angle1
                if (self.dir()):
                    if(diff<-(self.AC-4)):
                        self.c=self.c+1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                else:
                    if(diff>(self.AC-4)):
                        self.c=self.c-1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                first=False
                prev_angle1=angle1;
            else:
                angle1=self.dev.get_angle()/16354*self.AC
                diff =angle1-prev_angle1
                if (self.dir()):
                    if(diff<-(self.AC-4)):
                        self.c=self.c+1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                else:
                    if(diff>(self.AC-4)):
                        self.c=self.c-1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                prev_angle1=angle1;
            print(self.angle)
            if(self.angle<70and self.angle>20):
                self.dev.turn_on_en()
                self.dev.turn_right_dir()
                self.dev.set_duty(friction)
                print("there's so much friction!!!")
            if(self.angle<170 and self.angle>120):
                self.dev.turn_on_en()
                self.dev.turn_left_dir()
                self.dev.set_duty(slip)
                print("oops i slipped") #so we know we slipped
            else:
                self.dev.set_duty(0)
                self.dev.turn_off_en()
                print("simply smooth")
            t=t+1
            current_time = time.time();
            relative_time = current_time-start_time;
            relative_time = round(relative_time,2);
            time_axis.append(relative_time);
            anglelist.append(self.angle);
        plt.plot(time_axis, anglelist);
        plt.title('Angle vs Time');
        plt.xlabel('Time (s)');
        plt.ylabel('Angle(degrees)');
        plt.show();




    def wall(self): #WORKS WELL
        time_axis = [];
        anglelist = [];
        start_time = time.time();
        current_time=0;
        t=0
        angle2=0
        angle1=0
        prev_angle1=0
        diff=0
        first= True;
        offset=self.dev.get_angle()/16354*self.AC;
        while(t<15000):
            if (first):
                angle1=self.dev.get_angle()/16354*self.AC
                angle2=self.dev.get_angle()/16354*self.AC
                diff =angle2-angle1
                if (self.dir()):
                    if(diff<-(self.AC-4)):
                        self.c=self.c+1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                else:
                    if(diff>(self.AC-4)):
                        self.c=self.c-1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                first=False
                prev_angle1=angle1;
            else:
                angle1=self.dev.get_angle()/16354*self.AC
                diff =angle1-prev_angle1
                if (self.dir()):
                    if(diff<-(self.AC-4)):
                        self.c=self.c+1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                else:
                    if(diff>(self.AC-4)):
                        self.c=self.c-1
                    self.angle=self.dev.get_angle()/16354*self.AC + self.c*self.AC - offset
                prev_angle1=angle1;
            print(self.angle)
            if(self.angle<180 and self.angle>150):
                self.dev.turn_on_en()
                self.dev.turn_right_dir()
                self.dev.set_duty(100)
                print("i hit a wall")
            if(self.angle<-90 and self.angle>-120):
                self.dev.turn_on_en()
                self.dev.turn_left_dir()
                self.dev.set_duty(100)
                print("i hit a wall")
            else:
                self.dev.set_duty(0)
                self.dev.turn_off_en()
                print("im blind and im walking")
            t=t+1
            current_time = time.time();
            relative_time = current_time-start_time;
            relative_time = round(relative_time,2);
            time_axis.append(relative_time);
            anglelist.append(self.angle);
        plt.plot(time_axis, anglelist);
        plt.title('Angle vs Time');
        plt.xlabel('Time (s)');
        plt.ylabel('Angle(degrees)');
        plt.show();

    def dir(self): #returns 1 if direction is anticlockwise and 0 if it is clockwise
        first = True
        while(1):
            if (first):
                r1=self.dev.get_angle()
                r2=self.dev.get_angle()
                if (abs(r2-r1)<8):
                    pass
                elif((r2>r1 or r1>r2+10000)and not r2>r1+10000): #increasing
                    return 1
                else:
                    return 0
                first = False
                pr1=r1
            else:
                r1=self.dev.get_angle()

                if(abs(pr1-r1)<8):
                    return 'stat'
                elif((r1>pr1 or pr1>r1+10000) and not r1>pr1+10000): #increasing
                    return 1
                else:
                    return 0
                pr1=r1
