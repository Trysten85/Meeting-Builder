"""
Meeting Time Calculator Module
Contains all the calculation logic for finding optimal meeting times.
Based on your classmate's original algorithm with GUI integration.
"""

# Global list to store participant data (matches your classmate's original design)
participants = []

# ========================
# CORE ALGORITHM FUNCTIONS (Your classmate's original logic)
# ========================

def find_top_meeting_time():
    """
    Your classmate's original function - slightly modified to return results and handle ties
    Finds the most popular time slot across all participants
    """
    time_votes = {}

    for person in participants:
        for time in person['best_times']:
            if time in time_votes:
                time_votes[time] += 1
            else:
                time_votes[time] = 1

    if not time_votes:
        return "No best time slots were chosen."

    # Find the maximum number of votes
    max_votes = max(time_votes.values())
    
    # Find all time slots with the maximum votes (handles ties)
    top_times = [time for time, votes in time_votes.items() if votes == max_votes]
    
    if len(top_times) == 1:
        return f"{top_times[0]} ({max_votes} vote{'s' if max_votes > 1 else ''})"
    else:
        times_str = ", ".join(top_times)
        return f"TIE: {times_str} (each with {max_votes} vote{'s' if max_votes > 1 else ''})"

def find_best_time_day_one():
    """Find the best meeting time for day one only"""
    time_votes = {}

    for person in participants:
        times_to_check = person.get('day_one_times', [])
        for time in times_to_check:
            if time in time_votes:
                time_votes[time] += 1
            else:
                time_votes[time] = 1

    if not time_votes:
        return "No day one times selected"

    max_votes = max(time_votes.values())
    top_times = [time for time, votes in time_votes.items() if votes == max_votes]
    
    if len(top_times) == 1:
        return f"{top_times[0]} ({max_votes} vote{'s' if max_votes > 1 else ''})"
    else:
        times_str = ", ".join(top_times)
        return f"TIE: {times_str} (each with {max_votes} vote{'s' if max_votes > 1 else ''})"

def find_best_time_day_two():
    """Find the best meeting time for day two only"""
    time_votes = {}

    for person in participants:
        times_to_check = person.get('day_two_times', [])
        for time in times_to_check:
            if time in time_votes:
                time_votes[time] += 1
            else:
                time_votes[time] = 1

    if not time_votes:
        return "No day two times selected"

    max_votes = max(time_votes.values())
    top_times = [time for time, votes in time_votes.items() if votes == max_votes]
    
    if len(top_times) == 1:
        return f"{top_times[0]} ({max_votes} vote{'s' if max_votes > 1 else ''})"
    else:
        times_str = ", ".join(top_times)
        return f"TIE: {times_str} (each with {max_votes} vote{'s' if max_votes > 1 else ''})"

# ========================
# DATA CONVERSION FUNCTIONS (GUI Integration)
# ========================

def convert_gui_data_to_participants(gui_data):
    """Convert GUI data format to your classmate's participants format (combined)"""
    global participants
    participants = []
    
    for user in gui_data:
        best_times = []
        
        # Add day one time slots if selected
        if user['day_one'] != "Not selected":
            day_one_slots = convert_time_range_to_slots(user['day_one'])
            best_times.extend(day_one_slots)
        
        # Add day two time slots if selected
        if user['day_two'] != "Not selected":
            day_two_slots = convert_time_range_to_slots(user['day_two'])
            best_times.extend(day_two_slots)
        
        # Remove duplicates and sort
        best_times = list(set(best_times))
        best_times = sort_time_slots(best_times)
        
        person = {
            'name': user['user'],
            'best_times': best_times,
            'worst_times': []
        }
        
        participants.append(person)

def convert_gui_data_to_participants_separate_days(gui_data):
    """Convert GUI data format but keep day one and day two separate"""
    global participants
    participants = []
    
    for user in gui_data:
        day_one_times = []
        day_two_times = []
        
        # Add day one time slots if selected
        if user['day_one'] != "Not selected":
            day_one_slots = convert_time_range_to_slots(user['day_one'])
            day_one_times.extend(day_one_slots)
        
        # Add day two time slots if selected
        if user['day_two'] != "Not selected":
            day_two_slots = convert_time_range_to_slots(user['day_two'])
            day_two_times.extend(day_two_slots)
        
        # Remove duplicates and sort
        day_one_times = sort_time_slots(list(set(day_one_times)))
        day_two_times = sort_time_slots(list(set(day_two_times)))
        
        person = {
            'name': user['user'],
            'best_times': day_one_times + day_two_times,  # Combined for compatibility
            'day_one_times': day_one_times,
            'day_two_times': day_two_times,
            'worst_times': []
        }
        
        participants.append(person)

