from pages.base_page import BasePage

class MyAccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # --- CODE CŨ CỦA BẠN (GIỮ NGUYÊN) ---
        # Link Order History
        self.order_history_link = page.get_by_role("link", name="View your order history")
        
        # Thêm chữ "a" vào trước để bắt buộc tìm thẻ Link (<a>)
        # Tránh nhầm với thẻ <button> ẩn
        
        # 1. Nút View (Màu xanh - Là thẻ a)
        self.view_btn = page.locator("a.btn.btn-info").first
        
        # 2. Nút Return (Màu đỏ - Là thẻ a)
        # Lúc nãy lỗi vì nó tìm nhầm nút <button title="Remove">
        self.return_item_btn = page.locator("a.btn.btn-danger").first

        # --- PHẦN BỔ SUNG MỚI (CHỈ ĐỂ CHẠY TEST 04) ---
        # Link Returns ở cột bên phải (Right Column)
        self.right_column_returns = page.locator("#column-right").get_by_role("link", name="Returns")

    # --- CÁC HÀM CŨ (GIỮ NGUYÊN) ---
    def go_to_order_history(self):
        print("Action: Vao lich su don hang")
        self.click(self.order_history_link)
        self.page.wait_for_timeout(1000)

    def go_to_return_form(self):
        print("Action: Chon don hang -> Return")
        # Click View
        self.view_btn.click()
        # Chờ trang Info load xong
        self.page.wait_for_selector("a.btn.btn-danger")
        # Click Return
        print("Action: Click nut Return (Mau do)...")
        self.return_item_btn.click()

    # --- CÁC HÀM MỚI (BỔ SUNG CHO TEST 04) ---
    def go_to_return_list(self):
        print("Action: Click menu Returns (Cot ben phai)")
        self.right_column_returns.click()

    def view_first_return_record(self):
        print("Action: Click nut 'View' (Hinh con mat)...")
        # Tận dụng lại nút view màu xanh ở trên (vì class giống nhau)
        self.view_btn.click()