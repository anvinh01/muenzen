from playwright.sync_api import Page, expect
import random


def scenario(page: Page, num_scenario: int) -> None:
    """
    Scenario to throw a coin. for each scenario
    :param page:
    :param num_scenario:
    :return: None
    """
    # Click the button to throw a coin
    page.get_by_role("button", name=f"{num_scenario}-Mal werfen").click()

    choices = []        # later to check if your selections are correct

    # Choose randomly between Kopf and Zahl for the number of scenarios
    for curr_scenario in range(num_scenario):
        # Expects page to have 2 cards with "Kopf" or "Zahl" and a Text inbetween them
        expect(page.get_by_role("heading", name="Oder")).to_be_visible()
        expect(page.get_by_role("button", name="Kopf")).to_be_visible()
        expect(page.get_by_role("button", name="Zahl")).to_be_visible()

        # count the selections
        # The unknown selections are in the class "unknown" (not selected yet)
        # The selected selections are in the class "Kopf" or "Zahl"
        assert page.locator(".unknown").count() == num_scenario - curr_scenario
        assert page.locator(".Kopf").count() == choices.count("Kopf")
        assert page.locator(".Zahl").count() == choices.count("Zahl")

        # Click "Kopf" or "Zahl" randomly
        temp_choice = random.choice(["Kopf", "Zahl"])               # Choices name in the UI
        page.get_by_role("button", name=temp_choice).click()
        choices.append(temp_choice)

    # Check if the selections are correct
    expect(page.get_by_role("heading", name="Fertig!")).to_be_visible()
    assert page.locator(".Kopf").count() == choices.count("Kopf")
    assert page.locator(".Zahl").count() == choices.count("Zahl")
    assert page.locator(".unknown").count() == 0

    # Click the button "Bestätigen"
    # TODO: Create a test for the POST-Request
    page.get_by_role("button", name="Bestätigen").click()

    # Expects page to be back at the selection page
    expect(page.get_by_role("heading", name="Deine Aufgabe")).to_be_visible()


async def test_load_page(page: Page):
    browser = await playwright.safari.launch(headless=False)
    page.goto("http://localhost:5173/")

    # Expects page to have a heading with the name of Münzwurf
    expect(page.get_by_role("heading", name="Münzwurf"))

    # Click the button "Zum Münzwurf"
    page.get_by_role("link", name="Zum Münzwurf").click()

    # Expects page to have a heading with the name of Münzwurf
    expect(page.get_by_role("heading", name="Deine Aufgabe")).to_be_visible()

    # Check the Selection works for 8, 10 and 20 scenarios
    for num_scenario in [8, 10, 20]:
        scenario(page, num_scenario)
