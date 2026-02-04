from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.return_page import ReturnPage

# --- DỮ LIỆU ---
BASE_URL = "http://localhost/opencart_test/index.php?route=account/login"
EMAIL = "thuthuylac79@gmail.com"
PASSWORD = "ThuThuyLac99"

def test_tc02_return_validation_error(page: Page):
    login_p = LoginPage(page)
    acc_p = MyAccountPage(page)
    return_p = ReturnPage(page)

    # 1. Login & Vào form
    print("--- 1. Login & Vao Form ---")
    login_p.navigate(BASE_URL)
    login_p.login(EMAIL, PASSWORD)
    acc_p.go_to_order_history()
    acc_p.go_to_return_form()

    # 2. Bấm Submit LUÔN (Cố tình KHÔNG chọn lý do)
    print("--- 2. Bam Submit (De kich hoat loi) ---")
    return_p.submit()

    # 3. Verify (Kiểm tra dòng chữ đỏ xuất hiện)
    print("--- 3. Kiem tra thong bao loi ---")
    
    # Định vị chính xác dòng chữ trong ảnh bạn gửi
    error_message = page.get_by_text("You must select a return product reason!")
    
    # Chờ dòng chữ đó hiện ra (Visible)
    expect(error_message).to_be_visible()
    
    # Kiểm tra thêm: Phải vẫn đứng yên ở trang này (chưa qua trang Success)
    expect(page.locator("h1")).to_contain_text("Returns")
    
    print("\n>>> TEST PASSED: He thong da hien loi 'You must select a return product reason!' dung nhu mong doi!")