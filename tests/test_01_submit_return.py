from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.return_page import ReturnPage

# --- DỮ LIỆU ---
BASE_URL = "http://localhost/opencart_test/index.php?route=account/login"
EMAIL = "thuthuylac79@gmail.com"
PASSWORD = "ThuThuyLac99"
SUCCESS_TEXT = "Thank you for submitting your return request"

def test_tc01_submit_return_happy_case(page: Page):
    login_p = LoginPage(page)
    acc_p = MyAccountPage(page)
    return_p = ReturnPage(page)

    # 1. Login
    print("--- Buoc 1: Dang nhap ---")
    login_p.navigate(BASE_URL)
    login_p.login(EMAIL, PASSWORD)
    
    # 2. Vào form
    print("--- Buoc 2: Vao form tra hang ---")
    acc_p.go_to_order_history()
    acc_p.go_to_return_form()

    # Checkpoint
    print("--- Checkpoint: Dang o trang Returns ---")
    expect(page.locator("h1")).to_contain_text("Returns")

    # 3. Điền form
    print("--- Buoc 3: Dien thong tin ---")
    return_p.fill_return_form("Test Automation - Hang bi hong (Happy Case)")
    
    # 4. Submit
    print("--- Buoc 4: Bam nut Submit ---")
    return_p.submit()

    # 5. Verify Success (SỬA LẠI ĐOẠN NÀY)
    print("--- Buoc 5: Kiem tra ket qua ---")
    print(f"Check: Dang tim dong chu '{SUCCESS_TEXT}'...")
    
    
    expect(page.get_by_text(SUCCESS_TEXT)).to_be_visible(timeout=10000)
    
    print("\n>>> SUCCESS: CHUC MUNG! TEST CASE 01 DA PASSED (Da thay thong bao Thank You)!")