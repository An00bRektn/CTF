import pyshark

def extract_URLs():
    pcap_path = "./capture.pcap"
    packets = pyshark.FileCapture(pcap_path, display_filter="ip.src == 192.168.1.10")
    urls = []

    for pkt in packets:
        try:
            domain = pkt.dns.qry_name
            urls.append(domain)
        except Exception:
            pass
    
    return urls

domains = extract_URLs()
concat_hex = ""
for d in domains:
    concat_hex += d[:-16]

with open("output.xls", "wb") as fd:
    fd.write(bytes.fromhex(concat_hex))