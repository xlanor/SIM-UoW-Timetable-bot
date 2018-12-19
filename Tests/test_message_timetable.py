from Models.class_message import MessageTimetable


def test_message_timetable_init():
    """
    self.__cur_week = cur_week
        self.__last_sync_date = last_sync_date
        # prepares a nested list of lists.
        self.__class_list = []
        for i in range(7):
            # adds 7 empty arrays.
            self.__class_list.append([])
    """
    msg = MessageTimetable("27/01/2018", "27/02/2017")
    assert msg.__MessageTimetable__.last_sync_date == "27/01/2018"
