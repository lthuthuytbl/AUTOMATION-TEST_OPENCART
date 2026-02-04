from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Locator lấy từ code record của bạn
        self.email_input = page.get_by_role("textbox", name="E-Mail Address")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_btn = page.get_by_role("button", name="Login")

    def login(self, email, password):
        print(f"Action: Login voi {email}")
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.login_btn)