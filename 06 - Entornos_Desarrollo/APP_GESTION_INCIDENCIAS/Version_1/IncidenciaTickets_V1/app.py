from service import Service

def print_separator() -> None:
    print("\n" + "=" * 60 + "\n")

def main()->None:
    service = Service()

    service.close_ticket(1)
    print_separator()
    print("Listar todos los tickets")
    for ticket in service.get_all_tickets():
        print(ticket)

    print_separator()
    print("6. Lista los tickets abiertos..")
    for ticket in service.get_open_tickets():
        print(ticket)


if __name__ == "__main__":
    main()