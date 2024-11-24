import argparse

def main(option, autre_option):
    print(f"Option: {option}")
    print(f"Autre option: {autre_option}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description de votre script.")
    parser.add_argument('-option', type=str, required=True, help='Description de l\'option')
    parser.add_argument('-autre', type=str, required=True, help='Description de l\'autre option')

    args = parser.parse_args()
    main(args.option, args.autre)
