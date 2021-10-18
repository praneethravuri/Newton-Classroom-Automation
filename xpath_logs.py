import datetime


now = datetime.datetime.now()
current_date_time = now.strftime("%d/%m/%Y %H:%M:%S %p")


page_loaded_element = "//*[@class='layout_brandName__DDxk3']"  # Newton Classroom Top Right Logo Text

google_login_button = "//img[@alt='sign in with google']"  # Sign in with google button

email_text_box = '//*[@id="identifierId"]'  # Email input box

next_button = "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b']"  # Next button on google sign email address and password

password_text_box = "//input[@type='password']"  # Password input box

click_current_class = "//div[@class='UpcomingPeriods_period__1tBa_ UpcomingPeriods_isPresentSlot__3ZzxW']"  # Current class box

join_google_meet = "//button[@class='ant-btn Button_bold__2gfxX ant-btn-primary']"  # Join google meet button after clicking on the current class

join_now_button = "//div[@class='uArJ5e UQuaGc Y5sE8d uyXBBb xKiqt']" # Join now button in the google meet

exit_class = "//div[@class='U26fgb JRY2Pb mUbCce kpROve GaONte Qwoy0d ZPasfd vzpHY M9Bg4d']"  # Exit class button in google meet

just_leave_call = "//div[@class='U26fgb O0WRkf oG5Srb C0oVfc kHssdc uiOEcf M9Bg4d']"  # Just leave call button to be used during testing

dismiss_button = "(//div[@class='U26fgb O0WRkf oG5Srb HQ8yf C0oVfc kHssdc HvOprf DEhM1b M9Bg4d'])[2]"  # Google chrome dismiss button

div_inside_class_block = "/html/body/div[1]/div/div/section/section/main/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div[1]"  # Used for parsing through the page when there is information about the next day's classes

classes_info_class_value = "UpcomingPeriods_period__1tBa_"  # Used for paring through the page when there is no information about the next day's classes
