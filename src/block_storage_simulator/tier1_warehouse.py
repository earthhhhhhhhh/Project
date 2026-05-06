class BulkWarehouse:
    def __init__(self):
        # ปรับให้เหลือช่องที่วางได้จริง (ลองทดสอบที่ 2x2 หรือ 2x3 ดูก่อนครับ)
        self.rows = 3  # แถวแนวตั้ง
        self.cols = 4  # แถวแนวนอน (Simulator พื้นที่แนวนอนจะยาวกว่า)
        self.max_layers = 1
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.total_items = 0
        print(f"--- [System] {self.__class__.__name__} Initialized ---")

    def find_empty_slot(self): # เปลี่ยนชื่อให้ตรงกับที่ __main__ เรียก
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] < self.max_layers:
                    return r, c # ส่งกลับแค่ 2 ค่าตามที่ __main__ ต้องการ
        return None

    def add_item(self, row, col):
        self.grid[row][col] += 1
        self.total_items += 1
        self.print_storage_map()
        return True

    def remove_item(self):
        # วนหาช่องที่มีของ แล้วส่งพิกัดกลับไปให้หุ่นยนต์ไปหยิบ
        for r in reversed(range(self.rows)):
            for c in reversed(range(self.cols)):
                if self.grid[r][c] > 0:
                    self.grid[r][c] -= 1
                    self.total_items -= 1
                    self.print_storage_map()
                    return r, c # สำคัญมาก! ต้องส่งพิกัดกลับไป
        return None

    def print_storage_map(self):
        print("\n[Current Storage Map]")
        for row in self.grid:
            print(" ".join(f"[{val}]" for val in row))
        print(f"Summary: {self.total_items} units\n")

    def reset_warehouse(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.total_items = 0
        self.print_storage_map()