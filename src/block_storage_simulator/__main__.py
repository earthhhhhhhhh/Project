"""CLI entry point for the simulator."""

from __future__ import annotations
import argparse
import time
from .ads_server import AdsServer
from .gui import SimulatorApp
from .simulator import BlockStorageSimulator
from .tier1_warehouse import BulkWarehouse
from .models import TransferCommand

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Block storage simulator")
    parser.add_argument("--mode", choices=("gui", "ads", "both"), default="gui")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=48898)
    return parser

def main() -> None:
    args = build_parser().parse_args()
    simulator = BlockStorageSimulator()
    
    # กำหนดใช้งานคลังสินค้าแบบ Tier 1 (Bulk)
    simulator.warehouse = BulkWarehouse() 

    server: AdsServer | None = None

    if args.mode in {"ads", "both"}:
        server = AdsServer(simulator=simulator, ip_address=args.bind, port=args.port)
        server.start()

    if args.mode in {"gui", "both"}:
        app = SimulatorApp(simulator)

        def handle_add_block():
            if not simulator.can_modify_pallet_at_home(): 
                return
            
            # Tier 1: รับค่าพิกัดพ้นที่ว่าง (คืนค่าเฉพาะ row และ col)
            result = simulator.warehouse.find_empty_slot() 
            if result:
                row, col = result 
                layer = 0 # Tier 1 ไม่มีการวางซ้อน กำหนดเป็นชั้นพื้นฐาน
                
                target_x = 80.0 + (col * 85.0) 
                target_y = 80.0 + (row * 85.0) 

                simulator.add_block_to_home_pallet() 
                simulator.send_pallet()              
                simulator.release_from_imaging()     
                
                cmd = TransferCommand(src_x=160.0, src_y=410.0, dst_x=target_x, dst_y=target_y) 
                
                if simulator.transfer_item(cmd):
                    simulator.warehouse.add_item(row, col) 
                    print(f"Tier 1 Success: Row {row}, Col {col}")
                    simulator.return_pallet()

        def handle_remove_block():
            # Tier 1: ค้นหาไอเทมที่จะนำออก (คืนค่าเฉพาะ row และ col)
            result = simulator.warehouse.remove_item() 
            if result:
                row, col = result 
                layer = 0
                
                src_x = 80.0 + (col * 85.0) 
                src_y = 80.0 + (row * 85.0) 

                simulator.send_pallet()
                simulator.release_from_imaging()
                
                cmd = TransferCommand(src_x=src_x, src_y=src_y, dst_x=160.0, dst_y=410.0)
                
                if simulator.transfer_item(cmd):
                    simulator.return_pallet() 
                    simulator.remove_block_from_home_pallet()
                    print(f"Tier 1 Removed: Row {row}, Col {col}")
                else:
                    print(f"Error: {simulator.state.last_error}")

        def handle_reset():
            # 1. ล้างสถานะระบบและหยุดการทำงานค้างของหุ่นยนต์
            simulator.reset() 
            # 2. ล้างข้อมูลตาราง Grid ในคลังสินค้า Tier 1
            simulator.warehouse.reset_warehouse()
            print("--- Hard Reset: System & Warehouse Cleared ---")

        # เชื่อมต่อปุ่มกดเข้ากับฟังก์ชันควบคุม
        app.on_add_click = handle_add_block
        app.on_remove_click = handle_remove_block
        app.on_reset_click = handle_reset

        try:
            print("--- Starting GUI Mode (Tier 1) ---")
            app.run() 
        finally:
            if server is not None:
                server.stop()
        return 

    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        if server is not None:
            server.stop()

if __name__ == "__main__":
    main()