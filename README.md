# Protocol Hub

This repo includes protocols for modbus rtu, tcp and more. Protocol is written in yaml. 


## How to add ne protocol

1. Create folder for protocol
2. Add info file and yml file
3. Info file syntax should like this:  
    pri-*value*_type-*value*_name-*value*.info
   yml file should be same name as folder name
4. fill in yml file


## syntax yaml file
yaml file are unique for each connection type




### modbus

type: pv #sensor types
host: !parameter
adr: !parameter
port: 502
prcl: #protocol
  - unique_id: Reserve1
    address: 5002 
    input_type: input
    data_type: uint16
    scale: 0.1



## types

actuator types
- switch (Switch ; SW)
- proportional switch  (ProportionalSwitch , SW)
- value power (ValuePower ; VP) 
- Sync meter values (SyncMeter; SM)
- power limit of inverter (PowerLimit ; PL), subtype exportlimit, InverterLimit


sensor type
- sensor to get all meter values (mainmeter)
- sensor to get all gas values (gasmeter)
- pv production sensor (pv)
- battery info sensor (battery)
- usage power sensor (usage)
- ev charger sensor (charger)

