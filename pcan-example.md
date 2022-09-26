## python-can-demo


```python
!pip install python-can uptime
# or use !pip install python-can<4 uptime for v3 since v4 is under development
```

    Requirement already satisfied: python-can in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (4.0.0)
    Requirement already satisfied: uptime in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (3.0.1)
    Requirement already satisfied: windows-curses in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (from python-can) (2.3.0)
    Requirement already satisfied: typing-extensions>=3.10.0.0 in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (from python-can) (4.3.0)
    Requirement already satisfied: packaging in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (from python-can) (21.3)
    Requirement already satisfied: wrapt~=1.10 in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (from python-can) (1.14.1)
    Requirement already satisfied: setuptools in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (from python-can) (63.2.0)
    Requirement already satisfied: pywin32 in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (from python-can) (304)
    Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in c:\users\odain\appdata\local\programs\python\python310\lib\site-packages (from packaging->python-can) (3.0.9)
    

((Or see instructions at: https://python-can.readthedocs.io/en/master/index.html))

## Setup to use with PCAN-Usb Pro


```python
import can
import time
```


```python
config = {'interface': 'pcan', 'bitrate': 125000}
can.rc.update(config)
```

## List all available channels.


```python
can.detect_available_configs('pcan')
```




    [{'interface': 'pcan', 'channel': 'PCAN_USBBUS1', 'supports_fd': True},
     {'interface': 'pcan', 'channel': 'PCAN_USBBUS2', 'supports_fd': True}]



## Connect to a bus, then flash the lights for 10 seconds


```python
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
    
```

    bus.status_string()='OK'
    bus.get_device_number()=20277
    20277
    

## Send and receive a single message


```python
with can.Bus(channel="PCAN_USBBUS1") as  bus_a, can.Bus(channel="PCAN_USBBUS2") as bus_b:
    try:
        message = can.Message(arbitration_id=15)
        bus_a.send(message)
        print(f'Sent {repr(message)} on {bus_a.channel_info}')
    except can.CanError:
        print("NOT sent")
        
    received_msg = bus_b.recv()
    print('Received', repr(received_msg), 'on', bus_b.channel_info)
    
```

    Sent can.Message(timestamp=0.0, arbitration_id=0xf, is_extended_id=True, dlc=0, data=[]) on PCAN_USBBUS1
    Received can.Message(timestamp=1664198212.2983868, arbitration_id=0xf, is_extended_id=True, dlc=0, data=[]) on PCAN_USBBUS2
    

## Send mulitiple messsages and attach a listener/notifier


```python
with can.Bus(channel="PCAN_USBBUS1") as  bus_a, can.Bus(channel="PCAN_USBBUS2") as bus_b:
    print(f'{bus_a.status_string()=}, {bus_b.status_string()=}')
    notify =  can.Notifier(bus_b, [can.Printer()])
    
    for i in range(5):
        # send a couple of messages
        bus_a.send(can.Message(data=[i] * 3))
        
    
    # give the notifier some time to notify
    time.sleep(2)
    notify.stop()
```

    bus_a.status_string()='OK', bus_b.status_string()='OK'
    Timestamp: 1664198212.677151    ID: 00000000    X Rx                DL:  3    00 00 00
    Timestamp: 1664198212.677951    ID: 00000000    X Rx                DL:  3    01 01 01
    Timestamp: 1664198212.678759    ID: 00000000    X Rx                DL:  3    02 02 02
    Timestamp: 1664198212.679567    ID: 00000000    X Rx                DL:  3    03 03 03
    Timestamp: 1664198212.680367    ID: 00000000    X Rx                DL:  3    04 04 04
    

See can.interfaces.pcan.pcan.

## Accessing the PCAN Basic API from Peak
Pyton-can acts as a higher-level wrapper around the lower-level but official PCAN Basic API from Peak. All the methods from the Peak API are accessible thorugh here. 


```python
from pprint import pprint
with can.Bus(channel="PCAN_USBBUS1") as  bus, can.Bus(channel="PCAN_USBBUS2") as  bus_2:
    
    print(bus.get_api_version())
    print('The backend:', type(bus.m_objPCANBasic).__name__)
    print('...', help(bus.m_objPCANBasic))
```

    4.6.1.728
    The backend: PCANBasic
    Help on PCANBasic in module can.interfaces.pcan.basic object:
    
    class PCANBasic(builtins.object)
     |  PCAN-Basic API class implementation
     |  
     |  Methods defined here:
     |  
     |  FilterMessages(self, Channel, FromID, ToID, Mode)
     |      Configures the reception filter
     |      
     |      Remarks:
     |        The message filter will be expanded with every call to this function.
     |        If it is desired to reset the filter, please use the 'SetValue' function.
     |      
     |      Parameters:
     |        Channel : A TPCANHandle representing a PCAN Channel
     |        FromID  : A c_uint value with the lowest CAN ID to be received
     |        ToID    : A c_uint value with the highest CAN ID to be received
     |        Mode    : A TPCANMode representing the message type (Standard, 11-bit
     |                  identifier, or Extended, 29-bit identifier)
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  GetErrorText(self, Error, Language=0)
     |      Configures or sets a PCAN Channel value
     |      
     |      Remarks:
     |      
     |        The current languages available for translation are:
     |        Neutral (0x00), German (0x07), English (0x09), Spanish (0x0A),
     |        Italian (0x10) and French (0x0C)
     |      
     |        The return value of this method is a 2-tuple, where
     |        the first value is the result (TPCANStatus) of the method and
     |        the second one, the error text
     |      
     |      Parameters:
     |        Error    : A TPCANStatus error code
     |        Language : Indicates a 'Primary language ID' (Default is Neutral(0))
     |      
     |      Returns:
     |        A tuple with 2 values
     |  
     |  GetStatus(self, Channel)
     |      Gets the current status of a PCAN Channel
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  GetValue(self, Channel, Parameter)
     |      Retrieves a PCAN Channel value
     |      
     |      Remarks:
     |        Parameters can be present or not according with the kind
     |        of Hardware (PCAN Channel) being used. If a parameter is not available,
     |        a PCAN_ERROR_ILLPARAMTYPE error will be returned.
     |      
     |        The return value of this method is a 2-tuple, where
     |        the first value is the result (TPCANStatus) of the method and
     |        the second one, the asked value
     |      
     |      Parameters:
     |        Channel   : A TPCANHandle representing a PCAN Channel
     |        Parameter : The TPCANParameter parameter to get
     |      
     |      Returns:
     |        A tuple with 2 values
     |  
     |  Initialize(self, Channel, Btr0Btr1, HwType=c_ubyte(0), IOPort=c_ulong(0), Interrupt=c_ushort(0))
     |      Initializes a PCAN Channel
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |        Btr0Btr1 : The speed for the communication (BTR0BTR1 code)
     |        HwType   : Non-PnP: The type of hardware and operation mode
     |        IOPort   : Non-PnP: The I/O address for the parallel port
     |        Interrupt: Non-PnP: Interrupt number of the parallel port
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  InitializeFD(self, Channel, BitrateFD)
     |      Initializes a FD capable PCAN Channel
     |      
     |      Parameters:
     |        Channel  : The handle of a FD capable PCAN Channel
     |        BitrateFD : The speed for the communication (FD bit rate string)
     |      
     |      Remarks:
     |        * See PCAN_BR_* values.
     |        * parameter and values must be separated by '='
     |        * Couples of Parameter/value must be separated by ','
     |        * Following Parameter must be filled out: f_clock, data_brp, data_sjw, data_tseg1, data_tseg2,
     |          nom_brp, nom_sjw, nom_tseg1, nom_tseg2.
     |        * Following Parameters are optional (not used yet): data_ssp_offset, nom_sam
     |      
     |      Example:
     |        f_clock=80000000,nom_brp=10,nom_tseg1=5,nom_tseg2=2,nom_sjw=1,data_brp=4,data_tseg1=7,data_tseg2=2,data_sjw=1
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  LookUpChannel(self, Parameters)
     |      Finds a PCAN-Basic channel that matches with the given parameters
     |      
     |      Remarks:
     |      
     |        The return value of this method is a 2-tuple, where
     |        the first value is the result (TPCANStatus) of the method and
     |        the second one a TPCANHandle value
     |      
     |      Parameters:
     |          Parameters   : A comma separated string contained pairs of parameter-name/value
     |                         to be matched within a PCAN-Basic channel
     |      
     |      Returns:
     |        A tuple with 2 values
     |  
     |  Read(self, Channel)
     |      Reads a CAN message from the receive queue of a PCAN Channel
     |      
     |      Remarks:
     |        The return value of this method is a 3-tuple, where
     |        the first value is the result (TPCANStatus) of the method.
     |        The order of the values are:
     |        [0]: A TPCANStatus error code
     |        [1]: A TPCANMsg structure with the CAN message read
     |        [2]: A TPCANTimestamp structure with the time when a message was read
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |      
     |      Returns:
     |        A tuple with three values
     |  
     |  ReadFD(self, Channel)
     |      Reads a CAN message from the receive queue of a FD capable PCAN Channel
     |      
     |      Remarks:
     |        The return value of this method is a 3-tuple, where
     |        the first value is the result (TPCANStatus) of the method.
     |        The order of the values are:
     |        [0]: A TPCANStatus error code
     |        [1]: A TPCANMsgFD structure with the CAN message read
     |        [2]: A TPCANTimestampFD that is the time when a message was read
     |      
     |      Parameters:
     |        Channel  : The handle of a FD capable PCAN Channel
     |      
     |      Returns:
     |        A tuple with three values
     |  
     |  Reset(self, Channel)
     |      Resets the receive and transmit queues of the PCAN Channel
     |      
     |      Remarks:
     |        A reset of the CAN controller is not performed
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  SetValue(self, Channel, Parameter, Buffer)
     |      Returns a descriptive text of a given TPCANStatus error
     |      code, in any desired language
     |      
     |      Remarks:
     |        Parameters can be present or not according with the kind
     |        of Hardware (PCAN Channel) being used. If a parameter is not available,
     |        a PCAN_ERROR_ILLPARAMTYPE error will be returned.
     |      
     |      Parameters:
     |        Channel      : A TPCANHandle representing a PCAN Channel
     |        Parameter    : The TPCANParameter parameter to set
     |        Buffer       : Buffer with the value to be set
     |        BufferLength : Size in bytes of the buffer
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  Uninitialize(self, Channel)
     |      Uninitializes one or all PCAN Channels initialized by CAN_Initialize
     |      
     |      Remarks:
     |        Giving the TPCANHandle value "PCAN_NONEBUS", uninitialize all initialized channels
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  Write(self, Channel, MessageBuffer)
     |      Transmits a CAN message
     |      
     |      Parameters:
     |        Channel      : A TPCANHandle representing a PCAN Channel
     |        MessageBuffer: A TPCANMsg representing the CAN message to be sent
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  WriteFD(self, Channel, MessageBuffer)
     |      Transmits a CAN message over a FD capable PCAN Channel
     |      
     |      Parameters:
     |        Channel      : The handle of a FD capable PCAN Channel
     |        MessageBuffer: A TPCANMsgFD buffer with the message to be sent
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    ... None
    


```python
help(bus.m_objPCANBasic)
```

    Help on PCANBasic in module can.interfaces.pcan.basic object:
    
    class PCANBasic(builtins.object)
     |  PCAN-Basic API class implementation
     |  
     |  Methods defined here:
     |  
     |  FilterMessages(self, Channel, FromID, ToID, Mode)
     |      Configures the reception filter
     |      
     |      Remarks:
     |        The message filter will be expanded with every call to this function.
     |        If it is desired to reset the filter, please use the 'SetValue' function.
     |      
     |      Parameters:
     |        Channel : A TPCANHandle representing a PCAN Channel
     |        FromID  : A c_uint value with the lowest CAN ID to be received
     |        ToID    : A c_uint value with the highest CAN ID to be received
     |        Mode    : A TPCANMode representing the message type (Standard, 11-bit
     |                  identifier, or Extended, 29-bit identifier)
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  GetErrorText(self, Error, Language=0)
     |      Configures or sets a PCAN Channel value
     |      
     |      Remarks:
     |      
     |        The current languages available for translation are:
     |        Neutral (0x00), German (0x07), English (0x09), Spanish (0x0A),
     |        Italian (0x10) and French (0x0C)
     |      
     |        The return value of this method is a 2-tuple, where
     |        the first value is the result (TPCANStatus) of the method and
     |        the second one, the error text
     |      
     |      Parameters:
     |        Error    : A TPCANStatus error code
     |        Language : Indicates a 'Primary language ID' (Default is Neutral(0))
     |      
     |      Returns:
     |        A tuple with 2 values
     |  
     |  GetStatus(self, Channel)
     |      Gets the current status of a PCAN Channel
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  GetValue(self, Channel, Parameter)
     |      Retrieves a PCAN Channel value
     |      
     |      Remarks:
     |        Parameters can be present or not according with the kind
     |        of Hardware (PCAN Channel) being used. If a parameter is not available,
     |        a PCAN_ERROR_ILLPARAMTYPE error will be returned.
     |      
     |        The return value of this method is a 2-tuple, where
     |        the first value is the result (TPCANStatus) of the method and
     |        the second one, the asked value
     |      
     |      Parameters:
     |        Channel   : A TPCANHandle representing a PCAN Channel
     |        Parameter : The TPCANParameter parameter to get
     |      
     |      Returns:
     |        A tuple with 2 values
     |  
     |  Initialize(self, Channel, Btr0Btr1, HwType=c_ubyte(0), IOPort=c_ulong(0), Interrupt=c_ushort(0))
     |      Initializes a PCAN Channel
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |        Btr0Btr1 : The speed for the communication (BTR0BTR1 code)
     |        HwType   : Non-PnP: The type of hardware and operation mode
     |        IOPort   : Non-PnP: The I/O address for the parallel port
     |        Interrupt: Non-PnP: Interrupt number of the parallel port
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  InitializeFD(self, Channel, BitrateFD)
     |      Initializes a FD capable PCAN Channel
     |      
     |      Parameters:
     |        Channel  : The handle of a FD capable PCAN Channel
     |        BitrateFD : The speed for the communication (FD bit rate string)
     |      
     |      Remarks:
     |        * See PCAN_BR_* values.
     |        * parameter and values must be separated by '='
     |        * Couples of Parameter/value must be separated by ','
     |        * Following Parameter must be filled out: f_clock, data_brp, data_sjw, data_tseg1, data_tseg2,
     |          nom_brp, nom_sjw, nom_tseg1, nom_tseg2.
     |        * Following Parameters are optional (not used yet): data_ssp_offset, nom_sam
     |      
     |      Example:
     |        f_clock=80000000,nom_brp=10,nom_tseg1=5,nom_tseg2=2,nom_sjw=1,data_brp=4,data_tseg1=7,data_tseg2=2,data_sjw=1
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  LookUpChannel(self, Parameters)
     |      Finds a PCAN-Basic channel that matches with the given parameters
     |      
     |      Remarks:
     |      
     |        The return value of this method is a 2-tuple, where
     |        the first value is the result (TPCANStatus) of the method and
     |        the second one a TPCANHandle value
     |      
     |      Parameters:
     |          Parameters   : A comma separated string contained pairs of parameter-name/value
     |                         to be matched within a PCAN-Basic channel
     |      
     |      Returns:
     |        A tuple with 2 values
     |  
     |  Read(self, Channel)
     |      Reads a CAN message from the receive queue of a PCAN Channel
     |      
     |      Remarks:
     |        The return value of this method is a 3-tuple, where
     |        the first value is the result (TPCANStatus) of the method.
     |        The order of the values are:
     |        [0]: A TPCANStatus error code
     |        [1]: A TPCANMsg structure with the CAN message read
     |        [2]: A TPCANTimestamp structure with the time when a message was read
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |      
     |      Returns:
     |        A tuple with three values
     |  
     |  ReadFD(self, Channel)
     |      Reads a CAN message from the receive queue of a FD capable PCAN Channel
     |      
     |      Remarks:
     |        The return value of this method is a 3-tuple, where
     |        the first value is the result (TPCANStatus) of the method.
     |        The order of the values are:
     |        [0]: A TPCANStatus error code
     |        [1]: A TPCANMsgFD structure with the CAN message read
     |        [2]: A TPCANTimestampFD that is the time when a message was read
     |      
     |      Parameters:
     |        Channel  : The handle of a FD capable PCAN Channel
     |      
     |      Returns:
     |        A tuple with three values
     |  
     |  Reset(self, Channel)
     |      Resets the receive and transmit queues of the PCAN Channel
     |      
     |      Remarks:
     |        A reset of the CAN controller is not performed
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  SetValue(self, Channel, Parameter, Buffer)
     |      Returns a descriptive text of a given TPCANStatus error
     |      code, in any desired language
     |      
     |      Remarks:
     |        Parameters can be present or not according with the kind
     |        of Hardware (PCAN Channel) being used. If a parameter is not available,
     |        a PCAN_ERROR_ILLPARAMTYPE error will be returned.
     |      
     |      Parameters:
     |        Channel      : A TPCANHandle representing a PCAN Channel
     |        Parameter    : The TPCANParameter parameter to set
     |        Buffer       : Buffer with the value to be set
     |        BufferLength : Size in bytes of the buffer
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  Uninitialize(self, Channel)
     |      Uninitializes one or all PCAN Channels initialized by CAN_Initialize
     |      
     |      Remarks:
     |        Giving the TPCANHandle value "PCAN_NONEBUS", uninitialize all initialized channels
     |      
     |      Parameters:
     |        Channel  : A TPCANHandle representing a PCAN Channel
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  Write(self, Channel, MessageBuffer)
     |      Transmits a CAN message
     |      
     |      Parameters:
     |        Channel      : A TPCANHandle representing a PCAN Channel
     |        MessageBuffer: A TPCANMsg representing the CAN message to be sent
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  WriteFD(self, Channel, MessageBuffer)
     |      Transmits a CAN message over a FD capable PCAN Channel
     |      
     |      Parameters:
     |        Channel      : The handle of a FD capable PCAN Channel
     |        MessageBuffer: A TPCANMsgFD buffer with the message to be sent
     |      
     |      Returns:
     |        A TPCANStatus error code
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    


```python

```


```python

```
