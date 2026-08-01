import queue

transcript_queue = queue.Queue()


def add_transcript(text):
    transcript_queue.put(text)


def get_latest():
    data = []

    while not transcript_queue.empty():
        data.append(transcript_queue.get())

    return " ".join(data)