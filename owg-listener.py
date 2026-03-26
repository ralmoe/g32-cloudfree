#!/usr/bin/env python3
import socket
from datetime import datetime

last_data = None

def decode_ow_temp(b1, b2):
    """Formula: (Byte1 * 100 + Byte2) / 10"""
    raw = b1 * 100 + b2
    if raw == 1500:
        return None
    return raw / 10.0


def decode_ow_temp_str(b1, b2):
    t = decode_ow_temp(b1, b2)
    return f"{t:>5.1f} °C" if t is not None else "--- (not connected)"


def process_packet(data):
    global last_data
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    # ignore packages without diff
    if last_data is not None and data == last_data:
        last_data = data
        return

    print(f"\n[{ts}]")

    # internal sensors (offset 06-13)
    print("  ZONES:")
    # for name, offset in zones:
    for i in range(4):
        offset = 6 + (i * 2)
        if len(data) >= offset + 2:
            print(
                f"    Zone {i + 1}: {decode_ow_temp_str(data[offset], data[offset + 1])}"
            )

    # external sensors (offset 14-21)
    print("  EXT. SENSOR:")
    for i in range(4):
        offset = 14 + (i * 2)
        if len(data) >= offset + 2:
            print(
                f"    Ext {i + 1} : {decode_ow_temp_str(data[offset], data[offset + 1])}"
            )

    last_data = data


def run_server():
    HOST = "0.0.0.0"
    PORT = 4501
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Lausche auf {HOST}:{PORT}...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"CONNECTED: {addr}")
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        process_packet(data)
                    except Exception as e:
                        print(f"ERROR: {e}")
                        break
                print("CONNECTION LOST.")


if __name__ == "__main__":
    run_server()
