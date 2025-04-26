class Config:
    """
    Configuration class for the application.
    """

    # Scrolling
    SCROLL_PAUSE_TIME = 3
    MAX_CONSECUTIVE_SCROLLS = 1

    # Facebook login"
    FACEBOOK_EMAIL = "wachterson34@gmail.com"
    FACEBOOK_PASSWORD = "mqsolutions123,"
    COOKIES_FILE_PATH = "cookies/fb_cookies.json"

    # # Instagram login
    # INSTAGRAM_FILE_PATH = "instagram_cookies.json"
    INSTAGRAM_SESSIONID_VALUE = "51375314644%3AuibAf9idJuFKhk%3A16%3AAYcQFeIyaqr07UegHZNU2XUHcsU6OzFMrGpnkBBJ0w"

    # TikTok 
    TIKTOK_FILE_PATH = "scraped_data/tiktok.txt"
    TIKTOK_ERROR_FILE_PATH = "scraped_data/tiktok_error.txt"
    MS_TOKENS = ['azquqBjM67uB1DOXOvXJuaQxP1vQD8Ez_a8kDxBXNDBbLFFRE4KWUDuX-l0OjQvpgbE_dYsreYMw739sg14g8lycqGHMkEzwuWRN-L0ldYWWGwWoYs4Gw8MDxAWhEscDMqFxCSFgB3ayJ_KUoLceFA==']
    # X 
    X_FILE_PATH = "scraped_data/x.txt"
    # facebook
    FACEBOOK_FILE_PATH = "scraped_data/facebook.txt"

    # instagram
    INSTAGRAM_FILE_PATH = "scraped_data/instagram.txt"

    # logs
    LOG_FILE_PATH = "logs.log"

    # Json
    JSON_FILE_PATH = "scraped_data/"

    # # Facebook paths
    # FRIEND_LIST_URL = "friends"
    # WORK_AND_EDUCATION_URL = "about_work_and_education"
    # PLACES_URL = "about_places"
    # FAMILY_URL = "about_family_and_relationships"
    CONTACT_URL = "about_contact_and_basic_info"

    # Save to json
    INDENT = 4
    ENSURE_ASCII = False

    GMAIL = "nguyen.do.cong@mqsolutions.com.vn"
    GMAIL_PASSWORD = "123456789"
    X_USERNAME = "CongNguyen62411"
    X_PASSWORD = "mqsolutions123"