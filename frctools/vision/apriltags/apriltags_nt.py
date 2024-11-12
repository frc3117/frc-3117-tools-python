from ntcore import NetworkTableInstance, NetworkTableEntry, Event, EventFlags


class AprilTagEntry:
    def __init__(self, id: int, nt_instance: NetworkTableInstance):
        self.id = id
        self.nt_instance = nt_instance

        parent_path = f'/SmartDashboard/AprilTags/{id}'

        self.__position = [0., 0., 0.]
        self.__position_entry: NetworkTableEntry = nt_instance.getEntry(f'{parent_path}/position')
        nt_instance.addListener(self.__position_entry, EventFlags.kValueAll, self.__on_pos_update__)

        self.__center = [0., 0.]
        self.__center_entry: NetworkTableEntry = nt_instance.getEntry(f'{parent_path}/center')
        nt_instance.addListener(self.__center_entry, EventFlags.kValueAll, self.__on_center_update__)

        self.__is_detected = False
        self.__is_detected_entry: NetworkTableEntry = nt_instance.getEntry(f'{parent_path}/is_detected')
        nt_instance.addListener(self.__is_detected_entry, EventFlags.kValueAll, self.__on_detected_update__)

    def get_position(self):
        return self.__position
    def set_position(self, position):
        self.__position_entry.setDoubleArray([position[0], position[1], position[2]])

    def get_center(self):
        return self.__center
    def set_center(self, center):
        self.__center_entry.setDoubleArray([center[0], center[1]])

    def is_detected(self):
        return self.__is_detected
    def set_detected(self, state: bool):
        self.__is_detected_entry.setBoolean(state)

    def __on_pos_update__(self, event: Event):
        self.__position = event.data.value.getDoubleArray()
    def __on_center_update__(self, event: Event):
        self.__center = event.data.value.getDoubleArray()
    def __on_detected_update__(self, event: Event):
        self.__is_detected = event.data.value.getBoolean()


class AprilTagsNetworkTable:
    __INSTANCE__: 'AprilTagsNetworkTable' = None

    def __init__(self, tag_count: int, nt_instance: NetworkTableInstance = None):
        AprilTagsNetworkTable.__INSTANCE__ = self

        self.nt_instance = NetworkTableInstance.getDefault() if nt_instance is None else nt_instance

        self.tags = []
        for i in range(tag_count):
            self.tags.append(AprilTagEntry(i + 1, self.nt_instance))

    def __call__(self, detections):
        detected_id = []
        for d in detections:
            id = d.tag_id - 1
            tag = self.tags[id]

            detected_id.append(id)

            tag.set_detected(True)
            tag.set_position([d.pose_t[0][0], d.pose_t[1][0], d.pose_t[2][0]])
            tag.set_center(d.center)

        for i in range(len(self.tags)):
            if i in detected_id:
                continue

            tag = self.tags[i]
            tag.set_detected(False)

    @staticmethod
    def get_tag(id: int):
        return AprilTagsNetworkTable.__INSTANCE__.tags[id - 1]

    @staticmethod
    def get_detected():
        return [tag for tag in AprilTagsNetworkTable.__INSTANCE__.tags if tag.is_detected()]

    @staticmethod
    def instance():
        return AprilTagsNetworkTable.__INSTANCE__
