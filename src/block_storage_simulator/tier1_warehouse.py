class BulkWarehouse:
    def __init__(self):
        self.item_count = 0 
        self.max_capacity = 30
        print("--- Tier 1 BulkWarehouse System Initialized ---")

    def find_empty_slot(self):
        if self.item_count >= self.max_capacity:
            return None
            
        current_slot = self.item_count % 15
        row = current_slot // 5
        col = current_slot % 5
        return row, col

    def add_item(self):
        if self.item_count < self.max_capacity:
            self.item_count += 1
            self.report_status()
            return True
        return False

    def remove_item(self, row=None, col=None):
        if self.item_count > 0:
            self.item_count -= 1
            print("Action: Item dispatched successfully.")
        else:
            print("Warning: Out of stock!")
        self.report_status()

    def report_status(self):
        print(f"Current Inventory Status: {self.item_count} items remaining.")