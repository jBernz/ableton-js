from Interface import Interface


class Data(Interface):
    @staticmethod
    def serialize_data(song):

        data = {
            'id': None,
            'loops': [],
            'fx': [],
            'has_empty_loops': False
        }

        data.id = Interface.save_obj(data)

        for scene in song.scenes:
            status = get_scene_status(scene)
            set_scene_color(scene, status, song)
            if scene.name is 'loop[]':
                data.has_empty_loops = True
            elif 'loop' in scene.name:
                data.loops.append(parse_scene(scene))
        
        return data

    def __init__(self, c_instance, socket):
        super(Data, self).__init__(c_instance, socket)


# Song parsers ------------------------------------------

color_index_map = {
    9: 'blue',
    12: 'pink',
    56: 'red',
    69: 'dim-red',
    13: 'white'
}

def parse_scene(scene, status):
    loop = {}
    loop['key_name'] = scene.name[len('loop['):-len(']')]
    if status is 'stopped':
        loop['color'] = 'dim-' + color_index_map[scene.color_index]
    else:
        loop['color'] = color_index_map[scene.color_index]
    return loop


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


def set_scene_color(scene, status, song):
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
        if scene.name in song.get_data('held_scene_names',[]):
            scene.color_index = 13