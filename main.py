import bfs
import a_star
import service

def main():
    while True:
        print("\nChoose one of the options:")
        print("1 - Run BFS with an random initial state.")
        print("2 - Run A* with an random initial state.")
        print("3 - Run BFS and A* with the same random initial state for comparison.")
        print("q - quit.")
        print()

        user_choice = input("Enter your choice: ").strip()
        print()

        if user_choice.lower() == 'q':
            print("Exiting...")
            break

        if user_choice == '1':
            bfs.run(service.generate_random_state())

        elif user_choice == '2':
            a_star.run(service.generate_random_state())

        elif user_choice == '3':
            initial_state = service.generate_random_state()
            service.print_default_bfs()
            bfs.run(initial_state)
            service.print_default_a_star()
            a_star.run(initial_state)

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()