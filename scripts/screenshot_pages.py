#!/usr/bin/env python3
"""
项目报价系统操作手册 - 自动截图脚本 (v2)
"""
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://10.60.100.1:8080"
OUT_DIR = Path("/home/rs8568/project-quote-system/docs/manual_screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHROME = "/home/rs8568/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome"

ACCOUNTS = {
    "admin":    ("admin",    "admin123",    "管理员",   "01_admin"),
    "manager":  ("manager",  "manager123",  "报价经理", "02_manager"),
    "business": ("sales",    "sales123",    "业务员",   "03_business"),
    "viewer":   ("viewer",   "viewer123",   "查看者",   "04_viewer"),
}

COMMON_PAGES = [
    ("01_login",            "/login",                  "login"),
    ("02_dashboard",        "/dashboard",              "dashboard"),
    ("03_quotations_list",  "/quotations",             "quotations"),
    ("04_my_assignments",   "/my-assignments",         "assignments"),
    ("05_messages",         "/messages",               "messages"),
    ("06_pending_approvals","/pending-approvals",      "pending"),
]

QUOTATION_ID = 3  # 主板锁螺丝机 (status=draft, 否则 view 会重定向回 /quotations)
VIEW_TABS = [
    ("01_basic",       "基本信息"),
    ("02_modules",     "模块管理"),
    ("03_participants","参与人员"),
    ("04_fees",        "费用"),
    ("05_labor",       "人力工时"),
    ("06_materials",   "物料清单"),     # agency/electrical 可见
    ("07_packing",     "运输包装"),
    ("08_travel_days", "差旅人天"),
    ("09_travel_trips","差旅人次"),
    ("10_versions",    "版本"),
    ("11_export",      "导出"),
    ("12_summary",     "汇总"),
    ("13_coefficients","费用系数"),     # admin 全权限可见 (but not project type 默认)
]

ADMIN_PAGES = [
    ("10_users",              "/users",                          "users"),
    ("11_roles",              "/roles",                          "roles"),
    ("12_system",             "/system",                         "system"),
    ("13_participant_types",  "/participant-type-permissions",   "ptype_perms"),
    ("14_materials",          "/materials",                      "materials"),
    ("15_fee_types",          "/fee-types",                      "fee_types"),
    ("16_fee_rates",          "/fee-rates",                      "fee_rates"),
    ("17_exchange_rates",     "/exchange-rates",                 "exchange_rates"),
    ("18_travel_fee_config",  "/travel-fee-config",              "travel_fee"),
    ("19_logs",               "/logs",                           "logs"),
    ("20_ai_assistant",       "/ai-chat",                        "ai_chat"),
    ("21_trends",             "/trends",                         "trends"),
]

def login(page, username, password):
    page.goto(f"{BASE}/login", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_selector('input[placeholder="请输入用户名"]', timeout=10000)
    page.fill('input[placeholder="请输入用户名"]', username)
    page.fill('input[placeholder="请输入密码"]', password)
    page.click('button:has-text("登 录")')
    page.wait_for_url(f"{BASE}/dashboard", timeout=10000)

def shot(page, name, full_page=True):
    path = OUT_DIR / f"{name}.png"
    page.screenshot(path=str(path), full_page=full_page)
    print(f"  ✓ {name}.png ({path.stat().st_size//1024} KB)")

def click_tab(page, tab_label):
    try:
        # 用 js 找 el-tab-pane 的 label, 不存在返回 False
        return page.evaluate(f"""() => {{
            const items = document.querySelectorAll('.el-tabs__item');
            for (const it of items) {{
                if (it.textContent.trim() === '{tab_label}') {{ it.click(); return true; }}
            }}
            return false;
        }}""")
    except Exception as e:
        print(f"  click_tab error: {e}")
        return False
    except Exception:
        page.click(f'.el-tabs__item:has-text("{tab_label}")')
    page.wait_for_timeout(800)

def shot_role(playwright, role_key, account):
    username, password, real_name, label = account
    print(f"\n=== {role_key} ({real_name}) ===")

    browser = playwright.chromium.launch(executable_path=CHROME, headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.set_default_timeout(15000)

    prefix = label

    # 登录页
    page.goto(f"{BASE}/login", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(800)
    shot(page, f"{prefix}_00_login")

    # 登录
    login(page, username, password)
    page.wait_for_timeout(1000)

    # 通用页面
    for name, path, _ in COMMON_PAGES:
        if name == "01_login":
            continue  # 已截过
        try:
            page.goto(f"{BASE}{path}", wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(1500)
            shot(page, f"{prefix}_{name}")
        except Exception as e:
            print(f"  ✗ {path}: {e}")

    # 报价单 view (13 tab)
    try:
        # 用 vue-router push 而非 hard goto, 避免权限重定向
        page.goto(f"{BASE}/quotations/{QUOTATION_ID}/view", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        # 检测是否真的到了 view 页 (h1 包含"编辑报价单"或"查看报价单")
        h1 = page.text_content("h1.page-title, h1") or ""
        print(f"  [view page] h1={h1.strip()[:50]!r}")
        for tab_name, tab_label in VIEW_TABS:
            try:
                clicked = click_tab(page, tab_label)
                if not clicked:
                    print(f"  - tab/{tab_label}: 不存在, 跳过")
                    continue
                page.wait_for_timeout(1200)
                shot(page, f"{prefix}_20_view_{tab_name}")
            except Exception as e:
                print(f"  ✗ tab/{tab_label}: {e}")
    except Exception as e:
        print(f"  ✗ view: {e}")

    # 报价单 edit (admin 全权限可见) - SKIP, view 已涵盖 UI, edit 多"保存"按钮
    # if role_key == "admin":
    #     try:
    #         page.goto(f"{BASE}/quotations/{QUOTATION_ID}/edit", wait_until="domcontentloaded", timeout=15000)
    #         page.wait_for_timeout(2500)
    #         for tab_name, tab_label in VIEW_TABS:
    #             try:
    #                 click_tab(page, tab_label)
    #                 page.wait_for_timeout(1200)
    #                 shot(page, f"{prefix}_21_edit_{tab_name}")
    #             except Exception as e:
    #                 print(f"  ✗ edit/{tab_label}: {e}")
    #     except Exception as e:
    #         print(f"  ✗ edit: {e}")

    # admin 管理页
    if role_key == "admin":
        for name, path, _ in ADMIN_PAGES:
            try:
                page.goto(f"{BASE}{path}", wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(1500)
                shot(page, f"{prefix}_30_admin_{name}")
            except Exception as e:
                print(f"  ✗ admin/{path}: {e}")

    context.close()
    browser.close()

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None

    with sync_playwright() as p:
        for role_key, account in ACCOUNTS.items():
            if target and role_key != target:
                continue
            try:
                shot_role(p, role_key, account)
            except Exception as e:
                print(f"!! 角色 {role_key} 失败: {e}")

    n = len(list(OUT_DIR.glob("*.png")))
    print(f"\n✅ {n} 张截图保存到: {OUT_DIR}")

if __name__ == "__main__":
    main()