# ========================
# TIME UTILITY FUNCTIONS
# ========================

def convert_time_range_to_slots(time_range):
    """Convert a time range like '9:00 AM - 2:00 PM' into hourly slots"""
    if time_range == "Not selected" or " - " not in time_range:
        return []
    
    try:
        start_str, end_str = time_range.split(" - ")
        
        start_hour = convert_to_24_hour(start_str)
        end_hour = convert_to_24_hour(end_str)
        
        # Generate hourly slots
        slots = []
        current_hour = start_hour
        
        while current_hour < end_hour:
            next_hour = current_hour + 1
            start_12h = convert_to_12_hour(current_hour)
            end_12h = convert_to_12_hour(next_hour)
            slot = f"{start_12h} - {end_12h}"
            slots.append(slot)
            current_hour = next_hour
        
        return slots
    except Exception as e:
        print(f"Error parsing time range '{time_range}': {e}")
        return [time_range]

def convert_to_24_hour(time_str):
    """Convert '9:00 AM' to 9, '2:00 PM' to 14, etc."""
    time_str = time_str.strip()
    if 'AM' in time_str:
        hour = int(time_str.replace('AM', '').replace(':00', '').strip())
        return hour if hour != 12 else 0
    elif 'PM' in time_str:
        hour = int(time_str.replace('PM', '').replace(':00', '').strip())
        return hour if hour == 12 else hour + 12
    return 0

def convert_to_12_hour(hour_24):
    """Convert 9 to '9:00 AM', 14 to '2:00 PM', etc."""
    if hour_24 == 0:
        return "12:00 AM"
    elif hour_24 < 12:
        return f"{hour_24}:00 AM"
    elif hour_24 == 12:
        return "12:00 PM"
    else:
        return f"{hour_24 - 12}:00 PM"

def sort_time_slots(time_slots):
    """Sort time slots chronologically"""
    def get_start_hour(slot):
        try:
            start_time = slot.split(" - ")[0]
            return convert_to_24_hour(start_time)
        except:
            return 0
    
    return sorted(time_slots, key=get_start_hour)

# ========================
# HIGH-LEVEL API FUNCTIONS (What your GUI should call)
# ========================

def calculate_combined_best_time(gui_data):
    """
    High-level function: Calculate the single best time across both days
    Returns: string with the best time result
    """
    convert_gui_data_to_participants(gui_data)
    return find_top_meeting_time()

def calculate_separate_day_times(gui_data):
    """
    High-level function: Calculate separate best times for each day
    Returns: tuple of (day_one_result, day_two_result)
    """
    convert_gui_data_to_participants_separate_days(gui_data)
    day_one_result = find_best_time_day_one()
    day_two_result = find_best_time_day_two()
    return day_one_result, day_two_result

def get_participants_data():
    """Get the current participants data (for debugging)"""
    return participants

def print_debug_info():
    """Print debug information about current participants"""
    print("=== Current Participants Data ===")
    for person in participants:
        print(f"Name: {person['name']}")
        if 'day_one_times' in person:
            print(f"  Day One times: {person['day_one_times']}")
            print(f"  Day Two times: {person['day_two_times']}")
        else:
            print(f"  Best times (combined): {person['best_times']}")
        print(f"  Worst times: {person['worst_times']}")
        print()

# ========================
# ORIGINAL CLASSMATE FUNCTIONS (For command-line use)
# ========================

def collect_availability():
    """Your classmate's original data collection function"""
    print("Enter each person's availability. Type 'done' when you are finished.\n")
    global participants
    participants = []
    
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

def main():
    """Your classmate's original main function"""
    print("=== Meeting Time Picker ===\n")
    collect_availability()
    result = find_top_meeting_time()
    print(f"\nMost popular meeting time: {result}")

if __name__ == "__main__":
    main()