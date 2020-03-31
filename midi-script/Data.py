from Interface import Interface


class Data(Interface):
    @staticmethod
    def serialize_data(song, c_instance):

        data = {
            'id': None,
            'loops': [],
            'has_empty_loops': False,
            'fx': [],
            'cbord': []
        }

        data['id'] = Interface.save_obj(data)

        scene_statuses = get_scene_statuses(song)
        color_scenes(song, scene_statuses)

        data['loops'] = get_loop_colors(scene_statuses, c_instance)
        data['has_empty_loops'] = has_empty_loops(scene_statuses)
        data['cbord'] = get_cbord_colors(song)
        
        return data

    def __init__(self, c_instance, socket):
        super(Data, self).__init__(c_instance, socket)


# Song parsers ------------------------------------------

def get_scene_statuses(song):
    statuses = {}
    for scene in song.scenes:
        statuses[scene.name] = {
            'type': None,
            'recording': False, 
            'playing': False, 
            'selected': False,
            'empty': True,
            'color': None
        }

        most_notes = 0
        i = 0
        n = 0

        for clip_slot in scene.clip_slots:

            if 'CLIP' in scene.name:
                statuses[scene.name]['type'] = 'clip'

            elif 'loop' in scene.name:
                statuses[scene.name]['type'] = 'loop'

            if clip_slot.is_recording:
                statuses[scene.name]['recording'] = True

            if clip_slot.is_playing:
                statuses[scene.name]['playing'] = True

            if(clip_slot.has_clip):
                clip_slot.clip.select_all_notes()
                if len(clip_slot.clip.get_selected_notes()) > most_notes:
                    most_notes = len(clip_slot.clip.get_selected_notes())
                    n = i
                    statuses[scene.name]['color'] = clip_slot.clip.color_index
            i += 1

        if statuses[scene.name]['color']:
            statuses[scene.name]['empty'] = False

            instrument_group = get_parent(song, song.tracks[n])

            if statuses[scene.name]['type'] == 'clip':
                if instrument_group.name == song.get_data('selected_instrument_group', None):
                    statuses[scene.name]['selected'] = True

            elif statuses[scene.name]['type'] == 'loop':
                statuses[scene.name]['type'] = 'loop'
                statuses[scene.name]['group_name'] = instrument_group.name
                if instrument_group.name in song.get_data('selected_fx_groups', []):
                    statuses[scene.name]['selected'] = True
                
    return statuses


def color_scenes(song, statuses):
    for scene in song.scenes:
        if statuses[scene.name]['recording']:
            scene.color_index = 56
        elif statuses[scene.name]['empty']:
            scene.color_index = 69
        elif statuses[scene.name]['selected'] and statuses[scene.name]['type'] == 'loop':
            scene.color_index = 13
        else:
            scene.color_index = statuses[scene.name]['color']


color_index_map = {
    9: 'blue',
    12: 'pink',
    39: 'lavender',
    56: 'red',
    61: 'green',
    69: 'maroon',
    13: 'white'
}

def get_loop_colors(statuses, c_instance):
    loops = []
    for name in statuses:
        if statuses[name]['type'] == 'loop' and not name == 'loop[]':
            key_name = name[name.find('[')+1:name.find(']')]
            color = None
            if statuses[name]['recording']:
                color = 'red'
            else:
                color = color_index_map[statuses[name]['color']]
                if statuses[name]['selected'] and statuses[name]['playing']:
                    color = 'bright-' + color
                elif not statuses[name]['selected'] and not statuses[name]['playing']:
                    color = 'dim-' + color
            loops.append({'color': color, 'key_name': key_name})
    return loops


def get_cbord_colors(song):
    i = 1
    cbord = []
    for track in song.tracks:
        if track.name == 'MIDI_IN' and track.input_routing_type.display_name == 'ALL_IN':
            color = color_index_map[track.color_index]
            if track.arm == 1:
                color = 'bright-' + color
            cbord.append({'color': color, 'name': 'CB'+str(i)})
            i += 1
    return cbord
    


def has_empty_loops(statuses):
    for name in statuses:
        if name == 'loop[]':
            return True
    return False


def get_parent(song, child_track):
    current_group = None
    for track in song.tracks:
        if track == child_track:
            return current_group
        if track.is_foldable and not track.is_grouped:
            current_group = track
    return None