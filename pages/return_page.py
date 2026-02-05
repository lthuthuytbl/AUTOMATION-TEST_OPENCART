from pages.base_page import BasePage

class ReturnPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # --- LOCATORS (ĐỊNH NGHĨA VỊ TRÍ) ---
        # 1. Các ô nhập liệu cá nhân
        self.firstname_input = page.locator("#input-firstname")
        self.lastname_input = page.locator("#input-lastname")
        self.email_input = page.locator("#input-email")
        self.telephone_input = page.locator("#input-telephone")
        
        # 2. Ngày đặt hàng & Số lượng
        self.order_date_input = page.locator("#input-date-ordered")
        self.quantity_input = page.locator("#input-quantity")
        
        # 3. Các nút chọn (Radio/Checkbox)
        self.reason_text = page.locator("label").filter(has_text="Dead On Arrival")
        self.opened_yes_text = page.get_by_text("Yes", exact=True)
        
        # 4. Ô ghi chú & Nút Gửi
        self.comment_input = page.locator("#input-comment")
        self.submit_btn = page.locator(".btn.btn-primary")


    def prepare_form_basics(self):
        """Hàm phụ: Cuộn trang và tick các mục bắt buộc (Dùng cho cả Test 01 và 03)"""
        print("Action: Cuon trang & Tick chon Ly do + Mo hop...")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(500)
        
        if self.reason_text.is_visible():
            self.reason_text.click(force=True)
        
        if self.opened_yes_text.is_visible():
            self.opened_yes_text.click(force=True)

    def fill_return_form(self, comment):
        print("Action: Dien form tra hang day du (Happy Case)")
        
        # Gọi hàm chuẩn bị ở trên
        self.prepare_form_basics()
        
        # Điền ghi chú
        print(f"Action: Dien ghi chu: {comment}")
        self.comment_input.fill(comment)

    def edit_personal_info(self, firstname, lastname):
        print(f"Action: Doi Ten thanh '{firstname}', Ho thanh '{lastname}'")
        self.firstname_input.fill(firstname)
        self.lastname_input.fill(lastname)

    def edit_order_info(self, date_ordered=None, quantity=None):
        if date_ordered:
            print(f"Action: Doi Ngay Dat Hang thanh '{date_ordered}'")
            self.order_date_input.fill(date_ordered)
            # Click ra ngoài để đóng lịch popup
            self.page.locator("h1").click()

        if quantity:
            print(f"Action: Doi So Luong thanh '{quantity}'")
            self.quantity_input.fill(str(quantity))

    def submit(self):
        print("Action: Bam nut Submit")
        self.submit_btn.click(force=True)