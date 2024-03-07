from datetime import datetime
import xmlrpc.client

# Connect to the server
s = xmlrpc.client.ServerProxy('http://localhost:8000')

def client_interface():
    while True:
        print("\n1. Add or Update Note")
        print("2. Get Notes by Topic")
        print("3. Search Wikipedia and Append to Topic")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            topic = input("Enter topic: ")
            note_name = input("Enter note name: ")
            text = input("Enter text: ")
            timestamp = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
            result = s.add_or_update_note(topic, note_name, text, timestamp)
            print(result)
        elif choice == '2':
            topic = input("Enter topic: ")
            notes = s.get_notes_by_topic(topic)
            if not notes:
                print("No notes found for this topic.")
            else:
                for note in notes:
                    print(f"\nNote Name: {note['name']}")
                    print(f"Text: {note['text']}")
                    print(f"Timestamp: {note['timestamp']}")
        elif choice == '3':
            search_term = input("Enter Wikipedia search term: ")
            topic = input("Enter topic to append Wikipedia info: ")
            wiki_info = s.query_wikipedia(search_term)
            if wiki_info:
                note_name = f"Wikipedia: {wiki_info['title']}"
                text = f"{wiki_info['summary']} More info: {wiki_info['link']}"
                timestamp = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
                result = s.add_or_update_note(topic, note_name, text, timestamp)
                print(result)
            else:
                print("No Wikipedia information found for this term.")
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    client_interface()
