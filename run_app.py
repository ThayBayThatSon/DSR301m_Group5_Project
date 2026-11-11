import sys
import socket
import subprocess
import uvicorn

sys.stdout.reconfigure(encoding="utf-8")


def get_network_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if ip not in ips and not ip.startswith("127."):
                ips.append(ip)
    except Exception:
        pass

    tailscale_ip = None
    for ip in ips:
        if ip.startswith("100."):
            tailscale_ip = ip
            break

    if not tailscale_ip:
        try:
            out = subprocess.check_output(["tailscale", "ip", "-4"], text=True, timeout=2).strip()
            if out:
                tailscale_ip = out.splitlines()[0].strip()
        except Exception:
            pass

    return ips, tailscale_ip


if __name__ == "__main__":
    port = 8000
    ips, ts_ip = get_network_ips()
    print("=" * 72)
    print("🚀 CALIFORNIA US AQI LIVE FORECASTER & MODEL BENCHMARK SUITE (24/7 CPU)")
    print("=" * 72)
    print(f"👉 Truy cập trực tiếp trên máy này : http://localhost:{port}")
    for ip in ips:
        print(f"👉 Truy cập qua mạng LAN / VPN     : http://{ip}:{port}")
    if ts_ip:
        print(f"🔒 Truy cập qua mạng Tailscale 24/7: http://{ts_ip}:{port}")
    else:
        print("🔒 Truy cập qua Tailscale          : http://<TAILSCALE_IP>:8000")
    print("=" * 72)

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True, log_level="info")

