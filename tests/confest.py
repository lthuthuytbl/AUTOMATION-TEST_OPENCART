import pytest
from datetime import datetime
import os
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        # slow_mo=1000: Chậm 1 giây mỗi bước để bạn kịp nhìn
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

# 1. Đặt tên báo cáo cho đẹp
def pytest_html_report_title(report):
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    report.title = f"Automation Report | OpenCart | {now}"

# 2. Hook quan trọng: Chụp ảnh và dán vào báo cáo khi FAIL
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        # Luôn thêm log output vào báo cáo
        extra.append(pytest_html.extras.url("http://localhost/opencart_test/"))
        
        # Nếu test thất bại (Failed)
        if report.failed:
            # Tìm đối tượng 'page' trong test case
            page = item.funcargs.get("page")
            if page:
                # Chụp ảnh màn hình
                screenshot_bytes = page.screenshot()
                # Đính kèm ảnh vào báo cáo HTML (dạng base64 - xem được ngay không cần file ảnh)
                extra.append(pytest_html.extras.image(screenshot_bytes, "Screenshot Lỗi"))
                
                # Nếu có video thì đính kèm video (Optional - cần config video dir)
                video_path = page.video.path()
                if video_path: extra.append(pytest_html.extras.html(f'<a href="{video_path}" target="_blank">Xem Video Lỗi</a>'))

        report.extra = extra