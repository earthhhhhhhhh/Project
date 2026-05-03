from .tier1_warehouse import BulkWarehouse

class Tier2Warehouse(BulkWarehouse):
    def __init__(self):
        super().__init__()
        self.inventory_map = {}

    def find_empty_slot(self):
        for row in range(3):
            for col in range(5):
                if (row, col) not in self.inventory_map:
                    self.inventory_map[(row, col)] = 1
                    return row, col

        for row in range(3):
            for col in range(5):
                if self.inventory_map.get((row, col)) == 1:
                    self.inventory_map[(row, col)] = 2
                    return row, col

        return None

    def remove_item(self, row=None, col=None):
        if row is not None and col is not None:
            if (row, col) in self.inventory_map:
                if self.inventory_map[(row, col)] == 2:
                    self.inventory_map[(row, col)] = 1
                else:
                    del self.inventory_map[(row, col)]
                if self.item_count > 0:
                    self.item_count -= 1
        elif self.item_count > 0:
            self.item_count -= 1
            
        self.report_status()