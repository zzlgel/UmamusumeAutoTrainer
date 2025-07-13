from playwright.sync_api import sync_playwright
import json

# 目标URL = 'https://game.bilibili.com/tool/pd/'
# 
def capture_api_responses():
    with sync_playwright() as p:
        # 启动浏览器（无头模式）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # 启用网络请求捕获
        api_responses = []
        
        def capture_response(response):
            if "api" in response.url:  # 捕获包含API的响应
                api_responses.append({
                    "url": response.url,
                    "status": response.status,
                    "headers": response.headers,
                    "json": response.json() if response.headers.get("content-type") == "application/json" else None
                })
        
        # 创建页面并添加监听器
        page = context.new_page()
        page.on("response", capture_response)
        
        # 导航到目标页面
        page.goto("https://game.bilibili.com/tool/pd/")
        
        # 示例：点击页面上的按钮
        page.get_by_text("养成助手").click()
        
        # 等待页面加载和API响应
        page.wait_for_timeout(5000)  # 等待5秒
        
        # 保存捕获的数据
        with open("api_responses.json", "w", encoding="utf-8") as f:
            json.dump(api_responses, f, ensure_ascii=False, indent=2)
        
        # 关闭浏览器
        browser.close()

if __name__ == "__main__":
    capture_api_responses()