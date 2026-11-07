from playwright.sync_api import sync_playwright

CP="28003"
URL_MERCADONA = "https://www.mercadona.es"

def introducir_CP(page, cp:str=CP):
    """Introducir código postal en la primera página de Mercadona"""

    print(page.title())
    print(page.url)

    form = page.get_by_role("banner").locator("form")
    form.get_by_label("Código postal").fill(cp)
    with page.expect_navigation():
        form.get_by_role("button", name="ENTRAR").click()

    print(page.url)
    page.screenshot(path="foto_tienda.png")

    return page

def entrar_en_categorias(page):

    with page.expect_navigation():
        page.get_by_role("link", name="Categorías").click()

    page.locator("body").wait_for(state="visible")
    print(page.url)
    page.screenshot(path="foto_categorias.png")

    return page


def main():

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL_MERCADONA)

        page = introducir_CP(page)
        page = entrar_en_categorias(page)

        browser.close()

if __name__ == "__main__":
    main()