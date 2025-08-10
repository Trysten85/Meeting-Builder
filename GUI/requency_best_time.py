#Creates an empty list to store the availability info for each person and each person’s info will be stored as a dictionary inside this list.
participants = []

#Prompts the user to enter each participant’s name, their best times, and worst times.
def collect_availability():
    #This dictionary is added to the participants list the loop goes on until the user types "done".
    print("Enter each person's availability. Type 'done' when  you are finished.\n")
    while True:
        name = input("Name: ")
        if name.strip().lower() == 'done':
            break

        best_input = input("Best times (EX: 9-10am, 2-3pm): ")
        worst_input = input("Worst times (EX: 12-1pm, 4-5pm): ")

        best_times = [slot.strip() for slot in best_input.split(',') if slot.strip()]
        worst_times = [slot.strip() for slot in worst_input.split(',') if slot.strip()]

        person = {
            'name': name,
            'best_times': best_times,
            'worst_times': worst_times
        }

        participants.append(person)
        print()

def find_top_meeting_time():
    #Creates a dictionary to keep track of how many times each time slot was marked as a best time
    time_votes = {}

    for person in participants:
        for time in person['best_times']:
            if time in time_votes:
                time_votes[time] += 1
            else:
                time_votes[time] = 1

    if not time_votes:
        print("No best time slots were chosen.")
        return

    top_time = max(time_votes, key=time_votes.get)
    votes = time_votes[top_time]
    print(f"\nMost popular meeting time: {top_time} ({votes} vote{'s' if votes > 1 else ''})")

def main():
    #gathers everyones input and calculates and displays the best meeting time
    print("=== Meeting Time Picker ===\n")
    collect_availability()
    find_top_meeting_time()

if __name__ == "__main__":
    main()
