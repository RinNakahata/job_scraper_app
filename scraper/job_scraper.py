import asyncio
import os
import pandas as pd
from playwright.async_api import async_playwright
from urllib.parse import quote

BASE_URL = "https://xn--pckua2a7gp15o89zb.com"  # 求人ボックスの基本URL
all_job_data = []  # 全求人情報を格納するリスト


def create_search_path(keyword, location, employment_type):
    # ユーザー入力をURLエンコードして検索URLを構築
    encoded_keyword = quote(keyword)
    encoded_location = quote(location)
    return f"/{encoded_keyword}の仕事-{encoded_location}?e={employment_type}"


async def extract_job_details(page, url):
    # 求人詳細ページにアクセスして情報を取得
    try:
        await page.goto(url, timeout=60000)

        # 指定したCSSセレクタからテキストを取得する内部関数
        async def get_text(selector):
            locator = page.locator(selector)
            try:
                if await locator.count() > 0:
                    content = await locator.text_content()
                    return content.strip() if content else ""
                else:
                    return ""
            except Exception:
                return ""

        # 各情報を辞書にまとめて返す
        return {
            "求人タイトル": await get_text("p.p-detail_head_title"),
            "企業名": await get_text("p.p-detail_head_company"),
            "所在地": await get_text("li.p-detail_summary.p-detail_summary-area.c-icon--U2"),
            "給与": await get_text("li.p-detail_summary.p-detail_summary-pay.c-icon--V2"),
            "雇用形態": await get_text("li.p-detail_tag.p-detail_tag-employType"),
        }

    except Exception as e:
        print(f"エラー: {e}（URL: {url}）")
        return None


async def scrape_page(page, url):
    # 一覧ページから各求人の詳細ページURLを抽出し、詳細情報を取得
    await page.goto(url)
    await page.wait_for_selector('[data-target-focus]')

    # 各求人のIDを取得（data-target-focus 属性から）
    job_ids = await page.locator('[data-target-focus]').evaluate_all(
        """(elements) => elements.map(el => el.getAttribute('data-target-focus')).filter(id => id);"""
    )

    detail_urls = [f"{BASE_URL}/jb/{job_id}" for job_id in job_ids]
    print(f"[INFO] スクレイピング対象URL: {url} - 求人数: {len(detail_urls)}")

    # 各詳細ページにアクセスして情報収集
    for detail_url in detail_urls:
        job_info = await extract_job_details(page, detail_url)
        if job_info:
            all_job_data.append(job_info)


async def scrape_main(keyword, location, employment_type):
    global all_job_data
    all_job_data = []  # 前回のデータをリセット

    search_path = create_search_path(
        keyword, location, employment_type)  # 検索条件でURL構築

    # Playwright のブラウザ起動
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # ヘッドレスモード（非表示）
        page = await browser.new_page()

        # 最初の2ページ分を対象にスクレイピング実行
        for page_num in range(1, 3):
            full_url = f"{BASE_URL}{search_path}&pg={page_num}"
            await scrape_page(page, full_url)

        await browser.close()  # ブラウザを閉じる

    # 出力用フォルダ作成とExcelファイルへの保存
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "求人情報一覧.xlsx")
    df = pd.DataFrame(all_job_data)
    df.to_excel(output_path, index=False)
    print(f"[INFO] Excelに保存完了: {output_path}")
