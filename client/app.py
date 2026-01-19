"""Client - Menu-based interface for text processing requests."""
import requests
import sys

CENTRAL_SERVER_URL = "http://central_server:5000"

MENU_OPTIONS = {
    '1': ('uppercase', 'Convert text to UPPERCASE'),
    '2': ('lowercase', 'Convert text to lowercase'),
    '3': ('reverse', 'Reverse text'),
    '4': ('wordcount', 'Count number of words'),
    '5': (None, 'Exit')
}


def display_menu():
    """Display the menu options."""
    print("\n" + "=" * 40)
    print("   Text Processing Service Menu")
    print("=" * 40)
    for key, (_, description) in MENU_OPTIONS.items():
        print(f"  {key}. {description}")
    print("=" * 40)


def get_user_choice():
    """Get user's menu choice."""
    while True:
        choice = input("Enter choice: ").strip()
        if choice in MENU_OPTIONS:
            return choice
        print("Error: Invalid choice. Please enter a number between 1-5.")


def get_user_text():
    """Get text input from user."""
    return input("Enter text: ")


def send_request(operation, text):
    """Send processing request to central server."""
    try:
        response = requests.post(
            f"{CENTRAL_SERVER_URL}/process",
            json={"operation": operation, "text": text},
            timeout=15
        )
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to central server. Please try again later."}, 503
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}, 504
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}, 500


def main():
    """Main client loop."""
    print("\nWelcome to the Distributed Text Processing Service!")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '5':
            print("Exiting...")
            sys.exit(0)

        operation, _ = MENU_OPTIONS[choice]
        text = get_user_text()

        # Validate empty input on client side
        if not text or text.strip() == '':
            print("Error: Input text cannot be empty")
            continue

        # Send request to central server
        response, status_code = send_request(operation, text)

        if 'error' in response:
            print(f"Error: {response['error']}")
        else:
            print(f"Result: {response['result']}")


if __name__ == '__main__':
    main()
