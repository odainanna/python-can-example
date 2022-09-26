#!/usr/bin/env python
# coding: utf-8

# ## python-can-demo

# In[1]:


get_ipython().system('pip install python-can uptime')
# or use !pip install python-can<4 uptime for v3 since v4 is under development


# ((Or see instructions at: https://python-can.readthedocs.io/en/master/index.html))

# ## Setup to use with PCAN-Usb Pro

# In[2]:


import can
import time


# In[3]:


config = {'interface': 'pcan', 'bitrate': 125000}
can.rc.update(config)


# ## List all available channels.

# In[4]:


can.detect_available_configs('pcan')


# ## Connect to a bus, then flash the lights for 10 seconds

# In[5]:


with can.Bus(channel="PCAN_USBBUS1") as  bus:    
    print(f'{bus.status_string()=}')
    
    # display device number
    print(f'{bus.get_device_number()=}')
    
    # flash the lights on the device 
    bus.flash(True)
    time.sleep(10)
    bus.flash(False)
    
    # get the internal device number 
    print(f'{bus.get_device_number()}')
    
    # change the internal device number to something useful (like the number taped on the back of the device)
    # bus.set_device_number(20277) 
    # print(f'{bus.get_device_number()}')
    


# ## Send and receive a single message

# In[6]:


with can.Bus(channel="PCAN_USBBUS1") as  bus_a, can.Bus(channel="PCAN_USBBUS2") as bus_b:
    try:
        message = can.Message(arbitration_id=15)
        bus_a.send(message)
        print(f'Sent {repr(message)} on {bus_a.channel_info}')
    except can.CanError:
        print("NOT sent")
        
    received_msg = bus_b.recv()
    print('Received', repr(received_msg), 'on', bus_b.channel_info)
    


# ## Send mulitiple messsages and attach a listener/notifier

# In[7]:


with can.Bus(channel="PCAN_USBBUS1") as  bus_a, can.Bus(channel="PCAN_USBBUS2") as bus_b:
    print(f'{bus_a.status_string()=}, {bus_b.status_string()=}')
    notify =  can.Notifier(bus_b, [can.Printer()])
    
    for i in range(5):
        # send a couple of messages
        bus_a.send(can.Message(data=[i] * 3))
        
    
    # give the notifier some time to notify
    time.sleep(2)
    notify.stop()


# See can.interfaces.pcan.pcan.

# ## Accessing the PCAN Basic API from Peak
# Pyton-can acts as a higher-level wrapper around the lower-level but official PCAN Basic API from Peak. All the methods from the Peak API are accessible thorugh here. 

# In[8]:


from pprint import pprint
with can.Bus(channel="PCAN_USBBUS1") as  bus, can.Bus(channel="PCAN_USBBUS2") as  bus_2:
    
    print(bus.get_api_version())
    print('The backend:', type(bus.m_objPCANBasic).__name__)
    print('...', help(bus.m_objPCANBasic))


# In[9]:


help(bus.m_objPCANBasic)


# In[ ]:





# In[ ]:




