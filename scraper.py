from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for year in range(1970, 1975):

        page.goto("https://dl.nanet.go.kr/")
        searchForm = page.locator("#searchQuery")

        # uses year + 1 because yearbooks are written
        # based on previous year's statistics
        search = f"한국통계연감{year + 1}"
        page.fill("#searchQuery", search)
        page.press("#searchQuery", "Enter")
        page.wait_for_load_state("load")

        download_button = page.locator(".btnD.ty1").nth(1)

        with page.expect_download() as download_info:
            # known error: searches occasionally do not appear first
            # manually click when necessary
            # (add check for list head text content)
            download_button.click()
            download = download_info.value

            path = "/Users/jeff/Desktop/korea-statistical-yearbooks/"
            download.save_as(f"{path}{year}-education-yearbook.pdf")
    
    browser.close()