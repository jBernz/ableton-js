from Interface import Interface


class ClipSlot(Interface):
    @staticmethod
    def serialize_clip_slot(clip_slot):
        if clip_slot is None:
            return None

        clip_slot_id = Interface.save_obj(clip_slot)
        return {
            "id": clip_slot_id, 
            "color": clip_slot.color,
            "has_clip": clip_slot.has_clip,
            "is_playing": clip_slot.is_playing,
            "is_recording": clip_slot.is_recording,
            "is_triggered": clip_slot.is_triggered
        }

    def __init__(self, c_instance, socket):
        super(ClipSlot, self).__init__(c_instance, socket)
