import pyshark

# Credit bakki for doing the hard part of actually parsing the pcap
def get_domains():
    pcap_path = "./out.pcap"
    domains = []
    packets = pyshark.FileCapture(pcap_path, display_filter="dns")

    print("[*] Parsing packets...")
    for pkt in packets:
        if pkt.dns.qry_name and "cybrforce.io" in pkt.dns.qry_name and pkt.dns.qry_name not in domains:
            domains.append(pkt.dns.qry_name)
    packets.close()
    print("[+] Parsing complete.")
    return domains

domains = get_domains()
payload = ""
for d in domains:
    payload += d.split(".")[0]

from base64 import b64decode
print(b64decode(bytes.fromhex(payload)))
