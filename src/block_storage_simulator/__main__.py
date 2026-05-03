from __future__ import annotations
import argparse
import time
from .ads_server import AdsServer
from .gui import SimulatorApp
from .simulator import BlockStorageSimulator
from .tier2_warehouse import Tier2Warehouse
from block_storage_simulator import simulator
def main() -> None:
    args = build_parser().parse_args()
    simulator = BlockStorageSimulator()
    simulator.warehouse = Tier2Warehouse()
    
    server: AdsServer | None = None

    if args.mode in {"ads", "both"}:
        server = AdsServer(simulator=simulator, ip_address=args.bind, port=args.port)
        server.start()

    if args.mode in {"gui", "both"}:
        app = SimulatorApp(simulator)

        def handle_add_block():
            slot = simulator.warehouse.find_empty_slot() 
            if slot:
                row, col = slot
                simulator.add_block_to_home_pallet() 
                simulator.move_block_to_storage(row, col)
                simulator.warehouse.add_item()
            else:
                print("Warehouse is full!")

        app.on_add_click = handle_add_block

        try:
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