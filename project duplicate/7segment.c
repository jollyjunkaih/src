#include "elecanisms.h"
#define digit1 D1
#define digit2 D2
#define digit3 D3
#define digit4 D4
#define segA D5
#define segB D6
#define segC D7
#define segD D8
#define segE D9
#define segF D10
#define segG D11

int counter=0;
int num1,num2,num3,num4;
bool digit2_iszero,digit3_iszero

void displaynum(int num)
{
  switch number
  {
    case 1:
    {
      segB=HIGH;
      segC=HIGH;
      segA=LOW;
      segD=LOW;
      segE=LOW;
      segF=LOW;
      segG=LOW;
      break;
    }
    case 2:
    {
      segA=HIGH;
      segB=HIGH;
      segG=HIGH;
      segE=HIGH;
      segD=HIGH;
      segF=LOW;
      segC=LOW;
      break;
    }
    case 3:
    {
      segA=HIGH;
      segB=HIGH;
      segG=HIGH;
      segC=HIGH;
      segD=HIGH;
      segF=LOW;
      segE=LOW;
      break;
    }
    case 4:
    {
      segB=HIGH;
      segG=HIGH;
      segF=HIGH;
      segC=HIGH;
      segA=LOW;
      segD=LOW;
      segE=LOW;
      break;
    }
    case 5:
    {
      segA=HIGH;
      segF=HIGH;
      segG=HIGH;
      segC=HIGH;
      segD=HIGH;
      segB=LOW;
      segE=LOW;
      break;
    }
    case 6:
    {
      segF=HIGH;
      segC=HIGH;
      segG=HIGH;
      segE=HIGH;
      segD=HIGH;
      segA=LOW;
      segB=LOW;
      break;
    }
    case 7:
    {
      segA=HIGH;
      segB=HIGH;
      segC=HIGH;
      segD=LOW;
      segE=LOW;
      segF=LOW;
      segG=LOW;
      break;
    }
    case 8:
    {
      segA=HIGH;
      segB=HIGH;
      segC=HIGH;
      segD=HIGH;
      segE=HIGH;
      segF=HIGH;
      segG=HIGH;
      break;
    }
    case 9:
    {
      segA=HIGH;
      segB=HIGH;
      segC=HIGH;
      segD=LOW;
      segE=LOW;
      segF=HIGH;
      segG=HIGH;
      break;
    }
    case 0:
    {
      segA=HIGH;
      segB=HIGH;
      segC=HIGH;
      segD=HIGH;
      segE=HIGH;
      segF=HIGH;
      segG=LOW;
      break;
    }
    case 10:
    {
      segA=LOW;
      segB=LOW;
      segC=LOW;
      segD=LOW;
      segE=LOW;
      segF=LOW;
      segG=LOW;
      break;
    }
  }
}

void main(void)
{
  init_elecanisms();
  T1CON=0x0030;
  PR1=0x1869;
  TMR1=0;

  D1_DIR = OUT;
  D2_DIR = OUT;
  D3_DIR = OUT;
  D4_DIR = OUT;
  D5_DIR = OUT;
  D6_DIR = OUT;
  D7_DIR = OUT;
  D8_DIR = OUT;
  D9_DIR = OUT;
  D10_DIR = OUT;
  D11_DIR = OUT;

  T1CONbits.TON=1;
  while(1)
  {
    IFS0bits.T1IF=0;
    int digit;
    for(digit=1;digit<=4;digit++)
    {
      switch digit
      {
        case 1:
        if(counter>999)
        {
          digit1=HIGH;
          displaynum(counter/1000);
          int interm;
          interm=counter%1000
          while(IFS0bits.T1IF==0)
          {

          }
          if(interm<100)
          {
            digit2_iszero=true;
            if(interm<10)
            {
              digit3_iszero=true;
            }
            else
            {
              digit3_iszero=false;
            }
          }
          else
          {
            digit2_iszero=false;
          }
        }
        break

        case 2:
        if(digit2_iszero)
        {
          digit2=HIGH;
          displaynum(0);
          IFS0bits.T1IF=0;
          while(IFS0bits.T1IF==0)
          {

          }
        }
        if(digit3_iszero)
        {
          break;
        }
        if(interm>99&&interm<1000)
        {
          digit2=HIGH;
          displaynum(interm/100);
          interm%=100;
          IFS0bits.T1IF=0;
          while(IFS0bits.T1IF==0)
          {

          }
          if(interm<10)
          {
            digit3_iszero=true;
          }
          else
          {
            digit3_iszero=false;
          }
        }

        case 3:
        if(digit3_iszero)
        {
          digit3=HIGH;
          displaynum(0);
          IFS0bits.T1IF=0;
          while(IFS0bits.T1IF==0)
          {

          }
          break;
        }
        if(interm>9&&interm<100)
        {
          digit3=HIGH;
          displayn  um(interm/10);
          interm %=10'
          IFS0bits.T1IF=0;
          while(IFS0bits.T1IF==0)
          {

          }
        }
        break;

        case 4:
        digit4=HIGH;
        displaynum(interm);
        IFS0bits.T1IF=0;
        while(IFS0bits.T1IF==0)
        {

        }
        break;
      }
      displaynum(10);
      digit1=LOW;
      digit2=LOW;
      digit3=LOW;
      digit4=LOW;
    }
    counter++;
  }
}
