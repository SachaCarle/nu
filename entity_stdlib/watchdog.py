from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

patterns = "*"
ignore_patterns = ""
ignore_directories = False
case_sensitive = True
my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
    mind.me > ('created', event.src_path)

def on_deleted(event):
    mind.me > ('deleted', event.src_path)

def on_modified(event):
    mind.me > ('modified', event.src_path)

def on_moved(event):
    mind.me > ('moved', event.src_path, event.dest_path)

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

path = mind.body[mind.me.LOCATION_PATH_KEY]
go_recursively = True

my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()


import time
@mind
def wait(self):
    def _():
        try:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
                my_observer.stop()
                my_observer.join()
    return _
