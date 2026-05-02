class BulkWarehouse:
    def __init__(self):
        self.item_count = 0 
        print("--- Tier 1 BulkWarehouse System Initialized ---")

    def add_item(self):
        """Action: Supplier -> Warehouse (Incoming)"""
        self.item_count += 1
        self.report_status()

    def remove_item(self):
        """2. What leaves? Warehouse -> Customer (Outgoing)"""
        if self.item_count > 0:
            self.item_count -= 1
            print("Action: Item dispatched successfully.")
        else:
            print("Warning: Out of stock! Cannot remove item.")
        self.report_status()

    def report_status(self):
        """3. What remains? (Status Reporting)"""
        print(f"Current Inventory Status: {self.item_count} items remaining.")

if __name__ == "__main__":
    my_warehouse = BulkWarehouse()
    my_warehouse.add_item()    #
    my_warehouse.add_item()    
    my_warehouse.remove_item() 