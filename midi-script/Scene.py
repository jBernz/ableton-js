from Interface import Interface
from ClipSlot import ClipSlot


class Scene(Interface):
    @staticmethod
    def serialize_scene(scene):
        if scene is None:
            return None

        scene_id = Interface.save_obj(scene)
        return {
            "id": scene_id, 
            "name": scene.name, 
            "color": scene.color, 
            "status": get_scene_status(scene)}

    def __init__(self, c_instance, socket):
        super(Scene, self).__init__(c_instance, socket)

    def get_clip_slots(self, ns):
        return map(ClipSlot.serialize_clip_slot, ns.clip_slots)

#custom param
def get_scene_status(scene):
    has_clip = False
    is_playing = False
    for clip_slot in scene.clip_slots:
        if(clip_slot.has_clip):
            has_clip = True
            if clip_slot.is_recording:
                return 'recording'
            if clip_slot.is_playing:
                is_playing = True
    if is_playing:
        return 'playing'
    if has_clip:
        return 'stopped'
    return 'ready'