try:
    from threading import Thread
    from typing import Union, Tuple

    from StreamDeck.DeviceManager import DeviceManager
    from StreamDeck.Devices.StreamDeck import StreamDeck

    from frctools.streamdeck.keys import StreamDeckKey

    import time


    class StreamDeckBoard:
        def __init__(self, device_id: int = 0):
            devices_list = DeviceManager().enumerate()
            self.device: StreamDeck = devices_list[device_id]

            self.keys = [None] * self.device.key_count()

            self.__is_running = False
            self.__thread = None

        def start(self):
            if self.__is_running:
                return

            self.device.open()
            self.device.reset()

            self.__is_running = True
            self.__thread = Thread(target=self.__update__, daemon=True)

            self.__thread.start()

        def stop(self):
            if not self.__is_running:
                return

            self.__is_running = False
            self.__thread.join()

        def __update__(self):
            held_keys = [False] * self.device.key_count()

            def key_callback(deck, key_id, state):
                if self.device != deck:
                    return  # Ignore events from other devices

                held_keys[key_id] = state

            self.device.set_key_callback(key_callback)

            while self.__is_running:
                for i in range(self.device.key_count()):
                    key = self.keys[i]
                    if key is None:
                        continue

                    if held_keys[i]:
                        key.handle_held()

                    key.update()
                time.sleep(1/60.)

        def wait_forever(self):
            self.__thread.join()

        def set_key(self, key_id: Union[int, Tuple[int, int]], key: StreamDeckKey):
            if isinstance(key_id, tuple):
                x, y = key_id
                height, width = self.device.key_layout()

                if x < 0 or x >= width or y < 0 or y >= height:
                    raise ValueError('Key coordinates out of bounds')

                key_id = (height - key_id[1] - 1) * width + key_id[0]

            self.keys[key_id] = key
            key.set_key_id(self.device, key_id)

except ImportError:
    class StreamDeckBoard:
        def __init__(self, *args, **kwargs):
            raise RuntimeError('StreamDeckBoard requires the StreamDeck SDK to be installed')
