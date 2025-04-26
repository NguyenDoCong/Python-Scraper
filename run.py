from config import Config
from src.utils.downloader import batch_download_from_file

def fb_videos_scraper(id = "official.parkhangseo"):
    from src.facebook.account.account_videos import AccountVideo
    
    videos_scraper = AccountVideo(id)
    videos_scraper.save_video_urls_to_database_pipeline()
    batch_download_from_file(Config.FACEBOOK_FILE_PATH)

def ins_videos_scraper(id = "baukrysie"):
    from src.instagram.instagram_profile import ProfileScraper    
    scraper = ProfileScraper(id)
    scraper.pipeline_videos()
    batch_download_from_file(Config.INSTAGRAM_FILE_PATH)

def x_login():
    from playwright.sync_api import sync_playwright
    # from config import Config

    username = Config.X_USERNAME
    password = Config.X_PASSWORD

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://twitter.com/i/flow/login?redirect_after_login=%2Fhome")

        page.wait_for_selector("input[autocomplete='username']", timeout=10000)
        page.fill("input[autocomplete='username']", username)
        page.get_by_role("button", name="Next").click()

        page.wait_for_selector("input[name='password']", timeout=10000)
        page.fill("input[name='password']", password)
        page.get_by_test_id("LoginForm_Login_Button").click()

        page.wait_for_url("**/home", timeout=300000)
        print("[INFO] Final URL:", page.url)

        # Save storage state into the file.
        storage = context.storage_state(path="state.json")

def x_videos_scraper(id = "elonmusk",scrolls = 5):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(storage_state="state.json")
        page = context.new_page() 

        # Truy cập trang cá nhân
        page.goto(f"https://x.com/{id}/media", timeout=15000)

        page.wait_for_timeout(5000)  # chờ page load

        hrefs = []
        # Cuộn xuống để tải thêm tweets
        for i in range(scrolls):
            print(f"Scrolling down... {i}")
            old_links = set(hrefs)
                
            # Cuộn bằng JS
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            page.wait_for_timeout(5000)

            # Kiểm tra tất cả <a> sau khi load
            for element in page.locator("a").all():
                link = element.get_attribute("href")
                if link and "/video/" in link:
                    full_link = f"https://x.com{link}"
                    if full_link not in hrefs:
                        hrefs.append(full_link)
                        print(full_link)

            if set(hrefs) == old_links:
                break
                    
        with open(Config.X_FILE_PATH, "w",encoding='utf-8') as f:
                        for item in hrefs:
                            f.write(f"{item}\n")

        context.close()
        browser.close()
    batch_download_from_file(Config.X_FILE_PATH)

def tiktok_videos_scraper(id = "therock",count = 10):
    from TikTokApi import TikTokApi
    import asyncio
    import os
    # import json
    from config import Config
    ms_token = os.environ.get(
    "ms_token", None
    )  # set your own ms_token, think it might need to have visited a profile
    ms_token = Config.MS_TOKENS
    
    async def user_example():
        async with TikTokApi() as api:
            # Đổi ms_tokens nếu bị lỗi chạy headless
            await api.create_sessions(ms_tokens=ms_token, num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "chromium"))
            user = api.user(f"{id}")
            videos=[]
            async for video in user.videos(count=count):
                print(f"https://www.tiktok.com/@{id}/video/"+video.as_dict['id'])
                videos.append(f"https://www.tiktok.com/@{id}/video/"+video.as_dict['id'])
                with open(Config.TIKTOK_ERROR_FILE_PATH, "w",encoding='utf-8') as f:
                    f.write(f"{video}\n")
                
            with open(Config.TIKTOK_FILE_PATH, "w",encoding='utf-8') as f:
                for item in videos:
                    f.write(f"{item}\n")
            batch_download_from_file(Config.TIKTOK_FILE_PATH, tiktok=True)
    asyncio.run(user_example())

def fb_save_cookies():
    from src.facebook.login import FacebookLogIn
    facebook = FacebookLogIn()
    facebook.login_2_step_pipeline()

if __name__ == "__main__":

    # fb_videos_scraper(id = "official.parkhangseo")
    # ins_videos_scraper(id = "baukrysie")
    # x_videos_scraper(id = "BillGates", scrolls=10)
    tiktok_videos_scraper(id = "kenh14official", count=2)
    # fb_save_cookies()
    # x_login()



    
