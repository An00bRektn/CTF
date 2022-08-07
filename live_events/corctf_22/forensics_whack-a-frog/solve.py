import turtle
import time
import pyshark

# Credit bakki for doing the hard part of actually parsing the pcap
def extract_URIs():
    pcap_path = "./whacking-the-froggers.pcap"
    uri_list = []
    packets = pyshark.FileCapture(pcap_path, display_filter="http.request and http.request.uri.query")

    print("[*] Parsing packets...")
    for pkt in packets:
        if pkt.http.request_full_uri:
            uri_list.append(pkt.http.request_full_uri)
    packets.close()
    print("[+] Parsing complete.")
    return uri_list

def parse_instruction(line):
    line = line.split('&')
    x = int(line[0][2:])
    y = int(line[1][2:])
    event = line[2][6:]
    return (x,y,event)


if __name__ == "__main__":
    uri_list = extract_URIs()

    # lets parse it so we only get the coordinates of the cursor:
    instructions = [query.replace("http://0.0.0.0:8000/anticheat?", "").strip() for query in uri_list]
    
    # Why :msfrog: when 🐢
    window = turtle.Screen()
    window.setup(2000,300)
    t = turtle.Turtle()

    t.penup()
    for line in instructions:
        x, y, event = parse_instruction(line)
        if event == "mousemove":
            t.goto(x,y)
        elif event == "mousedown":
            t.goto(x,y)
            t.pendown()
        elif event == "mouseup":
            t.goto(x,y)
            t.penup()

    time.sleep(20)