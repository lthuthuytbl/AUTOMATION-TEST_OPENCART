from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage

# --- DỮ LIỆU ---
BASE_URL = "http://localhost/opencart_test/index.php?route=account/login"
EMAIL = "thuthuylac79@gmail.com"
PASSWORD = "ThuThuyLac99"

def test_tc04_check_return_history(page: Page):
    print("\n--- START: Kiem tra Lich Su Tra Hang ---")
    login_p = LoginPage(page)
    acc_p = MyAccountPage(page)

    # 1. Login
    login_p.navigate(BASE_URL)
    login_p.login(EMAIL, PASSWORD)

    # 2. Vào danh sách trả hàng
    acc_p.go_to_return_list()

    print("Check: Dang cho trang load bang du lieu...")
    # Chờ cái bảng hiện ra
    expect(page.locator("#content table.table").first).to_be_visible(timeout=10000)
    print("   -> OK: Da thay bang danh sach!")

    # 3. Xem chi tiết đơn đầu tiên
    acc_p.view_first_return_record()
    
    # 4. Verify
    print("Check: Kiem tra xem da vao trang chi tiet chua...")
    
    page.wait_for_timeout(2000)

    expect(page.get_by_text("Return ID", exact=False).first).to_be_visible(timeout=10000)
    
    expect(page.get_by_text("Reason for Return")).to_be_visible()

    print("   -> OK: Da thay 'Return ID' & 'Reason' -> Chinh xac la trang chi tiet!")
    print("\n>>> TEST PASSED: Quy trinh kiem tra lich su OK!")