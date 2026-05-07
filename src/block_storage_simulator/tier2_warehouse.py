from .tier1_warehouse import BulkWarehouse
<<<<<<< HEAD
class Tier2Warehouse(BulkWarehouse):
    def __init__(self):
        super().__init__()
        self.rows = 4
        self.cols = 4
        self.max_layers = 2  # <--- แก้เป็น 2 เพื่อให้วางซ้อนได้
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.inventory_map = {} # เก็บเป็นลำดับ (row, col, layer) เพื่อ FIFO
        self.total_items = 0

    def find_empty_slot(self):
        # วนหาช่องที่ยังไม่เต็ม (max_layers = 2)
        for r in range(self.rows): 
            for c in range(self.cols): 
                if self.grid[r][c] < 2: # ถ้าชั้นยังไม่เต็ม 2
=======

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
>>>>>>> tier2_warehouse
                    layer = self.grid[r][c]
                    return r, c, layer
        return None

    def add_item(self, row, col):
<<<<<<< HEAD
        # บันทึกข้อมูล: ชิ้นที่ 1 จะเป็น (0,0,0), ชิ้นที่ 2 จะเป็น (0,0,1)
        layer = self.grid[row][col]
        self.inventory_map[(row, col, layer)] = 1 
        self.grid[row][col] += 1 # เพิ่มจำนวนชั้นในช่องนั้น
=======
        layer = self.grid[row][col]
        # เก็บ Key เป็นพิกัด 3 มิติ (r, c, l)
        self.inventory_map[(row, col, layer)] = True 
        self.grid[row][col] += 1
>>>>>>> tier2_warehouse
        self.total_items += 1
        self.report_status()
        return True

    def remove_item(self):
<<<<<<< HEAD
        if not self.inventory_map: return None
        
        # FIFO: ดึง key แรกสุดออกมา (ตัวที่เข้ามาก่อน)
        # เช่น ถ้าเราใส่ 1(ล่าง), 2(บน) -> ตัวแรกที่เจอคือ 1(ล่าง)
        first_key = next(iter(self.inventory_map))
        row, col, layer = first_key
        
        # แต่ในทางกายภาพ เราหยิบ 1(ล่าง) ไม่ได้ถ้ามี 2(บน) ทับอยู่! 
        # ดังนั้นถ้าชิ้นที่เราจะหยิบมีชั้นบนทับอยู่ เราต้องข้ามไปหยิบชั้นบนสุดก่อน
        
        # เช็คว่ามีชั้นที่สูงกว่าทับอยู่ไหมในช่องเดียวกัน
        top_layer = self.grid[row][col] - 1
        if layer < top_layer:
            # ถ้ามีของทับ ให้เปลี่ยนไปหยิบชั้นบนสุด (top_layer) ของช่องนั้นแทน
            row, col, layer = row, col, top_layer
            # อัปเดต key ที่จะลบจริง
            target_key = (row, col, layer)
        else:
            target_key = first_key

        # ลบข้อมูลชิ้นที่หยิบจริง
        del self.inventory_map[target_key]
        self.grid[row][col] -= 1
        self.total_items -= 1
        self.report_status()
        return row, col, layer

    def report_status(self):
        # เรียกฟังก์ชันจาก Tier 1 (BulkWarehouse) เพื่ออัปเดตหน้าจอ GUI
=======
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
>>>>>>> tier2_warehouse
        if hasattr(self, 'print_storage_map'):
            self.print_storage_map()

    def reset_warehouse(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.inventory_map = {} 
        self.total_items = 0   
        self.report_status()