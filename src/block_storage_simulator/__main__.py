"""CLI entry point for the simulator."""

from __future__ import annotations
import argparse
import time
from .ads_server import AdsServer
from .gui import SimulatorApp
from .simulator import BlockStorageSimulator
from .tier2_warehouse import Tier2Warehouse
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
    # เชื่อมต่อ Tier 2 Warehouse เข้ากับระบบ
    simulator.warehouse = Tier2Warehouse()

    server: AdsServer | None = None

    if args.mode in {"ads", "both"}:
        server = AdsServer(simulator=simulator, ip_address=args.bind, port=args.port)
        server.start()

    if args.mode in {"gui", "both"}:
        app = SimulatorApp(simulator)

        def handle_add_block():
            if not simulator.can_modify_pallet_at_home():
                return
    
            result = simulator.warehouse.find_empty_slot()
            if result:
                row, col, layer = result

        # --- เพิ่มบรรทัดนี้เพื่อความชัวร์ ---
        # สั่งให้ Simulator วางบล็อกบนถาดที่ Home ทันทีที่กดปุ่ม Add
                simulator.add_block_to_home_pallet() 
        
                simulator.send_pallet()                
                target_x = 80.0 + (col * 85.0)
                target_y = 80.0 + (row * 85.0)
        
                simulator.release_from_imaging()
        
        # คีบจาก 160.0, 410.0 ไปยังตำแหน่งที่คำนวณ
                cmd = TransferCommand(src_x=160.0, src_y=410.0, dst_x=target_x, dst_y=target_y)
        
                if simulator.transfer_item(cmd):
                    simulator.warehouse.add_item(row, col)
                    simulator.remove_block_from_home_pallet() # แจ้งซิมว่าของออกจากถาดแล้ว
                    simulator.return_pallet()
                    print(f"Added to ({target_x}, {target_y})")
                else:
                    print(f"Error: {simulator.state.last_error}")
                    simulator.return_pallet()

        def handle_remove_block():
    # ดึงพิกัดของที่เก่าที่สุด (FIFO) จาก Logic
            result = simulator.warehouse.remove_item()
            if result:
                row, col, layer = result
        
        # คำนวณพิกัดให้ตรงกับ Simulator (80, 165, 250, 335)
                src_x = 80.0 + (col * 85.0)
                src_y = 80.0 + (row * 85.0)

        # 1. ส่งถาดเปล่าออกไปรับของ
                simulator.send_pallet()
                simulator.release_from_imaging()

        # 2. สั่งหุ่นยนต์คีบจากคลังมาวางบนถาด (160, 410)
                cmd = TransferCommand(src_x=src_x, src_y=src_y, dst_x=160.0, dst_y=410.0)

                if simulator.transfer_item(cmd):
            # เมื่อคีบมาวางสำเร็จ ส่งถาดกลับ Home
                    simulator.return_pallet()
            
            # --- ส่วนที่เพิ่มเข้าไปเพื่อแก้ปัญหาของคุณ ---
            # ต้องแจ้ง Simulator ว่าเราหยิบบล็อกออกจากถาด (Pallet) แล้ว
            # เพื่อให้ภาพบล็อกสีเขียวหายไปจากหน้าจอ และสถานะถาดกลับมาว่างพร้อมใช้งานต่อ
                    simulator.remove_block_from_home_pallet() 
            
                    print(f"Success: Removed from Row {row}, Col {col} and cleared pallet")
                else:
            # หาก Simulator หาบล็อกที่พิกัด (src_x, src_y) ไม่เจอ
                    print(f"Sim Error (Remove): {simulator.state.last_error} at ({src_x}, {src_y})")
                    simulator.return_pallet()
            else:
                print("Warehouse is Empty!")

        def handle_reset():
            # ล้างค่าทั้งหมดทั้งใน Simulator และ Logic Warehouse
            simulator.reset()
            simulator.warehouse.reset_warehouse()
            print("--- System & Warehouse Reset Completed ---")

        # ผูกฟังก์ชันเข้ากับปุ่มบน GUI
        app.on_add_click = handle_add_block
        app.on_remove_click = handle_remove_block
        app.on_reset_click = handle_reset

        try:
            print("--- Starting Block Storage Simulator (Tier 2) ---")
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
