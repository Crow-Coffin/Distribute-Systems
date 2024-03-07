from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import requests

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Load or initialize XML database
    try:
        tree = ET.parse('notebook.xml')
        root = tree.getroot()
    except FileNotFoundError:
        root = ET.Element("data")
        tree = ET.ElementTree(root)

    # Function to add or update notes
    def add_or_update_note(topic, note_name, text, timestamp):
        # Check if the topic exists
        for tpc in root.findall(f".//topic[@name='{topic}']"):
            # If topic exists, append note
            new_note = ET.SubElement(tpc, "note", name=note_name)
            ET.SubElement(new_note, "text").text = text
            ET.SubElement(new_note, "timestamp").text = timestamp
            tree.write('notebook.xml')
            return f"Note added to topic '{topic}'."

        # If topic does not exist, create new topic and note
        new_topic = ET.SubElement(root, "topic", name=topic)
        new_note = ET.SubElement(new_topic, "note", name=note_name)
        ET.SubElement(new_note, "text").text = text
        ET.SubElement(new_note, "timestamp").text = timestamp
        tree.write('notebook.xml')
        return f"Topic '{topic}' with new note created."

    # Function to get notes by topic
    def get_notes_by_topic(topic):
        notes = []
        for tpc in root.findall(f".//topic[@name='{topic}']"):
            for note in tpc.findall("note"):
                notes.append({
                    'name': note.get('name'),
                    'text': note.find('text').text,
                    'timestamp': note.find('timestamp').text
                })
        return notes

    def query_wikipedia(topic):
        S = requests.Session()
        URL = "https://en.wikipedia.org/w/api.php"
        PARAMS = {
            "action": "opensearch",
            "namespace": "0",
            "search": topic,
            "limit": "1",
            "format": "json"
        }
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        # Assuming the first [1] is title list, [2] is summary, [3] is link; taking first result
        if DATA[1]:
            return {'title': DATA[1][0], 'summary': DATA[2][0], 'link': DATA[3][0]}
        else:
            return None

    server.register_function(query_wikipedia)

    server.register_function(add_or_update_note)
    server.register_function(get_notes_by_topic)

    # Run the server's main loop
    print("Serving XML-RPC on localhost port 8000...")
    server.serve_forever()