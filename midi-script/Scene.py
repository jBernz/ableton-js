from Interface import Interface
from ClipSlot import ClipSlot


class Scene(Interface):
    @staticmethod
    def serialize_scene(scene):
        if scene is None:
            return None

        scene_id = Interface.save_obj(scene)
        scene_status = get_scene_status(scene)
        set_scene_color(scene, scene_status)
        
        return {
            "id": scene_id, 
            "name": scene.name, 
            "color": scene.color_index, 
            "status": scene_status
        }

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

def set_scene_color(scene, status):
    if status == 'recording':
        scene.color_index = 56
    if status == 'ready':
        scene.color_index = 69
    if status == 'playing' or status == 'stopped':
        most_notes = 0
        for clip_slot in scene.clip_slots:
            if(clip_slot.has_clip):
                clip_slot.clip.select_all_notes()
                if len(clip_slot.clip.get_selected_notes()) > most_notes:
                    most_notes = len(clip_slot.clip.get_selected_notes())
                    scene.color_index = clip_slot.clip.color_index
                else:
                    clip_slot.clip.color_index = scene.color_index