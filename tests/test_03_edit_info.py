import pytest
import datetime
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.return_page import ReturnPage

# --- DỮ LIỆU ---
BASE_URL = "http://localhost/opencart_test/index.php?route=account/login"
EMAIL = "thuthuylac79@gmail.com"
PASSWORD = "ThuThuyLac99"
# Dòng thông báo chính xác bạn vừa gửi
SUCCESS_MSG = "Thank you for submitting your return request" 

# --- HÀM KIỂM TRA "SĂN BUG" ---
def check_negative_case(page, test_name):
    """
    Dùng cho các case nhập SAI.
    Nếu thấy thông báo thành công -> BÁO BUG NGAY LẬP TỨC.
    """
    print(f"Check: Dang kiem tra xem he thong co lo tay chap nhan {test_name} khong...")
    page.wait_for_timeout(1000)
    
    # Tìm dòng chữ "Thank you..."
    if page.get_by_text(SUCCESS_MSG).is_visible():
        # Nếu thấy -> Nghĩa là hệ thống nhận đơn sai -> BUG
        pytest.fail(f">>> BUG FOUND: He thong da chap nhan tra hang du {test_name}!")
    else:
        # Nếu không thấy -> Nghĩa là hệ thống đã chặn lại -> TỐT
        print(f"   -> OK: He thong da chan lai (Khong hien Success).")

# =========================================================================
# CASE A: TEST LỖI - TÊN RỖNG (Mong đợi chặn lại)
# =========================================================================
def test_tc03_case_a_empty_name(page: Page):
    print("\n--- [CASE A] Test: Ten Rong ---")
    login_p = LoginPage(page)
    acc_p = MyAccountPage(page)
    return_p = ReturnPage(page)

    login_p.navigate(BASE_URL)
    login_p.login(EMAIL, PASSWORD)
    acc_p.go_to_order_history()
    acc_p.go_to_return_form()
    return_p.prepare_form_basics() # Tick lý do trước

    # Action: Xóa tên
    return_p.edit_personal_info(firstname="", lastname="Lac")
    return_p.submit()

    # Check Bug (Nếu thấy Success là Fail)
    check_negative_case(page, "TEN RONG")
    
    # Kiểm tra thêm: Phải hiện lỗi text đỏ
    if not page.get_by_text(SUCCESS_MSG).is_visible():
        expect(page.get_by_text("First Name must be between")).to_be_visible()

# =========================================================================
# CASE B: TEST LỖI - SỐ LƯỢNG = 0 (Mong đợi chặn lại)
# =========================================================================
def test_tc03_case_b_zero_quantity(page: Page):
    print("\n--- [CASE B] Test: So Luong = 0 ---")
    login_p = LoginPage(page)
    acc_p = MyAccountPage(page)
    return_p = ReturnPage(page)

    login_p.navigate(BASE_URL)
    login_p.login(EMAIL, PASSWORD)
    acc_p.go_to_order_history()
    acc_p.go_to_return_form()
    return_p.prepare_form_basics()

    # Action: Nhập số lượng 0
    return_p.edit_order_info(quantity="0")
    return_p.submit()

    # Check Bug
    check_negative_case(page, "SO LUONG = 0")

# =========================================================================
# CASE C: TEST LỖI - NGÀY TƯƠNG LAI (Mong đợi chặn lại)
# =========================================================================
def test_tc03_case_c_future_date(page: Page):
    print("\n--- [CASE C] Test: Ngay Tuong Lai ---")
    login_p = LoginPage(page)
    acc_p = MyAccountPage(page)
    return_p = ReturnPage(page)

    login_p.navigate(BASE_URL)
    login_p.login(EMAIL, PASSWORD)
    acc_p.go_to_order_history()
    acc_p.go_to_return_form()
    return_p.prepare_form_basics()

    # Tính ngày mai
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Action: Nhập ngày mai
    return_p.edit_order_info(date_ordered=tomorrow)
    return_p.submit()

    # Check Bug: Nếu hệ thống nhận ngày mai -> BÁO LỖI ĐỎ NGAY
    check_negative_case(page, f"NGAY TUONG LAI ({tomorrow})")

# =========================================================================
# CASE D: TEST THÀNH CÔNG - NHẬP ĐÚNG (Mong đợi Success)
# =========================================================================
def test_tc03_case_d_valid_submit(page: Page):
    print("\n--- [CASE D] Test: Nhap Dung ---")
    login_p = LoginPage(page)
    acc_p = MyAccountPage(page)
    return_p = ReturnPage(page)

    login_p.navigate(BASE_URL)
    login_p.login(EMAIL, PASSWORD)
    acc_p.go_to_order_history()
    acc_p.go_to_return_form()
    return_p.prepare_form_basics()

    # Action: Điền đúng
    today = datetime.date.today().strftime("%Y-%m-%d")
    return_p.edit_personal_info(firstname="Thuy", lastname="Lac")
    return_p.edit_order_info(quantity="1", date_ordered=today)
    
    return_p.submit()

    # Check Success: Ở đây ta LẠI MONG thấy chữ Thank you
    print("Check: Mong doi trang Success hien ra...")
    page.wait_for_timeout(1000)
    expect(page.get_by_text(SUCCESS_MSG)).to_be_visible()
    print(">>> PASSED: Quy trinh Validate hoan tat!")