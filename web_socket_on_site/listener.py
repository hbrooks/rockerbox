from websocket import create_connection
import time
import json

SOURCE = 'ws://04623.interviews.rockerbox.com/echo'
TOPIC_TO_LISTEN_TO = 'external_events_2'
OUTPUT_FILE = 'stream_data.txt'


if __name__ == '__main__':
    ws = create_connection(SOURCE)
    ws.send('{"topic":"'+TOPIC_TO_LISTEN_TO+'","contains":[]}')
    print("Started Listening...")
    t_start = time.time()
    while True:
        raw_data = ws.recv()
        windowed_stream_data = json.loads(raw_data)
        if time.time() - t_start >= 5:
            t_start = time.time()
            unique_URLs_by_source = {}
            for message in windowed_stream_data['messages']:
                source = message['rb_source']
                url = message['referrer']
                if source not in unique_URLs_by_source:
                    unique_URLs_by_source[source] = set()
                unique_URLs_by_source[source].add(url)
            unique_URLs_by_source = {k: len(v) for k,v in unique_URLs_by_source.items()}
            print("Batch gathered... {} sources".format(len(unique_URLs_by_source.keys())))
            with open(OUTPUT_FILE, 'w') as file_stream:
                file_stream.write(json.dumps(unique_URLs_by_source))

    ws.close()