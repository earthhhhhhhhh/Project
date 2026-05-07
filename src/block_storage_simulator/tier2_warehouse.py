from .tier1_warehouse import BulkWarehouse

class Tier2Warehouse(BulkWarehouse):
    def __init__(self):
        super().__init__()
        self.rows = 3  # ปรับตามที่คุณต้องการ
        self.cols = 4
        self.max_layers = 2
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.inventory_map = {} 
        self.total_items = 0

    def find_empty_slot(self):
        # วนหาช่องว่างแบบลำดับ Row -> Col
        for r in range(self.rows): 
            for c in range(self.cols): 
                if self.grid[r][c] < self.max_layers:
                    layer = self.grid[r][c]
                    return r, c, layer
        return None

    def add_item(self, row, col):
        layer = self.grid[row][col]
        # เก็บ Key เป็นพิกัด 3 มิติ (r, c, l)
        self.inventory_map[(row, col, layer)] = True 
        self.grid[row][col] += 1
        self.total_items += 1
        self.report_status()
        return True

    def remove_item(self):
        if not self.inventory_map: 
            print("DEBUG: inventory_map is empty") # เพิ่มเช็ค
            return None
        
        keys_list = list(self.inventory_map.keys())
        for key in keys_list:
            r, c, l = key
            if l == self.grid[r][c] - 1:
                print(f"DEBUG: Found target to remove: {key}") # เช็คว่าเจอจริงไหม
                row, col, layer = key
                del self.inventory_map[key]
                self.grid[row][col] -= 1
                self.total_items -= 1
                return row, col, layer
        
        print("DEBUG: No accessible items found (all blocked by others)")
        return None

    def report_status(self):
        # อัปเดตตารางใน Terminal เพื่อเช็กว่า Logic เรายังแม่นอยู่ไหม
        if hasattr(self, 'print_storage_map'):
            self.print_storage_map()

    def reset_warehouse(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.inventory_map = {} 
        self.total_items = 0   
        self.report_status()