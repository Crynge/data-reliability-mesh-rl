from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> int:
    target = "http://127.0.0.1:4173"
    output = Path("docs/screenshots/mesh-dashboard.png")
    output.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1200}, color_scheme="dark")
        page.goto(target, wait_until="networkidle")
        page.screenshot(path=str(output), full_page=True)
        browser.close()

    print(f"screenshot saved to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

