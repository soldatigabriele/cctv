import random
from datetime import datetime
from modules.database import Database


database = Database()
i=0
for element in ['test1', 'test2']:
    event_id = database.createEvent({
        'filename': element,
        'timestamp': datetime.now()
    })
    print(event_id)
    database.updateEvent(event_id, {
        'camera': i,
        'video_folder': i,
        'total_frames': i
    })
    i = i+1


# v = 0
# while(v < random.randint(1,50)):
#     v = v+1
#     models = ['yolo', 'ssd']
#     event_id = database.createEvent({
#         'filename': '2019291038.h264',
#         'model': models[random.randint(0,1)],
#         'camera': random.randint(1,4),
#         'timestamp': datetime.now()
#     })
#     types = ['positive', 'negative']
#     labels = ['person', 'cat']
#     database.updateEvent(event_id, {
#         'event_type': types[random.randint(0,1)],
#         'object_label': labels[random.randint(0,1)],
#         'confidence': random.randint(1,100) / 100,
#         'payload': '{"label": "something", "coordinates": {"top": 10, "left":20, "bottom": 40, "bottom":50}}',
#         'total_frames': random.randint(1,20) * 100,
#         'skipped_frames': random.randint(1,50),
#     })
