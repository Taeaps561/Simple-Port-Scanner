import socket
import sys
from datetime import datetime

def scan_ports(target_host, port_range, timeout=1):
    """
    ทำการสแกนพอร์ตบนโฮสต์เป้าหมาย
    """
    print("-" * 50)
    print(f"กำลังสแกนเป้าหมาย: {target_host}")
    print(f"เริ่มสแกนเมื่อ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    try:
        # แยกช่วงพอร์ต
        start_port, end_port = map(int, port_range.split('-'))
    except ValueError:
        print("❌ รูปแบบช่วงพอร์ตไม่ถูกต้อง (เช่น: 1-100)")
        return

    open_ports = []

    for port in range(start_port, end_port + 1):
        # สร้างวัตถุ Socket: AF_INET สำหรับ IPv4, SOCK_STREAM สำหรับ TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout) # ตั้งค่า Timeout เพื่อไม่ให้โปรแกรมค้าง

        # ลองเชื่อมต่อ (Attempt to connect)
        result = s.connect_ex((target_host, port))
        
        if result == 0:
            # result = 0 หมายถึง การเชื่อมต่อสำเร็จ (Port is Open)
            try:
                # ลองดึงข้อมูลบริการที่ทำงานบนพอร์ตนั้น (ถ้ามี)
                service = socket.getservbyport(port, 'tcp')
            except OSError:
                service = "Unknown Service"
                
            print(f"✅ พอร์ต {port} : เปิดอยู่ ({service})")
            open_ports.append(port)

        s.close()

    print("-" * 50)
    print(f"การสแกนเสร็จสิ้น. พบ {len(open_ports)} พอร์ตที่เปิดอยู่")
    if open_ports:
        print(f"พอร์ตที่เปิด: {open_ports}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        # ตรวจสอบการรับ Input จาก Command Line
        print("การใช้งาน: python port_scanner.py <IP/Host> <StartPort-EndPort>")
        print("ตัวอย่าง: python port_scanner.py 127.0.0.1 20-80")
        sys.exit(1)

    target = sys.argv[1]
    ports = sys.argv[2]
    
    # แปลงชื่อโฮสต์เป็น IP Address ก่อนสแกน
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"❌ ไม่สามารถแก้ไขชื่อโฮสต์ '{target}' ได้")
        sys.exit(1)
        
    scan_ports(target_ip, ports)