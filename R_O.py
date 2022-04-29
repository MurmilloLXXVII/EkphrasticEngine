#version 0.4
import textwrap
import random

verb0dict = {}
verb1dict = {}
verb2dict = {}
verblitdict = {}
verblit2dict = {}
verb2litdict = {}
noundict = {}
multinoundict = {}

noun_id_dict = {}
verb_id_dict = {}

directions = ['n','s','w','e','nw','ne','sw','se','u','d']

pronouns = ['they', 'he', 'she', 'it', 'you']

directionsdict = {
    'n' : 'north',
    's' : 'south',
    'w' : 'west',
    'e' : 'east',
    'nw' : 'northwest',
    'ne' : 'northeast',
    'sw' : 'southwest',
    'se' : 'southeast',
    'u' : 'up',
    'd' : 'down'
}

pluralsdict = {
    'is' : 'are',
    'Is' : 'Are',
    'it' : 'they',
    'It' : 'They',
    'he' : 'they',
    'He' : 'They',
    'she' : 'they',
    'She' : 'They',
    'this' : 'these',
    'This' : 'These',
    'that' : 'those',
    'That' : 'Those'

}

obliquesdict = {
    'they' : 'them',
    'he' : 'him',
    'she' : 'her',
    'who' : 'whom',
    'I' : 'me',
    'we' : 'us',
    'They' : 'Them',
    'He' : 'Him',
    'She' : 'Her',
    'Who' : 'Whom',
    'We' : 'Us'
}

reflexivesdict = {
    'they' : 'themself',
    'he' : 'himself',
    'she' : 'herself',
    'it' : 'itself',
    'we' : 'ourself',
    'you' : 'yourself',
    'I' : 'myself',
    'They' : 'Themself',
    'He' : 'Himself',
    'She' : 'Herself',
    'It' : 'Itself',
    'We' : 'Ourself',
    'You' : 'Yourself',
}

posessivesdict = {
    'they' : 'theirs',
    'he' : 'his',
    'she' : 'hers',
    'it' : 'its',
    'we' : 'our',
    'you' : 'your',
    'who' : 'whose',
    'I' : 'my',
    'They' : 'Theirs',
    'He' : 'His',
    'She' : 'Hers',
    'It' : 'Its',
    'We' : 'Our',
    'You' : 'Your',
    'Who' : 'Whose',
}

def define_pronoun(nom, obl, ref, pos): #create and add more pronouns if you so wish, or redefine and modify existing pronouns
    if nom not in pronouns: #unfortunately no duplicates allowed (wouldn't work with dictionary structures)
        pronouns.append(nom)
    obliquesdict[nom] = obl
    reflexivesdict[nom] = ref
    posessivesdict[nom] = pos

def a_an(word):
    assert type(word) == str, 'The word must be a string.'
    vowels = ['a','e','i','o','u']
    if word[0].lower() in vowels:
        return 'an ' + word
    return 'a ' + word

def test_a_an(word):
    assert type(word) == str, 'The word must be a string.'
    vowels = ['a','e','i','o','u']
    if word[0].lower() in vowels:
        return 'an'
    return 'a'

def obliquefy(phrase):
    l = phrase.split(' ')
    b = ''
    for word in l:
        if word in obliquesdict:
            b += obliquesdict[word]; b += ' '
        else:
            b += word; b += ' '
    return b[:-1]

def reflexify(phrase):
    l = phrase.split(' ')
    b = ''
    for word in l:
        if word in reflexivesdict:
            b += reflexivesdict[word]; b += ' '
        else:
            b += word; b += ' '
    return b[:-1]

def posessify(phrase):
    l = phrase.split(' ')
    b = ''
    for word in l:
        if word in posessivesdict:
            b += posessivesdict[word]; b += ' '
        else:
            b += word; b += ' '
    return b[:-1]

class Room:
    def __init__(self):
        self.desc = 'This is a nondescript room.'
        self.dark = False
        self.dark_desc = 'This is a dark place.'
        self.sound_desc = 'You hear nothing.'
        self.smell_desc = 'You smell nothing.'
        self.contents = []
        self.exits = {}
        self.nexits = {}
        for x in directions:
            if (x not in self.exits) and (x not in self.nexits):
                self.nexits[x] = 'You cannot go in that direction.'

    def add_exit(self, dir, dest, msg):
        assert dir in directions, 'The supplied direction is invalid.'
        assert isinstance(dest, Room), 'The supplied destination is not a room.'
        assert type(msg) == str, 'The travel message must be a string.'
        self.exits[dir] = (dest, msg)
        if dir in self.nexits:
            self.nexits.pop(dir)

    def add_nexit(self, dir, msg):
        assert dir in directions, 'The supplied direction is invalid.'
        assert type(msg) == str, 'The obstruction message must be a string.'
        self.nexits[dir] = msg
        if dir in self.exits:
            self.exits.pop(dir)

    def make_all_nexit_defaults(self, msg):
        assert type(msg) == str, 'The obstruction message must be a string.'
        for x in directions:
            if (x not in self.exits):
                self.nexits[x] = msg

    def add_door(self, dir, door):
        assert dir in directions, 'The supplied direction is invalid.'
        assert isinstance(door, Door), 'The supplied door is not actually a door.'
        self.exits[dir] = (door, door.get_move_message())
        if dir in self.nexits:
            self.nexits.pop(dir)

    def travelcheck(self, dir):
        assert dir in directions, 'The supplied direction is invalid.'
        return True

    def set_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.desc = desc

    def set_dark_desc(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.dark_desc = desc

    def set_sound_description(self, desc):
        assert type(desc) == str or isinstance(desc, Perception), 'The description must be a string or a perception.'
        self.sound_desc = desc

    def set_smell_description(self, desc):
        assert type(desc) == str or isinstance(desc, Perception), 'The description must be a string or a perception.'
        self.smell_desc = desc

    def get_exits(self):
        return self.exits

    def get_nexits(self):
        return self.nexits

    def get_contents(self):
        return self.contents

    def is_noisy(self):
        if isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
            return True
        else:
            for x in self.get_contents():
                if x.is_noisy():
                    return True
        return False

    def is_smelly(self):
        if isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
            return True
        else:
            for x in self.get_contents():
                if x.is_smelly():
                    return True
        return False

    def describe_sound(self, implicit = False):

        def report_ambient_sounds(thing, implicit2 = False):
            if (isinstance(thing, Container) and (thing.is_transparent_sound() or thing.is_open())) or isinstance(thing, Room):
                for x in thing.get_contents():
                    if (not implicit2) or x != player:
                        report_ambient_sounds(x)
            if isinstance(thing.sound_desc, Perception) and thing.sound_desc.get_activity():
                if isinstance(thing, Room) or thing.is_visible():
                    pront(thing.sound_desc.get_description())
                else:
                    pront(thing.sound_desc.get_invisible_description())

        if self.is_noisy():
            report_ambient_sounds(self, implicit)
        else:
            if isinstance(self.sound_desc, str):
                pront(self.sound_desc)
            elif isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
                if self.is_visible():
                    pront(self.sound_desc.get_description())
                else:
                    pront(self.sound_desc.get_invisible_description())

    def describe_smell(self, implicit = False):

        def report_ambient_smells(thing, implicit2 = False):
            if (isinstance(thing, Container) and (thing.is_transparent_smell() or thing.is_open())) or isinstance(thing, Room):
                for x in thing.get_contents():
                    if (not implicit2) or x != player:
                        report_ambient_smells(x)
            if isinstance(thing.smell_desc, Perception) and thing.smell_desc.get_activity():
                if isinstance(thing, Room) or thing.is_visible():
                    pront(thing.smell_desc.get_description())
                else:
                    pront(thing.smell_desc.get_invisible_description())

        if self.is_smelly():
            report_ambient_smells(self, implicit)
        else:
            if isinstance(self.smell_desc, str):
                pront(self.smell_desc)
            elif isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
                pront(self.smell_desc.get_description())

    def make_dark(self):
        self.dark = True

    def make_lit(self):
        self.dark = False

    def is_dark(self):
        return self.dark

    def is_illuminated(self):
        if self.is_dark():
            for x in self.get_contents():
                if x.is_illuminated():
                    return True
        else:
            return True

    def describe(self):
        if self.is_illuminated():
            pront(self.desc)
            for x in self.get_contents():
                if x != player and not isinstance(x, NPC) and 'hidden' not in x.get_properties():
                    if 'initialize' in x.get_properties():
                        pront(x.init_desc)
                    elif ('unlisted' in x.get_properties()) and isinstance(x, Surface) and len(x.get_contents()) > 0 and 'suppressed' not in x.get_properties():
                        pront(f'{x.art_d().capitalize()} {x.pluralize("bears")}:')
                        x.list_contents(1)
                    elif ('unlisted' in x.get_properties()) and isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()) and 'suppressed' not in x.get_properties():
                        pront(f'{x.art_d().capitalize()} {x.pluralize("contains")}:')
                        x.list_contents(1)
            for y in self.get_contents():
                w = ''
                if isinstance(y, RopeTrail) and y.is_visible():
                    k = y.get_parent_rope()
                    if k.get_tied_objects()[0].is_visible():
                        if 'plug' in k.get_properties():
                            w += f' (plugged into '
                        else:
                            w += f' (tied to '
                        if len(k.get_tied_objects()) == 1:
                            w += f'{k.get_tied_objects()[0].art_d()})'
                        elif len(k.get_tied_objects()) == 2:
                            if k.get_tied_objects()[0] is k.get_tied_objects()[1]:
                                w += f'{k.get_tied_objects()[0].art_d()} at both ends)'
                            elif k.get_tied_objects()[0].art_i() == k.get_tied_objects()[1].art_i():
                                w += f'{k.get_tied_objects()[0].art_i()} at both ends)'
                            else:
                                w += f'{k.get_tied_objects()[0].art_d()} and {k.get_tied_objects()[1].art_d()})'
                        pront(f'There {k.pluralize("is")} {k.art_i()}{w} here.')
                    elif len(k.get_tied_objects()) > 1 and k.get_tied_objects()[1].is_visible():
                        if 'plug' in k.get_properties():
                            w += f' (plugged into '
                        else:
                            w += f' (tied to '
                        w += f'{k.get_tied_objects()[1].art_d()})'
                        pront(f'There {k.pluralize("is")} {k.art_i()}{w} here.')
                    else:
                        pront(f'There {k.pluralize("is")} {k.art_i()} running across the ground here.')
                if ('unlisted' not in y.get_properties()) and ('initialize' not in y.get_properties() and 'hidden' not in y.get_properties()):
                    if 'plug' in y.get_properties() and isinstance(y, Rope) and len(y.get_tied_objects()) > 0:
                        w += f' (plugged into '
                    elif isinstance(y, Rope) and len(y.get_tied_objects()) > 0:
                        w += f' (tied to '
                    if isinstance(y, Rope) and len(y.get_tied_objects()) == 1:
                        w += f'{y.get_tied_objects()[0].art_d()})'
                    if isinstance(y, Rope) and len(y.get_tied_objects()) == 2:
                        if y.get_tied_objects()[0] is y.get_tied_objects()[1]:
                            w += f'{y.get_tied_objects()[0].art_d()} at both ends)'
                        elif y.get_tied_objects()[0].art_i() == y.get_tied_objects()[1].art_i():
                            w += f'{y.get_tied_objects()[0].art_i()} at both ends)'
                        else:
                            w += f'{y.get_tied_objects()[0].art_d()} and {y.get_tied_objects()[1].art_d()})'
                    if hasattr(y, 'parent_attachment'):
                        if 'plug' in y.get_properties():
                            w += f' (plugged into {y.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {y.get_parent_attachment().art_d()})'
                    if 'lamp' in y.get_properties() and y.get_brightness() == 2:
                        w += ' (lit)'
                    pront(f'There {y.pluralize("is")} {y.art_i()}{w} here.')
                    if isinstance(y, Surface) and len(y.get_contents()) > 0 and 'suppressed' not in x.get_properties():
                        pront(f'{y.art_d().capitalize()} {y.pluralize("bears")}:')
                        y.list_contents(1)
                    elif isinstance(y, Container) and len(y.get_contents()) > 0 and (y.is_open() or y.is_transparent()) and 'suppressed' not in x.get_properties():
                        pront(f'{y.art_d().capitalize()} {y.pluralize("contains")}:')
                        y.list_contents(1)
            for z in self.get_contents():
                if isinstance(z, NPC) and 'hidden' not in z.get_properties():
                    pront(z.get_activity_desc())
        else:
            pront(self.dark_desc)
            for x in self.get_contents():
                if x.get_brightness() == 1:
                    if x != player and not isinstance(x, NPC) and 'hidden' not in x.get_properties():
                        if 'initialize' in x.get_properties():
                            pront(x.init_desc)
                        elif ('unlisted' in x.get_properties()) and isinstance(x, Surface) and len(x.get_contents()) > 0 and 'suppressed' not in x.get_properties():
                            pront(f'{x.art_d().capitalize()} {x.pluralize("bears")}:')
                            x.list_contents(1)
                        elif ('unlisted' in x.get_properties()) and isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()) and 'suppressed' not in x.get_properties():
                            pront(f'{x.art_d().capitalize()} {x.pluralize("contains")}:')
                            x.list_contents(1)
            for y in self.get_contents():
                if y.get_brightness() == 1:
                    if ('unlisted' not in y.get_properties()) and ('initialize' not in y.get_properties() and 'hidden' not in y.get_properties()):
                        pront(f'There {y.pluralize("is")} {y.art_i()} here.')
                        if isinstance(y, Surface) and len(y.get_contents()) > 0 and 'suppressed' not in x.get_properties():
                            pront(f'{y.art_d().capitalize()} {y.pluralize("bears")}:')
                            y.list_contents(1)
                        elif isinstance(y, Container) and len(y.get_contents()) > 0 and (y.is_open() or y.is_transparent()) and 'suppressed' not in x.get_properties():
                            pront(f'{y.art_d().capitalize()} {y.pluralize("contains")}:')
                            y.list_contents(1)
            for z in self.get_contents():
                if y.get_brightness() == 1:
                    if isinstance(z, NPC) and 'hidden' not in z.get_properties():
                        pront(z.get_activity_desc())
        if self.is_noisy():
            self.describe_sound(True)
        if self.is_smelly():
            self.describe_smell(True)

offstage = Room()

class Object:

    def __init__(self, name, id, synonyms):
        assert type(name) == str, 'The name of the object must be a string.'
        assert type(id) == str, 'The internal id of the object must be a string.'
        assert ' ' not in id, 'The internal id cannot contain a space.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.name = name
        self.id = id
        self.synonyms = synonyms
        for x in self.synonyms:
            if x in noundict:
                multinoundict[x] = (noundict[x], self.id)
                noundict.pop(x)
            elif x in multinoundict:
                temp = multinoundict[x]
                new = temp + (self.id,)
                multinoundict[x] = new
            else:
                noundict[x] = self.id
        noun_id_dict[self.id] = self
        self.desc = 'It is an ordinary ' + self.name + '.'
        self.loc = offstage
        self.loc.contents.append(self)
        self.properties = []
        self.bulk = 10
        self.brightness = 0
        self.components = []
        self.allowed_parent_attachments = []
        self.allowed_child_attachments = []
        self.child_attachments = []
        self.attachment_limit = 1
        self.is_limiting_attachments = False
        self.known = False
        self.custom_immobile_message = 'It cannot be moved.'
        self.remaps_d = {}
        self.remaps_i = {}
        self.articles = ['the', test_a_an(self.name)]
        self.plural = False
        self.pronoun = 'it'
        self.sound_desc = 'You hear nothing.'
        self.smell_desc = 'You smell nothing.'
        self.touch_desc = 'You feel nothing unusual.'
        self.taste_desc = 'You taste no distinct flavor.'
        self.read_desc = 'Nothing is written there.'


    def set_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.desc = desc

    def set_initial_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.init_desc = desc

    def get_initial_description(self):
        return self.init_desc

    def swap_name(self, name):
        assert type(name) == str, 'The new name must be a string.'
        self.name = name

    def warp_to(self, loc):
        assert isinstance(loc, Room) or isinstance(loc, Container), 'The target location must be a room or container.'
        for x in self.get_child_attachments():
            if not(isinstance(x, Rope) and len(x.get_tied_objects()) > 1 and x.get_tied_objects()[0].is_within(player) and x.get_tied_objects()[1].is_within(player)):
                x.warp_to(loc)
        self.loc.contents.remove(self)
        self.loc = loc
        self.loc.contents.append(self)
        for x in self.get_components():
            x.warp_to(loc)
            if hasattr(x, 'parent_attachment'):
                x.detach()
        self.remove_property('worn')

    def drag_to(self, loc, r):
        assert isinstance(loc, Room) or isinstance(loc, Container), 'The target location must be a room or container.'
        assert isinstance(r, Rope), 'The dragging rope must be a rope.'
        self.loc.contents.remove(self)
        self.loc = loc
        self.loc.contents.append(self)
        for x in self.get_components():
            x.warp_to(loc)
            if hasattr(x, 'parent_attachment'):
                x.detach()
        for x in self.get_child_attachments():
            if x is not r:
                x.warp_to(loc)
        self.remove_property('worn')

    def make_component_of(self, obj):
        assert isinstance(obj, Object), 'The target must be an object.'
        self.set_bulk(0)
        self.add_property('component')
        self.add_property('unlisted')
        obj.add_component(self)
        self.warp_to(obj.get_loc())
        self.parent_object = obj

    def separate_component(self):
        assert 'component' in self.get_properties(), 'The object must be a component.'
        self.get_parent_object().remove_component(self)
        self.remove_property('component')
        self.remove_property('unlisted')
        del self.parent_object

    def get_components(self):
        return self.components

    def add_component(self, obj):
        assert isinstance(obj, Object), 'The component must be an object.'
        if obj not in self.get_components():
            self.get_components().append(obj)

    def remove_component(self, obj):
        assert isinstance(obj, Object), 'The component must be an object.'
        if obj in self.components:
            self.get_components().remove(obj)

    def get_allowed_parent_attachments(self):
        return self.allowed_parent_attachments

    def get_allowed_child_attachments(self):
        return self.allowed_child_attachments

    def get_parent_attachment(self):
        return self.parent_attachment

    def get_child_attachments(self):
        return self.child_attachments

    def set_allowed_parent_attachments(self, l):
        assert type(l) == list, 'The list of allowed parent attachments must be a list.'
        for x in l:
            assert isinstance(x, Object), 'The list of allowed parent attachments must be a list of objects.'
        self.allowed_parent_attachments = l

    def set_allowed_child_attachments(self, l):
        assert type(l) == list, 'The list of allowed child attachments must be a list.'
        for x in l:
            assert isinstance(x, Object), 'The list of allowed child attachments must be a list of objects.'
        self.allowed_child_attachments = l

    def add_allowed_parent_attachment(self, thing):
        assert isinstance(thing, Object), 'The allowed parent attachment must be an object.'
        if thing not in self.allowed_parent_attachments:
            self.allowed_parent_attachments.append(thing)

    def remove_allowed_parent_attachment(self, thing):
        assert isinstance(thing, Object), 'The allowed parent attachment must be an object.'
        if thing in self.allowed_parent_attachments:
            self.allowed_parent_attachments.remove(thing)

    def add_allowed_child_attachment(self, thing):
        assert isinstance(thing, Object), 'The allowed child attachment must be an object.'
        if thing not in self.allowed_parent_attachments:
            self.allowed_child_attachments.append(thing)

    def remove_allowed_child_attachment(self, thing):
        assert isinstance(thing, Object), 'The allowed child attachment must be an object.'
        if thing in self.allowed_child_attachments:
            self.allowed_child_attachments.remove(thing)

    def set_attachment_limiting_status(self, status):
        assert type(status) == bool, 'The status must be a boolean.'
        self.is_limiting_attachments = status

    def get_attachment_limiting_status(self):
        return self.is_limiting_attachments

    def set_attachment_limit(self, v):
        assert type(v) == int and v >= 1, 'The attachment limit must be a positive integer.'
        self.attachment_limit = v

    def get_attachment_limit(self):
        return self.attachment_limit

    def attach_to(self, thing):
        assert isinstance(thing, Object), 'The parent attachment must be an object.'
        assert thing in self.get_allowed_parent_attachments(), 'The parent attachment must be an allowed parent attachment.'
        assert self in thing.get_allowed_child_attachments(), 'The child attachment must be an allowed child attachment.'
        if hasattr(self, 'parent_attachment'):
            self.detach()
        self.parent_attachment = thing
        thing.child_attachments.append(self)
        self.warp_to(thing.get_loc())

    def detach(self):
        assert hasattr(self, 'parent_attachment'), 'The object must be attached to something.'
        self.get_parent_attachment().get_child_attachments().remove(self)
        del self.parent_attachment

    def get_parent_object(self):
        assert 'component' in self.get_properties(), 'The object must be a component.'
        return self.parent_object

    def add_synonym(self, word):
        assert type(word) == str, 'The synonym must be a string.'
        self.synonyms.append(word)
        noundict[word] = self.id

    def remove_synonym(self, word):
        assert type(word) == str, 'The synonym must be a string.'
        if word in self.synonyms:
            self.synonyms.remove(word)
            if word in noundict:
                del noundict[word]
            elif word in multinoundict:
                l = []
                for x in multinoundict[word]:
                    if x != self.id:
                        l.append(x)
                if len(l) == 2:
                    noundict[word] = tuple(l)
                    multinoundict.pop(word)
                else:
                    multinoundict[word] = tuple(l)

    def get_properties(self):
        return self.properties

    def add_property(self, prop):
        if prop not in self.properties:
            self.get_properties().append(prop)

    def remove_property(self, prop):
        if prop in self.properties:
            self.get_properties().remove(prop)

    def get_name(self):
        return self.name

    def get_loc(self):
        return self.loc

    def find_ultimate_room(self):
        if (isinstance(self.get_loc(), Room)):
            return self.get_loc()
        else:
            return self.get_loc().find_ultimate_room()

    def set_bulk(self, num):
        assert type(num) == int, 'The bulk must be an integer.'
        self.bulk = num

    def get_bulk(self):
        return self.bulk

    def set_custom_immobile_message(self, msg):
        assert type(msg) == str, 'The message must be a string.'
        self.custom_immobile_message = msg

    def get_custom_immobile_message(self):
        return self.custom_immobile_message

    def set_brightness(self, num):
        assert num in [0, 1, 2], 'The brightness value must be 0, 1, or 2.'
        self.brightness = num

    def get_brightness(self):
        return self.brightness

    def is_illuminated(self):
        if self.get_brightness() == 2:
            return True
        elif isinstance(self, Container) and (self.is_transparent() or self.is_open()):
            for x in self.get_contents():
                if x.is_illuminated():
                    return True
        return False

    def is_known(self):
        return self.known

    def make_known(self):
        self.known = True

    def make_unknown(self):
        self.known = False

    def get_remaps_d(self):
        return self.remaps_d

    def get_remaps_i(self):
        return self.remaps_i

    def add_remap_d(self, v, o):
        assert isinstance(v, Verb1) or isinstance(v, Verb2), 'The verb input must be a divalent or trivalent verb.'
        assert isinstance(o, Object), 'The object input must be an object.'
        self.remaps_d[v] = o

    def add_remap_i(self, v, o):
        assert isinstance(v, Verb2), 'The verb input must be a trivalent verb.'
        assert isinstance(o, Object), 'The object input must be an object.'
        self.remaps_i[v] = o

    def remove_remap_d(self, v):
        assert isinstance(v, Verb1) or isinstance(v, Verb2), 'The verb input must be a divalent or trivalent verb.'
        if v in self.remaps_d:
            del self.remaps_d[v]

    def remove_remap_i(self, v):
        assert isinstance(v, Verb2), 'The verb input must be a trivalent verb.'
        if v in self.remaps_i:
            del self.remaps_i[v]

    def art_d(self):
        if self.articles[0] == '':
            return self.get_name()
        else:
            return self.articles[0] + ' ' + self.get_name()

    def art_i(self):
        if self.articles[1] == '':
            return self.get_name()
        else:
            return self.articles[1] + ' ' + self.get_name()

    def is_plural(self):
        return self.plural

    def set_definite_article(self, word):
        assert type(word) == str, 'The article must be a string.'
        self.articles[0] = word

    def set_indefinite_article(self, word):
        assert type(word) == str, 'The article must be a string.'
        self.articles[1] = word

    def make_plural(self):
        if self.articles[1] in ['a', 'an']:
            self.set_indefinite_article('some')
        if self.desc == 'It is an ordinary ' + self.name + '.':
            self.desc = 'They are ordinary ' + self.name + '.'
        self.plural = True
        self.pronoun = self.pluralize(self.pronoun)

    def make_singular(self, newpronoun='it'):
        self.pronoun = newpronoun
        if self.articles[1] == 'some':
            self.set_indefinite_article(self.test_a_an())
        if self.desc == 'These are ordinary ' + self.name + '.':
            self.desc = 'This is an ordinary ' + self.name + '.'
        self.plural = False

    def set_pronoun(self, word):
        assert word in pronouns, 'The word must be a pronoun.'
        self.pronoun = word

    def get_pronoun(self):
        return self.pronoun

    def pluralize(self, phrase):
        if self.is_plural():
            l = phrase.split(' ')
            b = ''
            for word in l:
                if word in pluralsdict:
                    b += pluralsdict[word]; b += ' '
                elif word[-1] == 's':
                    b += word[:-1]; b += ' '
                else:
                    b += word; b += ' '
            return b[:-1]
        else:
            return phrase

    def is_within(self, thing):
        assert isinstance(thing, Room) or isinstance(thing, Object), 'The location to be checked must be a room or an object.'
        if self.get_loc() == thing:
            return True
        elif isinstance(self.get_loc(), Room):
            return False
        else:
            return self.get_loc().is_within(thing)

    def is_reachable(self):
        if 'distant' in self.get_properties():
            return False
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            if self.get_loc() == player or (self.get_loc() == player.get_state_position() or self == player.get_state_position()):
                return True
            elif isinstance(self.get_loc(), Container) and self.get_loc().is_open():
                return self.get_loc().is_reachable()
            else:
                return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and self.get_loc().is_open():
            return self.get_loc().is_reachable()
        else:
            return False

    def is_visible(self):
        if player.get_loc().is_illuminated():
            if 'hidden' in self.get_properties():
                return False
            elif self.get_loc() == player or self.get_loc() == player.get_loc():
                return True
            elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent()):
                return self.get_loc().is_visible()
            else:
                return False
        else:
            if 'hidden' in self.get_properties():
                return False
            elif self.get_loc() == player:
                return True
            elif self.get_loc() == player.get_loc() and self.get_brightness() == 1:
                return True
            elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent()):
                return self.get_loc().is_visible()
            else:
                return False

    def is_audible(self):
        if 'hidden' in self.get_properties():
            return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_sound()):
            return self.get_loc().is_audible()
        else:
            return False

    def is_touchable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            if self.get_loc() == player or (self.get_loc() == player.get_state_position() or self == player.get_state_position()):
                return True
            elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_touch()):
                return self.get_loc().is_touchable()
            else:
                return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_touch()):
            return self.get_loc().is_touchable()
        else:
            return False

    def is_smellable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_smell()):
            return self.get_loc().is_smellable()
        else:
            return False

    def is_tasteable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            if self.get_loc() == player or (self.get_loc() == player.get_state_position() or self == player.get_state_position()):
                return True
            elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_taste()):
                return self.get_loc().is_tasteable()
            else:
                return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_taste()):
            return self.get_loc().is_tasteable()
        else:
            return False

    def attachment_desc_helper(self):
        if len(self.get_child_attachments()) > 0:
            names = []
            plug_names = []
            tie_names = []
            pluralflag = False
            plug_pluralflag = False
            tie_pluralflag = False
            for x in self.get_child_attachments():
                if 'plug' in x.get_properties():
                    plug_names.append(x.art_i())
                    if x.is_plural():
                        plug_pluralflag = True
                elif isinstance(x, Rope):
                    tie_names.append(x.art_i())
                    if x.is_plural():
                        tie_pluralflag = True
                else:
                    names.append(x.art_i())
                    if x.is_plural():
                        pluralflag = True
            if len(names) > 1 or pluralflag: #some trickery here, if there is one object and it's plural, use 'are' in the description
                pront(f'{sequence(names, "and").capitalize()} are attached to {obliquefy(self.get_pronoun())}.')
            elif len(names) > 0: #possibly zero if all are plugs
                pront(f'{sequence(names, "and").capitalize()} is attached to {obliquefy(self.get_pronoun())}.')
            if len(tie_names) > 1 or tie_pluralflag: #see above comment about trickery
                pront(f'{sequence(tie_names, "and").capitalize()} are tied to {obliquefy(self.get_pronoun())}.')
            elif len(tie_names) > 0: #possibly zero if none are plugs
                pront(f'{sequence(tie_names, "and").capitalize()} is tied to {obliquefy(self.get_pronoun())}.')
            if len(plug_names) > 1 or plug_pluralflag: #see above comment about trickery
                pront(f'{sequence(plug_names, "and").capitalize()} are plugged into {obliquefy(self.get_pronoun())}.')
            elif len(plug_names) > 0: #possibly zero if none are plugs
                pront(f'{sequence(plug_names, "and").capitalize()} is plugged into {obliquefy(self.get_pronoun())}.')

    def describe(self):
        pront(self.desc)
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

    def set_sound_description(self, desc):
        assert type(desc) == str or (isinstance(desc, Perception) or isinstance(desc, PerceptionLink)), 'The description must be a string or a perception or a perception link.'
        self.sound_desc = desc

    def set_smell_description(self, desc):
        assert type(desc) == str or (isinstance(desc, Perception) or isinstance(desc, PerceptionLink)), 'The description must be a string or a perception or a perception link.'
        self.smell_desc = desc

    def set_taste_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.taste_desc = desc

    def set_touch_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.touch_desc = desc

    def set_read_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.read_desc = desc

    def get_read_description(self):
        return self.read_desc

    def is_noisy(self):
        if isinstance(self, Container):
            if isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
                return True
            else:
                if self.is_transparent_sound() or self.is_open():
                    for x in self.get_contents():
                        if x.is_noisy():
                            return True
        else:
            if isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
                return True
        return False

    def is_smelly(self):
        if isinstance(self, Container):
            if isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
                return True
            else:
                if self.is_transparent_smell() or self.is_open():
                    for x in self.get_contents():
                        if x.is_smelly():
                            return True
        else:
            if isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
                return True
        return False

    def describe_sound(self):

        def report_ambient_sounds(thing):
            if (isinstance(thing, Container) and (thing.is_transparent_sound() or thing.is_open())) or isinstance(thing, Room):
                for x in thing.get_contents():
                    report_ambient_sounds(x)
            if isinstance(thing.sound_desc, Perception) and thing.sound_desc.get_activity():
                if isinstance(thing, Room) or thing.is_visible():
                    pront(thing.sound_desc.get_description())
                else:
                    pront(thing.sound_desc.get_invisible_description())

        def find_outermost_location(thing):
            if (isinstance(thing.get_loc(), Container) and not thing.get_loc().is_transparent_sound()) or isinstance(thing.get_loc(), Room):
                return thing.get_loc()
            else:
                return find_outermost_location(thing.get_loc())

        if isinstance(self.sound_desc, PerceptionLink):
            if self.sound_desc.get_activity():
                destination = self.sound_desc.get_input()
                target = find_outermost_location(destination)
                if isinstance(target, Room):
                    report_ambient_sounds(target)
                elif isinstance(target, Container):
                    report_ambient_sounds(target)
                    for x in target.get_contents():
                        report_ambient_sounds(x)
            else:
                pront(self.smell_desc.get_inactive_sound_description())
        if isinstance(self, Container) and self.is_noisy():
            report_ambient_sounds(self)
        else:
            if isinstance(self.sound_desc, str):
                pront(self.sound_desc)
            elif isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
                if self.is_visible():
                    pront(self.sound_desc.get_description())
                else:
                    pront(self.sound_desc.get_invisible_description())

    def describe_smell(self):

        def report_ambient_smells(thing):
            if (isinstance(thing, Container) and (thing.is_transparent_smell() or thing.is_open())) or isinstance(thing, Room):
                for x in thing.get_contents():
                    report_ambient_smells(x)
            if isinstance(thing.smell_desc, Perception) and thing.smell_desc.get_activity():
                if isinstance(thing, Room) or thing.is_visible():
                    pront(thing.smell_desc.get_description())
                else:
                    pront(thing.smell_desc.get_invisible_description())

        def find_outermost_location(thing):
            if (isinstance(thing.get_loc(), Container) and not thing.get_loc().is_transparent_smell()) or isinstance(thing.get_loc(), Room):
                return thing.get_loc()
            else:
                return find_outermost_location(thing.get_loc())

        if isinstance(self.smell_desc, PerceptionLink):
            if self.smell_desc.get_activity():
                destination = self.smell_desc.get_input()
                target = find_outermost_location(destination)
                if isinstance(target, Room):
                    report_ambient_smells(target)
                elif isinstance(target, Container):
                    report_ambient_smells(target)
                    for x in target.get_contents():
                        report_ambient_smells(x)
            else:
                pront(self.smell_desc.get_inactive_smell_description())
        if isinstance(self, Container) and self.is_smelly():
            report_ambient_smells(self)
        else:
            if isinstance(self.smell_desc, str):
                pront(self.smell_desc)
            elif isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
                if self.is_visible():
                    pront(self.smell_desc.get_description())
                else:
                    pront(self.smell_desc.get_invisible_description())

    def describe_taste(self):
        pront(self.taste_desc)

    def describe_touch(self):
        pront(self.touch_desc)

    def get_allowed_states(self):
        return []

    def d_o_check(self, v):
        return True

    def i_o_check(self, v, d_o):
        return True

class MultiObject(Object):
    def __init__(self, name, id, synonyms):
        assert type(name) == str, 'The name of the object must be a string.'
        assert type(id) == str, 'The internal id of the object must be a string.'
        assert ' ' not in id, 'The internal id cannot contain a space.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.name = name
        self.id = id
        self.synonyms = synonyms
        for x in self.synonyms:
            if x in noundict:
                multinoundict[x] = (noundict[x], self.id)
                noundict.pop(x)
            elif x in multinoundict:
                temp = multinoundict[x]
                new = temp + (self.id,)
                multinoundict[x] = new
            else:
                noundict[x] = self.id
        noun_id_dict[self.id] = self
        self.desc = 'It is an ordinary ' + self.name + '.'
        self.loc_list = []
        self.properties = []
        self.bulk = 10
        self.brightness = 0
        self.components = []
        self.remaps_d = {}
        self.remaps_i = {}
        self.articles = ['the', test_a_an(self.name)]
        self.plural = False
        self.allowed_parent_attachments = []
        self.allowed_child_attachments = []
        self.child_attachments = []
        self.known = False
        self.custom_immobile_message = 'It cannot be moved.'
        self.pronoun = 'it'
        self.sound_desc = 'You hear nothing.'
        self.smell_desc = 'You smell nothing.'
        self.touch_desc = 'You feel nothing unusual.'
        self.taste_desc = 'You taste no distinct flavor.'
        self.read_desc = 'Nothing is written there.'
        self.add_property('distant')
        self.add_property('immobile')


    def warp_to(self, loc):
        raise Exception('This method (warp_to) should not be used for a MultiObject.')

    def get_loc(self):
        raise Exception('This method (get_loc) should not be used for a MultiObject.')

    def set_loc_list(self, l):
        assert type(l) == list, 'The list of locations must be a list.'
        for x in l:
            assert isinstance(x, Room), 'Only rooms are acceptable locations.'
        self.loc_list = l

    def get_loc_list(self):
        return self.loc_list

    def add_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        if loc not in self.loc_list:
            self.loc_list.append(loc)

    def remove_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        if loc in self.loc_list:
            self.loc_list.remove(loc)

    def is_within(self, thing):
        assert isinstance(thing, Room) or isinstance(thing, Object), 'The location to be checked must be a room or an object.'
        if thing in self.get_loc_list():
            return True
        return False

    def is_reachable(self):
        if 'distant' in self.get_properties():
            return False
        elif (hasattr(player, 'state_position') and player.get_state() != 'standing') and not 'ground' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
            #???? mystery effects
        else:
            return False

    def is_visible(self):
        if player.get_loc().is_illuminated():
            if 'hidden' in self.get_properties():
                return False
            elif player.get_loc() in self.get_loc_list():
                return True
            else:
                return False
        else:
            if 'hidden' in self.get_properties():
                return False
            elif player.get_loc() in self.get_loc_list() and self.get_brightness() == 1:
                return True
            else:
                return False

    def is_audible(self):
        if 'hidden' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
        else:
            return False

    def is_touchable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif (hasattr(player, 'state_position') and player.get_state() != 'standing') and not 'ground' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
        else:
            return False

    def is_smellable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
        else:
            return False

    def is_tasteable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif (hasattr(player, 'state_position') and player.get_state() != 'standing') and not 'ground' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
        else:
            return False

#all of these are dummy room components (walls, floors, etc.) for the default room types so they player doesn't get messages like "there is no floor here!"
dummy_ground = MultiObject('ground', 'ground#dummy', ['ground', 'floor'])
dummy_ground.remove_property('distant')
dummy_ground.add_property('ground')
dummy_ground.set_indefinite_article('')
dummy_ground.set_description('It is ordinary ground.')
dummy_sky = MultiObject('sky', 'sky#dummy', ['sky'])
dummy_wall = MultiObject('wall', 'wall#dummy', ['wall', 'walls'])
dummy_wall.remove_property('distant')
dummy_floor = MultiObject('floor', 'floor#dummy', ['floor', 'ground'])
dummy_floor.remove_property('distant')
dummy_floor.add_property('ground')
dummy_ceiling = MultiObject('ceiling', 'ceiling#dummy', ['ceiling'])
dummy_ceiling.remove_property('distant')

class InsideRoom(Room):

    def __init__(self):
        super().__init__()
        dummy_wall.add_loc(self)
        dummy_floor.add_loc(self)
        dummy_ceiling.add_loc(self)

class OutsideRoom(Room):

    def __init__(self):
        super().__init__()
        dummy_ground.add_loc(self)
        dummy_sky.add_loc(self)

class Container(Object):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.capacity = 100
        self.contents = []
        self.locked = False
        self.open = True
        self.transparent = False
        self.transparent_sound = False
        self.transparent_touch = False
        self.transparent_smell = False
        self.transparent_taste = False

    def set_capacity(self, num):
        assert type(num) == int, 'The capacity must be an integer.'
        self.capacity = num

    def get_capacity(self):
        return self.capacity

    def get_contents(self):
        return self.contents

    def set_transparent(self, val):
        assert type(val) == bool, 'The transparency must be a boolean.'
        self.transparent = val

    def set_transparent_sound(self, val):
        assert type(val) == bool, 'The sound transparency must be a boolean.'
        self.transparent_sound = val

    def set_transparent_touch(self, val):
        assert type(val) == bool, 'The touch transparency must be a boolean.'
        self.transparent_touch = val

    def set_transparent_smell(self, val):
        assert type(val) == bool, 'The smell transparency must be a boolean.'
        self.transparent_smell = val

    def set_transparent_taste(self, val):
        assert type(val) == bool, 'The sound transparency must be a boolean.'
        self.transparent_taste = val

    def add_content(self, thing):
        assert isinstance(thing, Object), 'The container can only hold other objects.'
        if thing not in self.contents:
            self.get_contents().append(thing)

    def remove_content(self, thing):
        assert isinstance(thing, Object), 'The container can only hold other objects.'
        if thing in self.contents:
            self.get_contents().remove(thing)

    def list_contents(self, n=0):
        if len(self.get_contents()) > 0:
            for x in self.get_contents():
                if 'unlisted' not in x.get_properties() and 'hidden' not in x.get_properties():
                    w = ''
                    if 'plug' in x.get_properties() and isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (plugged into '
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (tied to '
                    if isinstance(x, Rope) and len(x.get_tied_objects()) == 1:
                        w += f' (tied to {x.get_tied_objects()[0].art_d()})'
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) == 2:
                        if x.get_tied_objects()[0] is x.get_tied_objects()[1]:
                            w += f'{x.get_tied_objects()[0].art_d()} at both ends)'
                        elif x.get_tied_objects()[0].art_i() == x.get_tied_objects()[1].art_i():
                            w += f'{x.get_tied_objects()[0].art_i()} at both ends)'
                        else:
                            w += f'{x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    if hasattr(x, 'parent_attachment'):
                        if 'plug' in x.get_properties():
                            w += f' (plugged into {x.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {x.get_parent_attachment().art_d()})'
                    if 'worn' in x.get_properties():
                        w += ' (being worn)'
                    if 'lamp' in x.get_properties() and x.get_brightness() == 2:
                        w += ' (lit)'
                    pront('  ' * n + x.art_i() + w)
                    if isinstance(x, Surface) and len(x.get_contents()) > 0 and 'suppressed' not in x.get_properties():
                        pront('  ' * n + f'{x.art_d().capitalize()} {x.pluralize("bears")}:')
                        x.list_contents(n+1)
                    elif isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()) and 'suppressed' not in x.get_properties():
                        pront('  ' * n + f'{x.art_d().capitalize()} {x.pluralize("contains")}:')
                        x.list_contents(n+1)

    def get_content_bulk(self):
        b = 0
        for x in self.get_contents():
            b += x.get_bulk()
        return b

    def is_open(self):
        return self.open

    def is_locked(self):
        return self.locked

    def is_transparent(self):
        return self.transparent

    def is_transparent_sound(self):
        return self.transparent_sound

    def is_transparent_touch(self):
        return self.transparent_touch

    def is_transparent_smell(self):
        return self.transparent_smell

    def is_transparent_taste(self):
        return self.transparent_taste

    def make_open(self):
        self.open = True
        player.know_objects_in_loc(self)

    def make_closed(self):
        self.open = False

    def describe(self):
        if self.is_open():
            if len(self.get_contents()) > 0:
                pront(self.desc + f' {self.pluralize("It contains")}:')
                self.list_contents()
            else:
                pront(self.desc + f' {self.pluralize("It is")} empty.')
        elif self.is_transparent():
            if len(self.get_contents()) > 0:
                pront(self.desc + f' {self.pluralize("It is")} closed. {self.pluralize("It contains")}:')
                self.list_contents()
            else:
                pront(self.desc + f' {self.pluralize("It is")} closed and empty.')
        else:
            pront(self.desc + f' {self.pluralize("It is")} closed.')
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

    def update_internal_ropes(self):
        for x in self.get_contents():
            if isinstance(x, Rope):
                x.update_locations()
            elif isinstance(x, Container):
                x.update_internal_ropes()

    def check_taut_ropes(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        for x in self.get_contents():
            if isinstance(x, Rope):
                l = x.get_tied_objects()
                if len(l) == 1:
                    if len(x.get_room_order()) >= x.get_max_length() + 1 and not (len(x.get_room_order()) > 1 and loc == x.get_room_order()[-2]):
                        if l[0] in x.get_draggable_objects():
                            place = x.get_room_order()[0]
                            x.set_room_order(x.get_room_order()[1:])
                            if place not in x.get_room_order():
                                x.trail.remove_loc(place)
                            l[0].drag_to(x.get_room_order()[0], x)
                            return False
                        else:
                            pront(f'{x.art_d().capitalize()} jerks you to a stop as you try to leave; you will have to set it down if you want to go further.')
                            return True
                elif len(l) == 2:
                    if len(x.get_room_order()) >= x.get_max_length() + 1 and not (len(x.get_room_order()) > 1 and loc == x.get_room_order()[-2]):
                        if l[0] in self.get_contents():
                            z = l[1]
                        else:
                            z = l[0]
                        if z in x.get_draggable_objects():
                            place = x.get_room_order()[0]
                            x.set_room_order(x.get_room_order()[1:])
                            if place not in x.get_room_order():
                                x.trail.remove_loc(place)
                            z.drag_to(x.get_room_order()[0], x)
                            return False
                        else:
                            pront(f'{x.art_d().capitalize()} jerks you to a stop as you try to leave; you will have to set it down if you want to go further.')
                            return True
                return False
            elif isinstance(x, Container):
                if x.check_taut_ropes(loc):
                    return True
        return False

    def warp_to(self, loc):
        super().warp_to(loc)
        self.update_internal_ropes()

class Surface(Container):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)

    def describe(self):
        if len(self.get_contents()) > 1 or (len(self.get_contents()) == 1 and self.get_contents()[0].is_plural()):
            pront(self.desc + f' On {obliquefy(self.pluralize("it"))} are:')
            self.list_contents()
        elif len(self.get_contents()) == 1:
            pront(self.desc + f' On {obliquefy(self.pluralize("it"))} is:')
            self.list_contents()
        else:
            pront(self.desc)
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

class Furniture(Surface):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['sitting']
        self.default_state = 'sitting'
        self.add_property('immobile')

    def get_allowed_states(self):
        return self.allowed_states

    def set_allowed_states(self, l):
        assert type(l) == list, 'The allowed states must be in a list.'
        for x in l:
            assert type(x) == str, 'The allowed states must all be strings.'
        self.allowed_states = l

    def add_allowed_state(self, s):
        assert type(s) == str, 'The allowed state must be a string.'
        if s not in self.allowed_states:
            self.allowed_states.append(s)

    def remove_allowed_state(self, s):
        assert type(s) == str, 'The allowed state must be a string.'
        if s in self.allowed_states:
            self.allowed_states.remove(s)

    def get_default_state(self):
        return self.default_state

    def set_default_state(self, s):
        assert type(s) == str, 'The default state must be a string.'
        self.default_state = s

class Vehicle(Object):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['riding a vehicle']
        self.default_state = 'riding a vehicle'
        self.add_property('immobile')

    def get_allowed_states(self):
        return self.allowed_states

    def set_allowed_states(self, l):
        assert type(l) == list, 'The allowed states must be in a list.'
        for x in l:
            assert type(x) == str, 'The allowed states must all be strings.'
        self.allowed_states = l

    def add_allowed_state(self, s):
        assert type(s) == str, 'The allowed state must be a string.'
        if s not in self.allowed_states:
            self.allowed_states.append(s)

    def remove_allowed_state(self, s):
        assert type(s) == str, 'The allowed state must be a string.'
        if s in self.allowed_states:
            self.allowed_states.remove(s)

    def get_default_state(self):
        return self.default_state

    def set_default_state(self, s):
        assert type(s) == str, 'The default state must be a string.'
        self.default_state = s

class Chair(Furniture):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['sitting', 'standing atop something']
        self.default_state = 'sitting'

class Bed(Furniture):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['lying down', 'sitting', 'standing atop something']
        self.default_state = 'lying down'

class Table(Furniture):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['standing atop something', 'sitting']
        self.default_state = 'standing atop something'

class Mat(Furniture):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['standing', 'sitting', 'lying down']
        self.default_state = 'standing'

class Wrapper(Container):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.open = False
        self.locked = False
        self.add_property('openable')

    def make_open(self):
        super().make_open()
        self.remove_property('openable')

class Locker(Container):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.open = False
        self.locked = True
        self.keylist = []
        self.add_property('openable')

    def get_keylist(self):
        return self.keylist

    def add_key(self, key):
        assert isinstance(key, Object), 'The key must be an object.'
        if key not in self.keylist:
            self.keylist.append(key)

    def remove_key(self, key):
        assert isinstance(key, Object), 'The key must be an object.'
        if key in self.keylist:
            self.keylist.remove(key)

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

class Ampuole(Locker):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.open = False
        self.locked = True
        self.keylist = []

    def make_open(self):
        super().make_open()
        self.remove_property('openable')

class Ladder(Object):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.up_destination = offstage
        self.down_destination = offstage
        self.valid_up = False
        self.valid_down = False
        self.move_message = f'You climb {self.art_d()}.'
        self.add_property('immobile')
        self.add_property('unlisted')

    def set_valid_up(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.valid_up = val

    def leads_up(self):
        return self.valid_up

    def set_valid_down(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.valid_down = val

    def leads_down(self):
        return self.valid_down

    def set_up_destination(self, loc):
        assert isinstance(loc, Room), 'The destination must be a room.'
        self.up_destination = loc

    def get_up_destination(self):
        return self.up_destination

    def set_down_destination(self, loc):
        assert isinstance(loc, Room), 'The destination must be a room.'
        self.down_destination = loc

    def get_down_destination(self):
        return self.down_destination

    def get_move_up_message(self):
        return self.move_up_message

    def set_move_up_message(self, msg):
        assert type(msg) == str, 'The movement message must be a string.'
        self.move_up_message = msg

    def get_move_down_message(self):
        return self.move_down_message

    def set_move_down_message(self, msg):
        assert type(msg) == str, 'The movement message must be a string.'
        self.move_down_message = msg

class Door(Object):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.locked = False
        self.open = False
        self.locklink = True
        self.connection = self
        self.move_message = f'You go into {self.art_d()}.'
        self.add_property('immobile')
        self.add_property('openable')
        self.add_property('unlisted')
        self.add_property('portal')

    def is_open(self):
        return self.open

    def is_locked(self):
        return self.locked

    def make_open(self):
        self.open = True
        self.get_connection().open = True

    def make_closed(self):
        self.open = False
        self.get_connection().open = False

    def set_connection(self, other):
        assert isinstance(other, Door), 'Doors can only connect to doors.'
        self.connection = other
        other.connection = self

    def get_connection(self):
        return self.connection

    def link_locks(self):
        self.locklink = True

    def unlink_locks(self):
        self.locklink = False

    def get_locklink(self):
        return self.locklink

    def get_move_message(self):
        return self.move_message

    def set_move_message(self, msg):
        assert type(msg) == str, 'The movement message must be a string.'
        self.move_message = msg

    def describe(self):
        if self.is_open() and 'openable' in self.get_properties():
            pront(self.desc + f' {self.pluralize("It is")} currently open.')
        elif 'openable' in self.get_properties():
            pront(self.desc + f' {self.pluralize("It is")} currently closed.')
        else:
            pront(self.desc)
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

class LockedDoor(Door):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.locked = True

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

class KeyedDoor(LockedDoor):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.keylist = []

    def get_keylist(self):
        return self.keylist

    def add_key(self, key):
        assert isinstance(key, Object), 'The key must be an object.'
        if key not in self.keylist:
            self.keylist.append(key)

    def remove_key(self, key):
        assert isinstance(key, Object), 'The key must be an object.'
        if key in self.keylist:
            self.keylist.remove(key)

class RopeTrail(MultiObject):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.remove_property('distant')
        self.remove_property('immobile')
        self.add_property('unlisted')

    def is_visible(self):
        if self.parent_rope.is_visible() or len(self.parent_rope.get_tied_objects()) == 0:
            return False
        else:
            return super().is_visible()

    def describe(self):
        pront(self.parent_rope.desc)

    def set_loc_list(self, l):
        assert type(l) == list, 'The list of locations must be a list.'
        for x in l:
            assert isinstance(x, Room), 'Only rooms are acceptable locations.'
        ll = self.loc_list.copy()
        for y in ll:
            self.loc_list.remove(y)
            y.contents.remove(self)
        for z in l:
            self.add_loc(z)

    def get_loc_list(self):
        return self.loc_list

    def add_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        if loc not in self.loc_list:
            self.loc_list.append(loc)
            loc.contents.append(self)

    def remove_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        if loc in self.loc_list:
            self.loc_list.remove(loc)
            loc.contents.remove(self)

    def get_parent_rope(self):
        return self.parent_rope

class Rope(Object):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.trail = RopeTrail(self.name, self.id + '#trail', self.synonyms)
        self.trail.parent_rope = self
        self.room_order = [offstage]
        self.max_length = 0
        self.tied_objects = []
        self.draggable_objects = []

    def get_max_length(self):
        return self.max_length

    def set_max_length(self, n):
        assert type(n) == int and n > 0, 'The maximum length must be a positive integer.'
        self.max_length = n

    def get_room_order(self):
        return self.room_order

    def set_room_order(self, l):
        assert type(l) == list, 'The room order must be a list.'
        for x in l:
            assert isinstance(x, Room), 'Each room in the list must be a room.'
        self.room_order = l

    def add_room(self, r):
        assert isinstance(r, Room), 'The room must be a room.'
        self.room_order.append(r)

    def get_tied_objects(self):
        return self.tied_objects

    def add_tied_object(self, thing):
        assert isinstance(thing, Object), 'The tied object must be an object.'
        self.tied_objects.append(thing)

    def remove_tied_object(self, thing):
        assert isinstance(thing, Object), 'The tied object must be an object.'
        self.tied_objects.remove(thing)

    def set_tied_objects(self, l):
        assert type(l) == list, 'The list of draggable objects must be a list.'
        for x in l:
            assert isinstance(x, Object), 'Each tied object must be an object.'
        self.tied_objects = l

    def get_draggable_objects(self):
        return self.draggable_objects

    def set_draggable_objects(self, l):
        assert type(l) == list, 'The list of draggable objects must be a list.'
        for x in l:
            assert isinstance(x, Object), 'Each draggable object must be an object.'
        self.draggable_objects = l

    def add_draggable_object(self, thing):
        assert isinstance(thing, Object), 'The draggable object must be an object.'
        self.draggable_objects.append(thing)

    def remove_draggable_object(self, thing):
        assert isinstance(thing, Object), 'The draggable object must be an object.'
        self.draggable_objects.remove(thing)

    def tie_to(self, thing):
        assert isinstance(thing, Object), 'The tied object must be an object.'
        thing.child_attachments.append(self)
        self.add_tied_object(thing)
        if len(self.get_tied_objects()) == 2 and not thing.is_within(player):
            self.warp_to(thing.get_loc())

    def untie_from(self, thing):
        assert isinstance(thing, Object), 'The untied object must be an object.'
        thing.child_attachments.remove(self)
        self.remove_tied_object(thing)
        if len(self.get_tied_objects()) == 0:
            self.warp_to(thing.get_loc())

    def reverse_polarity(self):
        self.set_room_order(self.get_room_order()[::-1])
        self.set_tied_objects(self.get_tied_objects()[::-1])
        #if not self.get_room_order().count(self.get_room_order()[-1]) > 1:
            #self.trail.remove_loc(self.get_room_order()[-1])
        #self.trail.add_loc(self.get_room_order()[0])

    def update_locations(self):
        swapping = False
        if self.is_within(self.get_room_order()[0]) and len(self.get_room_order()) > 1:
            swapping = True
        if swapping or not self.is_within(self.get_room_order()[-1]):
            if len(self.get_tied_objects()) == 0:
                self.set_room_order([self.find_ultimate_room()])
            elif len(self.get_tied_objects()) == 1 and self.get_tied_objects()[0].find_ultimate_room() is self.find_ultimate_room():
                self.set_room_order([self.find_ultimate_room()])
            elif len(self.get_tied_objects()) == 2 and self.get_tied_objects()[0].find_ultimate_room() is self.find_ultimate_room() and self.get_tied_objects()[1].find_ultimate_room() is self.find_ultimate_room():
                self.set_room_order([self.find_ultimate_room()])
            else:
                if len(self.get_room_order()) > 1 and self.is_within(self.get_room_order()[-2]):
                    self.set_room_order(self.get_room_order()[0:-1])
                elif not swapping:
                    self.get_room_order().append(self.find_ultimate_room())

        if swapping:
            self.reverse_polarity()
        self.trail.set_loc_list(self.get_room_order())

    def warp_to(self, loc):
        super().warp_to(loc)
        self.update_locations()

class Button(Object):
    def activate():
        pass

class Lever(Object):
    def activate():
        pass

class Player(Container):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.wearing = []
        self.prior_loc = offstage
        self.state = 'standing'
        self.pronoun = 'you'

    def list_contents(self, n=0):
        if len(self.get_contents()) > 0:
            for x in self.get_contents():
                if ('unlisted' not in x.get_properties()) and ('player_anatomy' not in x.get_properties()):
                    w = ''
                    if 'plug' in x.get_properties() and isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (plugged into '
                        if len(x.get_tied_objects()) == 1:
                            w += f'{x.get_tied_objects()[0].art_d()})'
                        elif len(x.get_tied_objects()) == 2:
                            if x.get_tied_objects()[0] is x.get_tied_objects()[1]:
                                w += f'{x.get_tied_objects()[0].art_d()} at both ends)'
                            elif x.get_tied_objects()[0].art_i() == x.get_tied_objects()[1].art_i():
                                w += f'{x.get_tied_objects()[0].art_i()} at both ends)'
                            else:
                                w += f'{x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (tied to '
                        if len(x.get_tied_objects()) == 1:
                            w += f'{x.get_tied_objects()[0].art_d()})'
                        elif len(x.get_tied_objects()) == 2:
                            if x.get_tied_objects()[0] is x.get_tied_objects()[1]:
                                w += f'{x.get_tied_objects()[0].art_d()} at both ends)'
                            elif x.get_tied_objects()[0].art_i() == x.get_tied_objects()[1].art_i():
                                w += f'{x.get_tied_objects()[0].art_i()} at both ends)'
                            else:
                                w += f'{x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    if hasattr(x, 'parent_attachment'):
                        if 'plug' in x.get_properties():
                            w += f' (plugged into {x.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {x.get_parent_attachment().art_d()})'
                    if 'worn' in x.get_properties():
                        w += ' (being worn)'
                    if 'lamp' in x.get_properties() and x.get_brightness() == 2:
                        w += ' (lit)'
                    pront('  ' * n + x.art_i() + w)
                    if isinstance(x, Surface) and len(x.get_contents()) > 0 and 'suppressed' not in x.get_properties():
                        pront('  ' * n + f'{x.art_d().capitalize()} {self.pluralize("bears")}:')
                        x.list_contents(n+1)
                    elif isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()) and 'suppressed' not in x.get_properties():
                        pront('  ' * n + f'{x.art_d().capitalize()} {self.pluralize("contains")}:')
                        x.list_contents(n+1)

    def get_carried(self):
        l = []
        for x in self.get_contents():
            if not 'player_anatomy' in x.get_properties():
                l.append(x)
        return l

    def describe(self):
        pront(self.desc)
        self.attachment_desc_helper()

    def warp_to(self, loc):
        super().warp_to(loc)
        self.know_objects_in_loc(self.get_loc())

    def know_objects_in_loc(self, loc):
        assert isinstance(loc, Room) or isinstance(loc, Object), 'The location to be checked must be a room or an object.'
        if isinstance(loc, Room):
            for x in loc.get_contents():
                if x.is_visible():
                    self.know_objects_in_loc(x)
        elif isinstance(loc, Container) and loc.is_visible():
            loc.make_known()
            for x in loc.get_contents():
                if x.is_visible():
                    self.know_objects_in_loc(x)
        else:
            if loc.is_visible():
                loc.make_known()

    def get_prior_loc(self):
        return self.prior_loc

    def set_prior_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        self.prior_loc = loc

    def get_state(self):
        return self.state

    def set_state(self, s):
        assert type(s) == str, 'The state must be a string.'
        self.state = s

    def reset_state(self):
        if hasattr(self, 'state_position'):
            del self.state_position
        self.state = 'standing'

    def get_state_position(self):
        return self.state_position

    def set_state_position(self, thing):
        assert isinstance(thing, (Furniture, Vehicle)), 'The state position must be an article of furniture or a vehicle.'
        self.state_position = thing

player = Player('yourself','player', ['me', 'myself', 'self'])

class NPC(Container):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.add_property('unlisted')
        self.activity_desc = 'is standing here, doing nothing much in particular.'
        self.wearing = []
        self.covets = []
        self.owngreetingPulser = GreetingPulser(self)
        self.ownwanderPulser = WanderPulser(self)
        self.ownfollowPulser = FollowPulser(self)
        self.room_list = []
        self.private_room_list = []
        self.pronoun = 'they'
        self.greet_msg = 'Hello.'
        self.prior_loc = offstage
        self.greet_dur = 15
        self.last_greet_turn = -2147483648 #farthest negative turn so that NPCs greet player immediately (negative integer limit)
        self.unknown_ask_msg = 'I don\'t know anything about that subject.'
        self.unknown_tell_msg = 'I\'m not sure what to do with that information.'
        self.unknown_show_msg = 'I\'m not sure what to make of that.'
        self.ask_responses = {}
        self.tell_responses = {}
        self.show_responses = {}
        self.ask_event_triggers = []
        self.tell_event_triggers = []
        self.show_event_triggers = []

    def list_contents(self, n=0):
        if len(self.get_contents()) > 0:
            for x in self.get_contents():
                if ('unlisted' not in x.get_properties() and 'hidden' not in x.get_properties()):
                    w = ''
                    if 'plug' in x.get_properties() and isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (plugged into '
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (tied to '
                    if isinstance(x, Rope) and len(x.get_tied_objects()) == 1:
                        w += f' (tied to {x.get_tied_objects()[0].art_d()})'
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) == 2:
                        if x.get_tied_objects()[0] is x.get_tied_objects()[1]:
                            w += f'{x.get_tied_objects()[0].art_d()} at both ends)'
                        elif x.get_tied_objects()[0].art_i() == x.get_tied_objects()[1].art_i():
                            w += f'{x.get_tied_objects()[0].art_i()} at both ends)'
                        else:
                            w += f'{x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    if hasattr(x, 'parent_attachment'):
                        if 'plug' in x.get_properties():
                            w += f' (plugged into {x.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {x.get_parent_attachment().art_d()})'
                    if 'worn' in x.get_properties():
                        w += ' (being worn)'
                    if 'lamp' in x.get_properties() and x.get_brightness() == 2:
                        w += ' (lit)'
                    pront('  ' * n + x.art_i() + w)
                    if isinstance(x, Surface) and len(x.get_contents()) > 0 and 'suppressed' not in x.get_properties():
                        pront('  ' * n + f'{x.art_d().capitalize()} {self.pluralize("bears")}:')
                        x.list_contents(n+1)
                    elif isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()) and 'suppressed' not in x.get_properties():
                        pront('  ' * n + f'{x.art_d().capitalize()} {self.pluralize("contains")}:')
                        x.list_contents(n+1)

    def verify_not_all_hidden(self):
        for x in self.get_contents():
            if 'hidden' not in x.get_properties():
                return True
        return False

    def set_covets(self, l):
        assert type(l) == list, 'The coveted objects must be in a list.'
        for x in l:
            assert isinstance(x, Object), 'All coveted objects must be objects.'
        self.covets = l

    def get_covets(self):
        return self.covets

    def add_coveted(self, thing):
        assert isinstance(thing, Object), 'Only objects can be coveted.'
        if thing not in self.get_covets():
            self.covets.append(thing)

    def remove_coveted(self, thing):
        assert isinstance(thing, Object), 'Only objects can have their coveted status removed.'
        if thing in self.get_covets():
            self.covets.remove(thing)

    def set_room_list(self, l):
        assert type(l) == list, 'The permitted rooms must be in a list.'
        for x in l:
            assert isinstance(x, Room), 'Everything in the room list must be a room.'
        self.room_list = l

    def get_room_list(self):
        return self.room_list

    def add_room(self, thing):
        assert isinstance(thing, Room), 'Only rooms can be added to the room list.'
        if thing not in self.get_room_list():
            self.room_list.append(thing)

    def remove_room(self, thing):
        assert isinstance(thing, Room), 'Only rooms can be removed from the room list.'
        if thing in self.get_room_list():
            self.room_list.remove(thing)

    def set_private_list(self, l):
        assert type(l) == list, 'The private rooms must be in a list.'
        for x in l:
            assert isinstance(x, Room), 'Everything in the private room list must be a room.'
        self.private_room_list = l

    def get_private_list(self):
        return self.private_room_list

    def add_private_room(self, thing):
        assert isinstance(thing, Room), 'Only rooms can be added to the private room list.'
        if thing not in self.get_private_list():
            self.room_list.append(thing)

    def remove_private_room(self, thing):
        assert isinstance(thing, Room), 'Only rooms can be removed from the private room list.'
        if thing in self.get_private_list():
            self.room_list.remove(thing)

    def get_unknown_ask_msg(self):
        return self.unknown_ask_msg

    def set_unknown_ask_msg(self, msg):
        assert isinstance(msg, str), 'The message must be a string.'
        self.unknown_ask_msg = msg

    def get_unknown_tell_msg(self):
        return self.unknown_tell_msg

    def set_unknown_tell_msg(self, msg):
        assert isinstance(msg, str), 'The message must be a string.'
        self.unknown_tell_msg = msg

    def get_unknown_show_msg(self):
        return self.unknown_show_msg

    def set_unknown_show_msg(self, msg):
        assert isinstance(msg, str), 'The message must be a string.'
        self.unknown_show_msg = msg

    def get_ask_responses(self):
        return self.ask_responses

    def set_ask_responses(self, responses):
        assert isinstance(responses, dict), 'The dictionary of responses must be a dictionary.'
        for x in responses:
            assert isinstance(x, Object), 'The keys must all be objects.'
            assert isinstance(responses[x], tuple), 'The values must all be tuples.'
            assert isinstance(responses[x][0], str), 'Each response must be a string.'
            assert isinstance(responses[x][1], bool), 'Each quotation determiner must be a boolean.'
            assert isinstance(responses[x][2], tuple), 'Each collection of learned objects must be a tuple.'
            for y in responses[x][2]:
                assert isinstance(y, Object), 'Each learned object must be an object.'
        self.ask_responses = responses

    def add_ask_response(self, target, response, quotes = True, learned_objects = ()):
        assert isinstance(target, Object), 'The dictionary key must be an object.'
        assert isinstance(response, str), 'The dictionary value must be a string.'
        assert isinstance(quotes, bool), 'The quotation determiner must be a boolean.'
        assert isinstance(learned_objects, tuple), 'The collection of learned objects must be a tuple.'
        for x in learned_objects:
            assert isinstance(x, Object), 'Each learned object must be an object.'
        self.ask_responses[target] = (response, quotes, learned_objects)

    def get_tell_responses(self):
        return self.tell_responses

    def set_tell_responses(self, responses):
        assert isinstance(responses, dict), 'The dictionary of responses must be a dictionary.'
        for x in responses:
            assert isinstance(x, Object), 'The keys must all be objects.'
            assert isinstance(responses[x], tuple), 'The values must all be tuples.'
            assert isinstance(responses[x][0], str), 'Each response must be a string.'
            assert isinstance(responses[x][1], bool), 'Each quotation determiner must be a boolean.'
            assert isinstance(responses[x][2], tuple), 'Each collection of learned objects must be a tuple.'
            for y in responses[x][2]:
                assert isinstance(y, Object), 'Each learned object must be an object.'
        self.tell_responses = responses

    def add_tell_response(self, target, response, quotes = True, learned_objects = ()):
        assert isinstance(target, Object), 'The dictionary key must be an object.'
        assert isinstance(response, str), 'The dictionary value must be a string.'
        assert isinstance(quotes, bool), 'The quotation determiner must be a boolean.'
        assert isinstance(learned_objects, tuple), 'The collection of learned objects must be a tuple.'
        for x in learned_objects:
            assert isinstance(x, Object), 'Each learned object must be an object.'
        self.tell_responses[target] = (response, quotes, learned_objects)

    def get_show_responses(self):
        return self.show_responses

    def set_show_responses(self, responses):
        assert isinstance(responses, dict), 'The dictionary of responses must be a dictionary.'
        for x in responses:
            assert isinstance(x, Object), 'The keys must all be objects.'
            assert isinstance(responses[x], tuple), 'The values must all be tuples.'
            assert isinstance(responses[x][0], str), 'Each response must be a string.'
            assert isinstance(responses[x][1], bool), 'Each quotation determiner must be a boolean.'
            assert isinstance(responses[x][2], tuple), 'Each collection of learned objects must be a tuple.'
            for y in responses[x][2]:
                assert isinstance(y, Object), 'Each learned object must be an object.'
        self.show_responses = responses

    def add_show_response(self, target, response, quotes = True, learned_objects = ()):
        assert isinstance(target, Object), 'The dictionary key must be an object.'
        assert isinstance(response, str), 'The dictionary value must be a string.'
        assert isinstance(quotes, bool), 'The quotation determiner must be a boolean.'
        assert isinstance(learned_objects, tuple), 'The collection of learned objects must be a tuple.'
        for x in learned_objects:
            assert isinstance(x, Object), 'Each learned object must be an object.'
        self.show_responses[target] = (response, quotes, learned_objects)

    def get_ask_event_triggers(self):
        return self.ask_event_triggers

    def set_ask_event_triggers(self, triggers):
        assert isinstance(triggers, list), 'The event triggers must be in a list.'
        for x in triggers:
            assert isinstance(x, Object), 'The event triggers must all be objects.'
        self.ask_event_triggers = triggers

    def add_ask_event_trigger(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'
        if trigger not in self.get_ask_event_triggers():
            self.ask_event_triggers.append(trigger)

    def get_tell_event_triggers(self):
        return self.tell_event_triggers

    def set_tell_event_triggers(self, triggers):
        assert isinstance(triggers, list), 'The event triggers must be in a list.'
        for x in triggers:
            assert isinstance(x, Object), 'The event triggers must all be objects.'
        self.tell_event_triggers = triggers

    def add_tell_event_trigger(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'
        if trigger not in self.get_tell_event_triggers():
            self.tell_event_triggers.append(trigger)

    def get_show_event_triggers(self):
        return self.show_event_triggers

    def set_show_event_triggers(self, triggers):
        assert isinstance(triggers, list), 'The event triggers must be in a list.'
        for x in triggers:
            assert isinstance(x, Object), 'The event triggers must all be objects.'
        self.show_event_triggers = triggers

    def add_show_event_trigger(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'
        if trigger not in self.get_show_event_triggers():
            self.show_event_triggers.append(trigger)

    def do_ask_event(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'

    def do_tell_event(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'

    def do_show_event(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'

    def acquire(self, thing):
        assert isinstance(thing, Object), 'Only objects can be acquired.'
        thing.warp_to(self)

    def acquire_and_hide(self, thing):
        assert isinstance(thing, Object), 'Only objects can be acquired and hidden.'
        thing.warp_to(self)
        thing.add_property('hidden')

    def hide(self, thing):
        assert isinstance(thing, Object) and thing.get_loc() == self, 'NPCs can only hide something if it is an object they are currently holding.'
        thing.add_property('hidden')

    def reveal(self, thing):
        assert isinstance(thing, Object) and thing.get_loc() == self, 'NPCs can only reveal something if it is an object they are currently holding.'
        thing.remove_property('hidden')

    def drop(self, thing):
        assert isinstance(thing, Object) and thing.get_loc() == self, 'NPCs can only drop something if it is an object they are currently holding.'
        thing.remove_property('hidden')
        thing.warp_to(self.get_loc())

    def describe(self):
        if len(self.get_contents()) > 0 and self.verify_not_all_hidden():
            pront(self.desc + f' {self.get_pronoun().capitalize()} {self.is_are()} holding:')
            self.list_contents()
        else:
            pront(self.desc)
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

    def set_activity_desc(self, d):
        assert type(d) == str, 'The activity description must be a string.'
        self.activity_desc = d

    def get_activity_desc(self):
        return self.art_i().capitalize() + ' ' + self.activity_desc

    def follow_player(self):
        self.ownwanderPulser.deactivate() #do not wander if following the player
        self.ownfollowPulser.set_dur(0)
        self.ownfollowPulser.activate()

    def stop_following_player(self):
        self.ownfollowPulser.deactivate()
        if self.owngreetingPulser.get_activity():
            self.owngreetingPulser.reactivate()
            self.set_last_greet_turn(MasterState.turn_count)

    def wander(self, dur):
        assert type(dur) == int, 'The duration must be an integer.'
        self.ownfollowPulser.deactivate() #do not follow the player if wandering
        self.ownwanderPulser.activate()
        self.ownwanderPulser.set_dur(dur)

    def stop_wandering(self):
        self.ownwanderPulser.deactivate()

    def greet(self, dur):
        assert type(dur) == int, 'The duration must be an integer.'
        self.owngreetingPulser.activate()
        self.owngreetingPulser.set_dur(0)
        self.greet_dur = dur

    def get_greet_dur(self):
        return self.greet_dur

    def stop_greeting(self):
        self.owngreetingPulser.deactivate()

    def set_greet_msg(self, msg):
        assert type(msg) == str, 'The greeting message must be a string.'
        self.greet_msg = msg

    def get_greet_msg(self):
        return self.greet_msg

    def set_last_greet_turn(self, n):
        assert type(n) == int, 'The turn number must be an integer.'
        self.last_greet_turn = n

    def get_last_greet_turn(self):
        return self.last_greet_turn

    def greet_player(self):
        pront(f'{self.art_d()} says \"{self.get_greet_msg()}\"')

    def set_prior_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        self.prior_loc = loc

    def get_prior_loc(self, loc):
        return self.prior_loc

    def is_are(self):
        if self.get_pronoun() == 'they':
            return 'are'
        return 'is'

    def describe_taste(self):
        pront(f'{self.art_d().capitalize()} would definitely object to that.')

    def describe_touch(self):
        pront(f'{self.art_d().capitalize()} looks at you with a look of annoyance.')

def define_again_verbs(l):
    assert type(l) == list, 'The list of verbs must be a list.'
    for x in l:
        assert isinstance(x, str), 'Only strings are acceptable verb synonyms.'
    for x in l:
        verb0dict[x] = 'again'

class Verb0:

    def __init__(self, id, synonyms):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert ' ' not in id, 'The internal id cannot contain a space.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.id = id
        self.synonyms = synonyms
        for x in synonyms:
            verb0dict[x] = self.id
        verb_id_dict[self.id] = self
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb0dict[word] = self.id

    def execute(self):
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            self.body()
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self):
        pass

    def prioritize(self, thing): #template purposes, should not really be called
        return (thing, 0)

class Verb1:

    def __init__(self, id, synonyms):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert ' ' not in id, 'The internal id cannot contain a space.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.id = id
        self.synonyms = synonyms
        for x in synonyms:
            verb1dict[x] = self.id
        verb_id_dict[self.id] = self
        self.requires_sight = True
        self.requires_contact = True
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_requires_sight(self):
        return self.requires_sight

    def set_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.requires_sight = val

    def get_requires_contact(self):
        return self.requires_contact

    def set_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb1dict[word] = self.id

    def disambiguate(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + self.id.replace('|', ' ') + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    return(f'#You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + self.id.replace('|', ' ') + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize(x))
        return self.infer_nouns(prioritized_thinglist)

    def prioritize(self, thing):
        return (thing, 0)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        return new

    def execute(self, d_o):
        if self in d_o.get_remaps_d():
            d_o = d_o.get_remaps_d()[self]
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            if d_o.d_o_check(self):
                self.body(d_o)
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self, d_o):
        pass

class VerbLit:

    def __init__(self, id, synonyms):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert ' ' not in id, 'The internal id cannot contain a space.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.id = id
        self.synonyms = synonyms
        for x in synonyms:
            verblitdict[x] = self.id
        verb_id_dict[self.id] = self
        self.requires_sight = False
        self.requires_contact = False
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_requires_sight(self):
        return self.requires_sight

    def set_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.requires_sight = val

    def get_requires_contact(self):
        return self.requires_contact

    def set_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb1dict[word] = self.id

    def no_vis_notice(self, thing):
        assert isinstance(thing, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id.replace('|', ' ') + ' the ' + thing.get_name() + ' because there is no ' + thing.get_name() + ' here.')

    def disambiguate(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        return potentials.replace('_', ' ')

    def execute(self, d_o):
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            self.body(d_o)
        else:
            pront(f'You cannot do that while {player.get_state()}')

    def body(self, d_o):
        pass

class Verb2:

    def __init__(self, id, synonyms, prepositions):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert ' ' not in id, 'The internal id cannot contain a space.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        assert type(prepositions) == tuple, 'The prepositions must be in a tuple.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        for x in prepositions:
            assert type(x) == str, 'All prepositions must be strings.'
        self.id = id
        self.synonyms = synonyms
        self.prepositions = prepositions
        for x in synonyms:
            verb2dict[x] = (self.id, self.prepositions)
        verb_id_dict[self.id] = self
        self.d_o_requires_sight = True
        self.d_o_requires_contact = True
        self.i_o_requires_sight = True
        self.i_o_requires_contact = True
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_d_o_requires_sight(self):
        return self.d_o_requires_sight

    def set_d_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_sight = val

    def get_d_o_requires_contact(self):
        return self.d_o_requires_contact

    def set_d_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_contact = val

    def get_i_o_requires_sight(self):
        return self.i_o_requires_sight

    def set_i_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_sight = val

    def get_i_o_requires_contact(self):
        return self.i_o_requires_contact

    def set_i_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb2dict[word] = (self.id, self.prepositions)

    def no_vis_notice1(self, thing):
        assert isinstance(thing, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing.art_d()} ' + f' because there is no {thing.art_d()} here.')

    def no_vis_notice2(self, thing1, thing2):
        assert isinstance(thing1, Object), 'Only objects can have visibility checked.'
        assert isinstance(thing2, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + ' ' + thing1.art_d() + ' ' + self.id[self.id.index('_') + 1:].replace('|', ' ') + ' the ' + thing2.get_name() + ' because there is no ' + thing2.get_name() + ' here.')

    def disambiguate_d_o(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_d_o_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_d_o_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    pront(f'You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize_d_o(x))
        return self.infer_nouns(prioritized_thinglist)

    def disambiguate_i_o(self, d_o, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_i_o_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + d_o.get_name() + ' ' + after_(self.id.replace('|', ' ')) + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_i_o_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    return(f'#You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + d_o.get_name() + ' ' + after_(self.id.replace('|', ' ')) + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize_i_o(d_o, x))
        return self.infer_nouns(prioritized_thinglist)

    def prioritize_d_o(self, thing):
        return (thing, 0)

    def prioritize_i_o(self, thing1, thing2):
        return (thing2, 0)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        return new

    def execute(self, d_o, i_o):
        if self in d_o.get_remaps_d():
            d_o = d_o.get_remaps_d()[self]
        if self in i_o.get_remaps_i():
            i_o = i_o.get_remaps_i()[self]
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            if d_o.d_o_check(self):
                if i_o.i_o_check(self, d_o):
                    self.body(d_o, i_o)
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self, d_o, i_o):
        pass

class VerbLit2:

    def __init__(self, id, synonyms, prepositions):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert ' ' not in id, 'The internal id cannot contain a space.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        assert type(prepositions) == tuple, 'The prepositions must be in a tuple.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        for x in prepositions:
            assert type(x) == str, 'All prepositions must be strings.'
        self.id = id
        self.synonyms = synonyms
        self.prepositions = prepositions
        for x in synonyms:
            verblit2dict[x] = (self.id, self.prepositions)
        verb_id_dict[self.id] = self
        self.d_o_requires_sight = True
        self.d_o_requires_contact = True
        self.i_o_requires_sight = True
        self.i_o_requires_contact = True
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_d_o_requires_sight(self):
        return self.d_o_requires_sight

    def set_d_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_sight = val

    def get_d_o_requires_contact(self):
        return self.d_o_requires_contact

    def set_d_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_contact = val

    def get_i_o_requires_sight(self):
        return self.i_o_requires_sight

    def set_i_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_sight = val

    def get_i_o_requires_contact(self):
        return self.i_o_requires_contact

    def set_i_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb2dict[word] = (self.id, self.prepositions)

    def no_vis_notice1(self, thing):
        assert isinstance(thing, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing.art_d()} ' + f' because there is no {thing.art_d()} here.')

    def no_vis_notice2(self, thing1, thing2):
        assert isinstance(thing1, str), 'This function requires a string input.'
        assert isinstance(thing2, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing1} ' + self.id[self.id.index('_') + 1:].replace('|', ' ') + ' the' + f' {thing2.get_name()}' + ' because there is no ' + thing2.get_name() + ' here.')

    def disambiguate_d_o(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        return potentials

    def disambiguate_i_o(self, d_o, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_i_o_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + d_o.get_name() + ' ' + after_(self.id.replace('|', ' ')) + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_i_o_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    return(f'#You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + d_o.get_name() + ' ' + after_(self.id.replace('|', ' ')) + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize_i_o(d_o, x))
        return self.infer_nouns(prioritized_thinglist)

    def prioritize_d_o(self, thing):
        return (thing, 0)

    def prioritize_i_o(self, thing1, thing2):
        return (thing2, 0)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        return new

    def execute(self, d_o, i_o):
        d_o = d_o.replace('_', ' ')
        if self in i_o.get_remaps_i():
            i_o = i_o.get_remaps_i()[self]
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            if i_o.i_o_check(self, d_o):
                self.body(d_o, i_o)
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self, d_o, i_o):
        pass

class Verb2Lit:

    def __init__(self, id, synonyms, prepositions):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert ' ' not in id, 'The internal id cannot contain a space.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        assert type(prepositions) == tuple, 'The prepositions must be in a tuple.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        for x in prepositions:
            assert type(x) == str, 'All prepositions must be strings.'
        self.id = id
        self.synonyms = synonyms
        self.prepositions = prepositions
        for x in synonyms:
            verb2litdict[x] = (self.id, self.prepositions)
        verb_id_dict[self.id] = self
        self.d_o_requires_sight = True
        self.d_o_requires_contact = True
        self.i_o_requires_sight = True
        self.i_o_requires_contact = True
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_d_o_requires_sight(self):
        return self.d_o_requires_sight

    def set_d_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_sight = val

    def get_d_o_requires_contact(self):
        return self.d_o_requires_contact

    def set_d_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_contact = val

    def get_i_o_requires_sight(self):
        return self.i_o_requires_sight

    def set_i_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_sight = val

    def get_i_o_requires_contact(self):
        return self.i_o_requires_contact

    def set_i_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb2dict[word] = (self.id, self.prepositions)

    def no_vis_notice1(self, thing):
        assert isinstance(thing, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing.art_d()} ' + f' because there is no {thing.art_d()} here.')

    def no_vis_notice2(self, thing1, thing2):
        assert isinstance(thing1, str), 'This function requires a string input.'
        assert isinstance(thing2, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing1} ' + self.id[self.id.index('_') + 1:].replace('|', ' ') + ' the' + f' {thing2.get_name()}' + ' because there is no ' + thing2.get_name() + ' here.')

    def disambiguate_d_o(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_d_o_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_d_o_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    return(f'#You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize_d_o(x))
        return self.infer_nouns(prioritized_thinglist)

    def disambiguate_i_o(self, d_o, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        return potentials

    def prioritize_d_o(self, thing):
        return (thing, 0)

    def prioritize_i_o(self, thing):
        return (thing, 0)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        return new

    def execute(self, d_o, i_o):
        if self in d_o.get_remaps_d():
            d_o = d_o.get_remaps_d()[self]
        i_o = i_o.replace('_', ' ')
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            if d_o.d_o_check(self):
                self.body(d_o, i_o)
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self, d_o, i_o):
        pass

class Timer:

    def __init__(self):
        self.active = False
        self.dur = 0
        self.start_turn = 0
        MasterState.event_list.append(self)

    def activate(self):
        if not self.active:
            self.active = True
            self.start_turn = MasterState.turn_count

    def deactivate(self):
        self.active = False

    def reactivate(self):
        self.active = True
        self.start_turn = MasterState.turn_count

    def get_activity(self):
        return self.active

    def set_dur(self, n):
        assert (type(n) == int) and (n >= 0), 'The duration must be a non-negative integer.'
        self.dur = n

    def get_dur(self):
        return self.dur

    def get_start_turn(self):
        return self.start_turn

    def engage(self):
        self.deactivate()

class Pulser(Timer):

    def engage(self):
        self.reactivate()
        self.start_turn += 1

class AestheticPulser(Pulser):

    def __init__(self):
        super().__init__()
        self.percent = 100
        self.messages = []

    def get_percent(self):
        return self.percent

    def set_percent(self, n):
        assert (type(n) == int) and (n >= 0) and (n <= 100), 'The percentage must be an integer or float, greater than or equal to zero and less than or equal to one hundred.'
        self.percent = n

    def get_messages(self):
        return self.messages

    def add_message(self, msg):
        assert type(msg) == str, 'The message must be a string.'
        self.messages.append(msg)

    def remove_message(self, msg):
        assert type(msg) == str, 'The message must be a string.'
        if msg in self.get_messages():
            self.messages.remove(msg)

    def set_messages(self, l):
        assert type(l) == list, 'The messages must be in the form of a list.'
        for x in l:
            assert type(x) == str, 'The messages must all be strings.'
        self.messages = l

    def get_room_list(self):
        return self.room_list

    def add_room(self, r):
        assert isinstance(r, Room), 'The room must be an actual room.'
        self.room_list.append(r)

    def remove_room(self, r):
        assert isinstance(r, Room), 'The room must be an actual room.'
        if room in self.get_room_list():
            self.room_list.remove(r)

    def set_rooms(self, l):
        assert type(l) == list, 'The rooms must be in the form of a list.'
        for x in l:
            assert type(x) == str, 'The rooms must all be actual rooms.'
        self.room_list = l

    def engage(self):
        super().engage()
        if (random.randint(0, 100) <= self.get_percent()) and player.get_loc() in self.get_room_list():
            pront(choose(self.get_messages()))

class GreetingPulser(Pulser):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def engage(self):
        super().engage()
        if self.get_owner().get_loc() == player.get_loc() and MasterState.turn_count - self.get_owner().get_greet_dur() >= self.get_owner().get_last_greet_turn() and player.get_loc() != player.get_prior_loc() and not self.get_owner().ownfollowPulser.get_activity():
            self.get_owner().greet_player()
            self.get_owner().set_last_greet_turn(MasterState.turn_count)
            if self.get_owner().ownwanderPulser.get_activity():
                self.get_owner().ownwanderPulser.reactivate()

    def get_owner(self):
        return self.owner

    def set_owner(self):
        raise Exception('Do not attempt to change the owner of an NPC greeting schedule. You will crash the program. Why would you ever attempt this?')

class WanderPulser(Pulser):

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def get_owner(self):
        return self.owner

    def set_owner(self):
        raise Exception('Do not attempt to change the owner of an NPC wander schedule. You will crash the program. Why would you ever attempt this?')

    def keytest(self, door):
        for x in door.get_keylist():
            if x.get_loc() == self.get_owner():
                return True
        return False

    def engage(self):
        super().engage()
        l = []
        oldloc = self.get_owner().get_loc()
        k = self.get_owner().get_loc().get_exits()
        for x in k:
            if isinstance(k[x][0], Room):
                if k[x][0] in self.get_owner().get_room_list():
                    l.append(x)
            elif isinstance(k[x][0], Door):
                if k[x][0].get_connection().get_loc() in self.get_owner().get_room_list():
                    l.append(x)
        d = choose(l)
        if isinstance(k[d][0], Room):
            if self.get_owner().get_loc() == player.get_loc():
                if d == 'u':
                    pront(f'{self.get_owner().art_d().capitalize()} ascends out of view.')
                elif d == 'd':
                    pront(f'{self.get_owner().art_d().capitalize()} descends out of view.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} walks out to the {directionsdict[d]}.')
            self.get_owner().warp_to(k[d][0])
            newloc = k[d][0]
            d2 = ''
            if self.get_owner().get_loc() == player.get_loc():
                for y in newloc.get_exits():
                    if newloc.get_exits()[y][0] == oldloc:
                        d2 = y
                if d2 != '':
                    if d2 == 'u':
                        pront(f'{self.get_owner().art_d().capitalize()} comes down from above.')
                    elif d2 == 'd':
                        pront(f'{self.get_owner().art_d().capitalize()} comes up from below.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} walks in from the {directionsdict[d2]}.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} walks into the room.')
        elif isinstance(k[d][0], KeyedDoor) and not k[d][0].is_open(): #if attempting to go through a closed keyed door
            if self.keytest(k[d][0]) or not k[d][0].is_locked():
                if self.get_owner().get_loc() == player.get_loc():
                    if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                        pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()}, goes through {obliquefy(k[d][0].pluralize("it"))}, and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()} and goes through {obliquefy(k[d][0].pluralize("it"))}.')
                self.get_owner().warp_to(k[d][0].get_connection().get_loc())
                if not (k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list()):
                    k[d][0].make_open(); k[d][0].unlock()
                if self.get_owner().get_loc() == player.get_loc():
                    if self.get_owner().get_loc() == player.get_loc():
                        if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                            pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                        else:
                            pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()}.')
        elif isinstance(k[d][0], LockedDoor) and not k[d][0].is_open(): #if attempting to go through a closed keyed door
            if self.get_owner().get_loc() == player.get_loc():
                if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                    pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()}, goes through {obliquefy(k[d][0].pluralize("it"))}, and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()} and goes through {obliquefy(k[d][0].pluralize("it"))}.')
            self.get_owner().warp_to(k[d][0].get_connection().get_loc())
            if not (k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list()):
                k[d][0].make_open(); k[d][0].unlock()
            if self.get_owner().get_loc() == player.get_loc():
                if self.get_owner().get_loc() == player.get_loc():
                    if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()}.')
        elif isinstance(k[d][0], Door) and not k[d][0].is_open(): #if attempting to go through a closed keyed door
            if self.get_owner().get_loc() == player.get_loc():
                if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                    pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()}, goes through {obliquefy(k[d][0].pluralize("it"))}, and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()} and goes through {obliquefy(k[d][0].pluralize("it"))}.')
            self.get_owner().warp_to(k[d][0].get_connection().get_loc())
            if not (k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list()):
                k[d][0].make_open()
            if self.get_owner().get_loc() == player.get_loc():
                if self.get_owner().get_loc() == player.get_loc():
                    if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()}.')
        else:
            if self.get_owner().get_loc() == player.get_loc():
                if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                    pront(f'{self.get_owner().art_d().capitalize()} goes through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} goes through {k[d][0].art_d()}.')
            self.get_owner().warp_to(k[d][0].get_connection().get_loc())
            if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                k[d][0].make_closed()
                if isinstance(d, KeyedDoor) and self.keytest(d) or isinstance(d, LockedDoor):
                    k[d][0].make_locked()
            if self.get_owner().get_loc() == player.get_loc():
                if self.get_owner().get_loc() == player.get_loc():
                    if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()}.')
        self.get_owner().set_prior_loc(oldloc)
        if self.get_owner().get_loc() == player.get_loc() and MasterState.turn_count - self.get_owner().get_greet_dur() >= self.get_owner().get_last_greet_turn():
            self.get_owner().greet_player()
            self.get_owner().set_last_greet_turn(MasterState.turn_count)

class FollowPulser(Pulser):

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def get_owner(self):
        return self.owner

    def set_owner(self):
        raise Exception('Do not attempt to change the owner of an NPC follow schedule. You will crash the program. Why would you ever attempt this?')

    def engage(self):
        super().engage()
        if player.get_loc() != player.get_prior_loc():
            self.get_owner().set_prior_loc(self.get_owner().get_loc())
            self.get_owner().warp_to(player.get_loc())
            pront(self.get_owner().get_activity_desc())

def sequence(words, conj):
    assert type(words) == list, 'The words must be in a list.'
    for x in words:
        assert type(x) == str, 'All words must be strings.'
    assert type(conj) == str, 'The conjunction must be a string.'
    if len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return words[0] + ' ' + conj + ' ' + words[1]
    else:
        temp = ''
        for x in range(len(words) - 1):
            temp += words[x]; temp += ', '
        temp += conj; temp += ' '; temp += words[-1]
        return temp

def beautify_sequence(words, conj):
    assert type(words) == list, 'The words must be in a list.'
    for x in words:
        assert type(x) == str, 'All words must be strings.'
    assert type(conj) == str, 'The conjunction must be a string.'
    if len(words) == 1:
        return 'the ' + beautify_noun(words[0])
    elif len(words) == 2:
        return 'the ' + beautify_noun(words[0]) + ' ' + conj + ' the ' + beautify_noun(words[1])
    else:
        temp = ''
        for x in range(len(words) - 1):
            temp += 'the '; temp += beautify_noun(words[x]); temp += ', '
        temp += conj; temp += ' the '; temp += beautify_noun(words[-1])
        return temp

def before_(text):
    return (text[:text.index('_')])

def after_(text):
    return (text[text.index('_') + 1:])

class Perception():
    def __init__(self, source):
        assert isinstance(source, Room) or isinstance(source, Object), 'The source of the perception must be a room or an object.'
        self.source = source
        self.desc = 'You perceive something.'
        self.invisible_desc = 'You perceive something.'
        self.activity = True
        self.is_smell = False
        self.is_sound = False

    def make_sound(self):
        self.source.set_sound_description(self)
        self.is_smell = False
        self.is_sound = True

    def make_smell(self):
        self.source.set_smell_description(self)
        self.is_smell = True
        self.is_sound = False

    def is_sound(self):
        return self.is_sound

    def is_smell(self):
        return self.is_smell

    def set_description(self, desc):
        assert isinstance(desc, str), 'The description must be a string.'
        self.desc = desc

    def set_invisible_description(self, desc):
        assert isinstance(desc, str), 'The invisible description must be a string.'
        self.invisible_desc = desc

    def get_description(self):
        return self.desc

    def get_invisible_description(self):
        return self.invisible_desc

    def get_source(self):
        return self.source

    def get_activity(self):
        return self.activity

class PerceptionLink():
    def __init__(self, input, output):
        assert isinstance(input, Object), 'The perception input must be an object.'
        assert isinstance(output, Object), 'The perception output must be an object.'
        self.input = input
        self.output = output
        self.transparent_sound = False
        self.transparent_smell = False
        self.activity = True
        self.inactive_sound_description = 'You hear nothing.'
        self.inactive_smell_description = 'You smell nothing.'

    def get_input(self):
        return self.input

    def get_output(self):
        return self.output

    def connect_sound(self):
        self.output.set_sound_description(self)
        self.transparent_sound = True

    def connect_smell(self):
        self.output.set_smell_description(self)
        self.transparent_sound = True

    def get_transparent_sound(self):
        return self.transparent_sound

    def get_transparent_smell(self):
        return self.transparent_smell

    def activate(self):
        self.activity = True

    def deactivate(self):
        self.activity = False

    def get_activity(self):
        return self.activity

    def get_inactive_sound_description(self):
        return self.inactive_sound_description

    def get_inactive_smell_description(self):
        return self.inactive_smell_description

    def set_inactive_sound_description(self, desc):
        assert isinstance(desc, str), 'The description must be a string.'
        self.inactive_sound_description = desc

    def set_inactive_smell_description(self, desc):
        assert isinstance(desc, str), 'The description must be a string.'
        self.inactive_smell_description = desc

class MasterState():
    turn_count = 0
    win_states = {
    0 : 'You win.'
    }
    lose_states = {
    0 : 'You lose.',
    }

    event_list = []

def win(n):
    assert n in MasterState.win_states
    print()
    pront(MasterState.win_states[n])
    print()
    raise SystemExit(0)

def lose(n):
    assert n in MasterState.lose_states
    print()
    pront(MasterState.lose_states[n])
    print()
    raise SystemExit(0)

def add_win_condition(c, s):
    assert type(s) == str, 'The win message must be a string.'
    MasterState.win_states[c] = s

def add_lose_condition(c, s):
    assert type(s) == str, 'The loss message must be a string.'
    MasterState.lose_states[c] = s

def inc_turn():
    run_events()
    player.set_prior_loc(player.get_loc())
    MasterState.turn_count += 1

def run_events():
    for x in MasterState.event_list:
        if x.get_activity() and x.get_dur() + x.get_start_turn() == MasterState.turn_count:
            x.engage()

def beautify_noun(text):
    text = text.replace('_', ' ')
    if '#' in text:
        return (text[:text.index('#')])
    return text

def stringify_tuple(input):
    output = ''
    for x in input:
        output += '~'; output += x
    return output[1:]

def pront(text): #printing, but with wrapped text (will not work for blank lines, use print() instead, fixed so that it will interpret \n correctly)
    print(textwrap.fill(text, width = 80, replace_whitespace = False))

def choose(somelist):
    return somelist[random.randint(0,len(somelist) - 1)]

def no_reach_notice(thing):
    assert isinstance(thing, Object), 'Only objects can have reachability checked.'
    if 'distant' in thing.get_properties():
        pront(f'You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
    elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
        pront(f'You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
    elif isinstance(thing.get_loc(), Container):
        pront(f'You cannot reach {thing.art_d()} through a closed container.')

define_again_verbs(['g','again', 'do again', 'do it again', 'do it over', 'do over'])

def start_message():
    print()
    pront('Welcome to the text adventure engine game.')
    print()
    player.know_objects_in_loc(player.get_loc())
    player.get_loc().describe()
    print()

#rooms

room1 = Room()
room2 = Room()

#player stuff
player.warp_to(offstage)
player.set_description('At the moment, you happen to be yourself. It would be concerning if this were not so.')
player.add_property('unlisted')
player.add_property('custom_immobile')
player.set_custom_immobile_message('To attempt such a feat would be incredibly foolish.')
player.set_definite_article('')
player.set_indefinite_article('')
player.make_known()

hands = Object('hands', 'hands', ['hands', 'hand'])
hands.set_description('They are your own two hands.')
hands.set_bulk(0)
hands.warp_to(player)
hands.add_property('player_anatomy')
hands.set_definite_article('your')
hands.set_indefinite_article('your')
hands.make_plural()
#end of player stuff

class Debug(Verb0):
    def body(self):
        pass
debug = Debug('debug', ['debug'])

class Look(Verb0):
    def body(self):
        player.get_loc().describe()
        player.know_objects_in_loc(player.get_loc())
        inc_turn()
look = Look('look_around', ['l','look','look around', 'stare', 'gaze'])

class Listen(Verb0):
    def body(self):
        player.get_loc().describe_sound()
        inc_turn()
listen = Listen('listen', ['listen', 'hear', 'hearken', 'harken'])

class Smell(Verb0):
    def body(self):
        player.get_loc().describe_smell()
        inc_turn()
smell = Smell('smell#', ['smell', 'sniff'])

class Wait(Verb0):
    def body(self):
        pront('You wait for a brief moment.')
        inc_turn()
wait = Wait('wait', ['wait', 'z'])

class Stand(Verb0):
    def body(self):
        if player.get_state() == 'standing':
            pront('You are already standing.')
        else:
            if hasattr(player, 'state_position'):
                if player.get_state() == 'standing atop something':
                    pront(f'You step down off of {player.get_state_position().art_d()}.')
                else:
                    pront(f'You stand up from {player.get_state_position().art_d()}.')
                player.reset_state()
            else:
                player.set_state('standing')
                pront('You stand up.')
            inc_turn()
stand = Stand('stand', ['stand', 'stand up', 'get up', 'get down', 'get off'])

class Sit(Verb0):
    def body(self):
        if player.get_state() == 'sitting':
            pront('You are already sitting.')
        else:
            if hasattr(player, 'state_position'):
                if 'sitting' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to sitting on {player.get_state_position().art_d()}.')
                    player.set_state('sitting')
                    inc_turn()
                else:
                    pront(f'You cannot sit on {player.get_state_position().art_d()}.')
            else:
                player.set_state('sitting')
                if player.get_state() == 'lying down':
                    pront('You sit up.')
                else:
                    pront('You sit down.')
                inc_turn()
sit = Sit('sit', ['sit', 'sit up', 'sit down'])

class Lie(Verb0):
    def body(self):
        if player.get_state() == 'lying down':
            pront('You are already lying down.')
        else:
            if hasattr(player, 'state_position'):
                if 'lying down' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to lying on {player.get_state_position().art_d()}.')
                    player.set_state('lying down')
                    inc_turn()
                else:
                    pront(f'You cannot lie on {player.get_state_position().art_d()}.')
            else:
                player.set_state('lying down')
                pront('You lie down.')
                inc_turn()
lie = Lie('lie', ['lie', 'lie down'])

class Quit(Verb0):
    def body(self):
        raise SystemExit(0)
quit = Quit('quit', ['quit'])

class Meme(Verb0):
    def body(self):
        pront('A hollow voice says, "Fool."')
        inc_turn()
meme = Meme('meme', ['git gud', 'bean', 'beans', 'borgar', 'shak', 'frie', 'hecc', 'meem', 'meme', 'it is wednesday, my dudes', 'duck', 'ducc', 'all birds are ducks', 'plugh', 'xyzzy', 'count leaves', 'kek', 'fr*ck', 'h*ck', 'finsh', 'fonsh', 'sheej', 'sheej tits', 'i hate sand', 'thicc', 'chungus', 'big chungus', 'waluigi', 'luigi', 'did you ever hear the tradgedy of darth plagueis the wise?', 'arma virumque cano', 'arma vivmqve cano', 'beef', 'beeves', 'b', 'leopards ate my face', 'embiggen', 'imbibe', 'succ', 'whomst', 'hewwo', '42', '69', '420', 'heck'])

class Blink(Verb0):
    def body(self):
        pront('You blink.')
        inc_turn()
blink = Blink('blink', ['blink', 'nictate'])

class Jump(Verb0):
    def body(self):
        pront('You jump up and down on the spot.')
jump = Jump('jump', ['jump', 'leap', 'hop'])
jump.set_required_states(['standing', 'standing atop something'])

class Help(Verb0):
    def body(self):
        pront('In this game, you can move in ten directions: north, south,' +
              ' west, east, northwest, northeast, southwest, southeast, up,' +
              ' and down. These commands can be abbreviated to "n," "s," "w,"' +
              ' "e," "nw," "ne," "sw," "se," "u," and "d." Also useful is the'
              ' "examine" command, or "x" for short. "Quit" exits the game.')
help = Help('help', ['help','help me'])

class Hello(Verb0):
    def body(self):
        audience = False
        for x in player.get_loc().get_contents():
            if isinstance(x, NPC):
                if not audience:
                    audience = True
                    pront('You say "Hello."')
                if x.owngreetingPulser.get_activity():
                    x.greet_player()
                    x.owngreetingPulser.reactivate()
                    if x.ownwanderPulser.get_activity():
                        x.ownwanderPulser.reactivate()
                else:
                    pront(f'{x.art_d().capitalize()} does not respond.')
        if not audience:
            pront('You say "Hello," but notbody is there to respond.')
        inc_turn()
hello = Hello('hello', ['hello', 'hi', 'say hello', 'say hi'])

class Go_north(Verb0):
    def body(self):
        if 'n' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['n']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'n' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('n'):
                if 'n' in player.get_loc().get_exits():
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'n' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['n'])
go_north = Go_north('go_north', ['n', 'north', 'go north', 'walk north'])
go_north.set_required_states(['standing'])

class Go_south(Verb0):
    def body(self):
        if 's' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['s']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 's' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('s'):
                if 's' in player.get_loc().get_exits():
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 's' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['s'])
go_south = Go_south('go_south', ['s', 'south', 'go south', 'walk south'])
go_south.set_required_states(['standing'])

class Go_west(Verb0):
    def body(self):
        if 'w' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['w']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'w' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('w'):
                if 'w' in player.get_loc().get_exits():
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'w' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['w'])
go_west = Go_west('go_west', ['w', 'west', 'go west', 'walk west'])
go_west.set_required_states(['standing'])

class Go_east(Verb0):
    def body(self):
        if 'e' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['e']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'e' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('e'):
                if 'e' in player.get_loc().get_exits():
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'e' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['e'])
go_east = Go_east('go_east', ['e', 'east', 'go east', 'walk east'])
go_east.set_required_states(['standing'])

class Go_northwest(Verb0):
    def body(self):
        if 'nw' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['nw']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'nw' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('nw'):
                if 'nw' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['nw']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'nw' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['nw'])
go_northwest = Go_northwest('go_northwest', ['nw', 'northwest', 'go northwest', 'walk northwest'])
go_northwest.set_required_states(['standing'])

class Go_northeast(Verb0):
    def body(self):
        if 'ne' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['ne']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'ne' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('ne'):
                if 'ne' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['ne']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'ne' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['ne'])
go_northeast = Go_northeast('go_northeast', ['ne', 'northeast', 'go northeast', 'walk northeast'])
go_northeast.set_required_states(['standing'])

class Go_southwest(Verb0):
    def body(self):
        if 'sw' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['sw']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'sw' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('sw'):
                if 'sw' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['sw']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'sw' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['sw'])
go_southwest = Go_southwest('go_southwest', ['sw', 'southwest', 'go southwest', 'walk southwest'])
go_southwest.set_required_states(['standing'])

class Go_southeast(Verb0):
    def body(self):
        if 'se' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['se']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'se' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('se'):
                if 'se' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['se']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'se' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['se'])
go_southeast = Go_southeast('go_southeast', ['se', 'southeast', 'go southeast', 'walk southeast'])
go_southeast.set_required_states(['standing'])

class Go_up(Verb0):
    def body(self):
        if 'u' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['u']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'u' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('u'):
                if 'u' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['u']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'u' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['u'])
go_up = Go_up('go_up', ['u', 'up', 'go up'])
go_up.set_required_states(['standing'])

class Go_down(Verb0):
    def body(self):
        if player.get_loc().travelcheck('d'):
            if 'd' in player.get_loc().get_exits():
                temp = player.get_loc().get_exits()['d']
                if isinstance(temp[0], Room):
                    pront(temp[1])
                    player.warp_to(temp[0])
                    player.get_loc().describe()
                    inc_turn()
                else:
                    if temp[0].is_open():
                        pront(temp[1])
                        player.warp_to(temp[0].get_connection().get_loc())
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
            elif 'd' in player.get_loc().get_nexits():
                pront(player.get_loc().get_nexits()['d'])
go_down = Go_down('go_down', ['d', 'down', 'go down'])
go_down.set_required_states(['standing'])

class Check_inventory(Verb0):
    def body(self):
        if len(player.get_carried()) == 0:
            pront('You are not carrying anything.')
        else:
            pront('You are carrying:')
            player.list_contents()
check_inventory = Check_inventory('check_inventory', ['i', 'inventory', 'check inventory', 'take inventory'])

class Get_all(Verb0):
    def body(self):
        temp = []
        for x in player.get_loc().get_contents():
            taketest = True
            if x.is_reachable():
                for y in ['custom_immobile', 'immobile', 'anchored', 'component', 'no_implicit_get']:
                    if y in x.get_properties():
                        taketest = False
                        break
                if isinstance(x, NPC) or isinstance(x, RopeTrail):
                    taketest = False
                if isinstance(x, Rope) and len(x.get_tied_objects()) > 1:
                    taketest = False
                if hasattr(x, 'parent_attachment'):
                    taketest = False
                if taketest:
                    temp.append(x)
        if len(temp) == 0:
            pront('There is nothing here that you can pick up.')
        else:
            for z in temp:
                if z.get_bulk() > player.get_capacity():
                    pront(f'{z.art_d().capitalize()} {z.pluralize("is")} too big to carry around.')
                elif z.get_bulk() + player.get_content_bulk() > player.get_capacity():
                    pront(f'You are carrying too much to be able to get {z.art_d()}.')
                else:
                    z.warp_to(player)
                    z.remove_property('initialize')
                    pront(f'You pick up {z.art_d()}.')
            inc_turn()
get_all = Get_all('get_all', ['get all', 'get everything', 'pick up all', 'pick up everything', 'take all', 'take everything', 'acquire all', 'acquire everything', 'grab all', 'grab everything', 'yoink all', 'yoink everything'])

class Drop_all(Verb0):
    def body(self):
        temp = []
        for x in player.get_contents():
            rope_test = (isinstance(x, Rope) and len(x.get_tied_objects()) > 1) or (isinstance(x, Rope) and len(x.get_tied_objects()) == 1 and x.get_tied_objects()[0].is_within(player))
            if not(('component' in x.get_properties() or 'player_anatomy' in x.get_properties()) or hasattr(x, 'parent_attachment')) and not rope_test:
                temp.append(x)
        if len(temp) == 0:
            pront('You are not holding anything at the moment.')
        else:
            for z in temp:
                z.warp_to(player.get_loc())
                pront(f'You drop {z.art_d()}.')
            inc_turn()
drop_all = Drop_all('drop_all', ['drop all', 'drop everything', 'put down all', 'put down everything'])

class Examine(Verb1):
    def body(self, d_o):
        if player.get_loc().is_illuminated():
            d_o.describe()
            inc_turn()
        else:
            if d_o.get_brightness() == 1:
                d_o.describe()
                inc_turn()
            else:
                pront(f'It is too dark to see {d_o.art_d()} clearly.')
examine = Examine('examine', ['x', 'examine', 'inspect', 'look at', 'check', 'gaze at', 'stare at', 'view', 'investigate', 'behold', 'what is'])
examine.set_requires_contact(False)

class Listen_to(Verb1):
    def body(self, d_o):
        if d_o.is_audible():
            d_o.describe_sound()
        else:
            pront('You hear nothing.')
        inc_turn()
listen_to = Listen_to('listen|to', ['hear', 'listen to', 'harken', 'hearken'])
listen_to.set_requires_contact(False)

class Smell1(Verb1):
    def body(self, d_o):
        if d_o.is_smellable():
            d_o.describe_smell()
        else:
            pront('You smell nothing.')
        inc_turn()
smell1 = Smell1('smell', ['smell', 'sniff'])
smell1.set_requires_contact(False)

class Taste(Verb1):
    def body(self, d_o):
        if d_o.is_tasteable():
            d_o.describe_taste()
            inc_turn()
        else:
            pront(f'You cannot taste {d_o.art_d()} because you cannot reach {obliquefy(d_o.get_pronoun())}.')
taste = Taste('taste', ['taste', 'lick'])
taste.set_requires_contact(False)

class Touch(Verb1):
    def body(self, d_o):
        if d_o.is_touchable():
            d_o.describe_touch()
            inc_turn()
        else:
            pront(f'You cannot touch {d_o.art_d()} because you cannot reach {obliquefy(d_o.get_pronoun())}.')
touch = Touch('touch', ['touch', 'feel', 'prod', 'poke', 'tap', 'stroke'])
touch.set_requires_contact(False)

class Get(Verb1):
    def body(self, d_o):
        if (isinstance(d_o, MultiObject) or (d_o.is_within(player.get_loc()) and (not d_o.get_loc() == (player)))) and d_o.is_reachable():
            if 'custom_immobile' in d_o.get_properties():
                pront(d_o.get_custom_immobile_message())
            elif 'immobile' in d_o.get_properties():
                pront(f'{d_o.art_d().capitalize()} cannot be moved.')
            elif 'anchored' in d_o.get_properties():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} anchored in place.')
            elif 'component' in d_o.get_properties():
                if d_o.is_plural():
                    pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                else:
                    pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
            elif isinstance(d_o, NPC):
                pront(f'{d_o.art_d().capitalize()} might object to that.')
            elif not isinstance(d_o, MultiObject) and isinstance(d_o.get_loc(), NPC) and 'proffered' not in d_o.get_properties():
                pront(f'{d_o.get_loc().art_d().capitalize()} might object to that.')
            elif isinstance(d_o, RopeTrail) and len(d_o.get_parent_rope().get_tied_objects()) > 1:
                if 'plug' in d_o.get_parent_rope().get_properties():
                    pront(f'You cannot pick up {d_o.get_parent_rope().art_d()} while {d_o.get_parent_rope().get_pronoun()} {d_o.get_parent_rope().pluralize("is")} plugged in at both ends.')
                else:
                    pront(f'You cannot pick up {d_o.get_parent_rope().art_d()} while {d_o.get_parent_rope().get_pronoun()} {d_o.get_parent_rope().pluralize("is")} tied at both ends.')
            elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 1:
                if 'plug' in d_o.get_properties():
                    pront(f'You cannot pick up {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged in at both ends.')
                else:
                    pront(f'You cannot pick up {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} tied at both ends.')
            elif d_o.get_bulk() > player.get_capacity():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} too big to carry around.')
            elif d_o.get_bulk() + player.get_content_bulk() > player.get_capacity():
                pront(f'You are carrying too much to be able to get {d_o.pluralize("that")}.')
            elif isinstance(d_o, RopeTrail):
                p = d_o.get_parent_rope()
                c = p.get_room_order().index(player.get_loc())
                p.set_room_order(p.get_room_order()[:c+1])
                p.warp_to(player)
                pront(f'You gather up {p.art_d()} and pick it up.')
            else:
                d_o.remove_property('initialize')
                if 'proffered' in d_o.get_properties() and isinstance(d_o.get_loc(), NPC):
                    pront(f'You take {d_o.art_d()} from {d_o.get_loc().art_d()}.')
                elif hasattr(d_o, 'parent_attachment'):
                    t = d_o.get_parent_attachment()
                    d_o.detach()
                    if 'plug' in d_o.get_properties():
                        pront(f'You unplug {d_o.art_d()} from {t.art_d()} and pick {obliquefy(d_o.get_pronoun())} up.')
                    else:
                        pront(f'You detach {d_o.art_d()} from {t.art_d()} and pick {obliquefy(d_o.get_pronoun())} up.')
                else:
                    pront(f'You pick up {d_o.art_d()}.')
                d_o.warp_to(player)
                inc_turn()
        elif d_o in player.get_contents():
            if 'player_anatomy' in d_o.get_properties():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already part of your own body.')
            elif 'component' in d_o.get_properties():
                if d_o.is_plural():
                    pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                else:
                    pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
            else:
                pront(f'You already have {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        for x in ['player_anatomy', 'component', 'custom_immobile', 'immobile', 'anchored']:
            if x in d_o.get_properties():
                priority -= 1
        if d_o in player.get_contents():
            priority -= 5
        if isinstance(d_o, NPC):
            priority -= 1
        return (d_o, priority)
get = Get('get', ['get', 'pick up', 'acquire', 'take', 'grab', 'yoink', 'hold', 'obtain'])

class Get_all_but(Verb1):
    def body(self, d_o):
        temp = []
        for x in player.get_loc().get_contents():
            taketest = True
            if x.is_reachable():
                for y in ['custom_immobile', 'immobile', 'anchored', 'component', 'no_implicit_get']:
                    if y in x.get_properties():
                        taketest = False
                        break
                if isinstance(x, NPC) or isinstance(x, RopeTrail):
                    taketest = False
                if hasattr(x, 'parent_attachment'):
                    taketest = False
                if isinstance(x, Rope) and len(x.get_tied_objects()) > 1:
                    taketest = False
                if taketest and (x != d_o):
                    temp.append(x)
        if len(temp) == 0:
            if d_o.is_reachable() and not(d_o.get_loc() == player):
                pront('There is nothing else here that you can pick up.')
            else:
                pront('There is nothing here that you can pick up.')
        else:
            for z in temp:
                if z.get_bulk() > player.get_capacity():
                    pront(f'{z.art_d().capitalize()} {z.pluralize("is")} too big to carry around.')
                elif z.get_bulk() + player.get_content_bulk() > player.get_capacity():
                    pront(f'You are carrying too much to be able to get {z.art_d()}.')
                else:
                    z.warp_to(player)
                    z.remove_property('initialize')
                    pront(f'You pick up {z.art_d()}.')
            inc_turn()
get_all_but = Get_all_but('get|all|but', ['get all but', 'get everything but', 'pick up all but', 'pick up everything but', 'take all but', 'take everything but', 'acquire all but', 'acquire everything but', 'grab all but', 'grab everything but', 'yoink all but', 'yoink everything but', 'get all except', 'get everything except', 'pick up all except', 'pick up everything except', 'take all except', 'take everything except', 'acquire all except', 'acquire everything except', 'grab all except', 'grab everything except', 'yoink all except', 'yoink everything except'])
get_all_but.set_requires_contact(False)

class Drop(Verb1):
    def body(self, d_o):
            if 'component' in d_o.get_properties() and d_o in player.get_contents():
                if d_o.is_plural():
                    pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                else:
                    pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
            elif hasattr(d_o, 'parent_attachment'):
                if 'plug' in d_o.get_properties():
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged into {d_o.get_parent_attachment().art_d()}.')
                else:
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} attached to {d_o.get_parent_attachment().art_d()}.')
            elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 1:
                if 'plug' in d_o.get_properties():
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged in at both ends.')
                else:
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} tied at both ends.')
            elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) == 1 and d_o.get_tied_objects()[0].is_within(player):
                if 'plug' in d_o.get_properties():
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged into {d_o.get_tied_objects()[0].art_d()}.')
                else:
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} tied to {d_o.get_tied_objects()[0].art_d()}.')
            elif 'player_anatomy' in d_o.get_properties():
                pront(f'You are unwilling to attempt separating {d_o.art_d()} from your own body.')
            elif d_o in player.get_contents():
                d_o.warp_to(player.get_loc())
                pront(f'You drop {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'You do not have {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if d_o in player.get_contents():
            priority += 5
        if 'component' in d_o.get_properties():
            priority -= 10
        if hasattr(d_o, 'parent_attachment'):
            priority -= 10
        if 'player_anatomy' in d_o.get_properties():
            priority -= 10
        return (d_o, priority)
drop = Drop('drop', ['drop', 'put down'])

class Drop_all_but(Verb1):
    def body(self, d_o):
        temp = []
        for x in player.get_contents():
            rope_test = (isinstance(x, Rope) and len(x.get_tied_objects()) > 1) or (isinstance(x, Rope) and len(x.get_tied_objects()) == 1 and x.get_tied_objects()[0].is_within(player))
            if not(('component' in x.get_properties() or 'player_anatomy' in x.get_properties()) or hasattr(x, 'parent_attachment')) and not rope_test:
                if x != d_o:
                    temp.append(x)
        if len(temp) == 0:
            if d_o.get_loc() == player:
                pront('You are not holding anything else at the moment.')
            else:
                pront('You are not holding anything at the moment.')
        else:
            for z in temp:
                z.warp_to(player.get_loc())
                pront(f'You drop {z.art_d()}.')
            inc_turn()
drop_all_but = Drop_all_but('drop|all|but', ['drop all but', 'drop everything but', 'put down all but', 'put down everything but', 'drop all except', 'drop everything except', 'put down all except', 'put down everything except'])
drop_all_but.set_requires_contact(False)

class Go_to(Verb1):
    def body(self, d_o):
        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already nearby. You could reach over and touch {d_o.art_d()} if you so wished.')
go_to = Go_to('go|to', ['approach', 'go to', 'go towards', 'move to', 'move towards', 'walk to', 'walk towards'])

class Turn(Verb1):
    def body(self, d_o):
        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be turned.')
turn = Turn('turn', ['turn', 'twist', 'crank', 'rotate'])

class Wear(Verb1):
    def body(self, d_o):
        if d_o.get_loc() == player:
            if 'clothing' in d_o.get_properties() and not 'worn' in d_o.get_properties():
                pront(f'You put on {d_o.art_d()}.')
                d_o.add_property('worn')
                inc_turn()
            elif 'worn' in d_o.get_properties():
                pront(f'You are already wearing {d_o.art_d()}.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be worn.')
        else:
            pront(f'You are not holding {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if d_o in player.get_contents() and 'clothing' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
wear = Wear('wear', ['wear', 'put on', 'slip on', 'equip', 'don'])

class Take_off(Verb1):
    def body(self, d_o):
        if d_o.get_loc() == player:
            if 'worn' in d_o.get_properties():
                pront(f'You take off {d_o.art_d()}.')
                d_o.remove_property('worn')
                inc_turn()
            else:
                pront(f'You are not wearing {d_o.art_d()}.')
        else:
            pront(f'You are not in posession of {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if d_o in player.get_contents() and 'worn' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
take_off = Take_off('take|off', ['doff', 'unequip', 'take off', 'slip off', 'divest myself of', 'divest me of'])

class Remove(Verb1):
    def body(self, d_o):
        if d_o.get_loc() == player and 'worn' in d_o.get_properties():
            take_off.body(d_o)
        else:
            detach.body(d_o)

    def prioritize(self, d_o):
        priority = 0
        if d_o in player.get_contents() and 'worn' in d_o.get_properties():
            priority += 5
        elif hasattr(d_o, 'parent_attachment') or (isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 0):
            priority += 5
        return (d_o, priority)
remove = Remove('remove', ['remove'])

class Enter(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Door) and 'enterable' in d_o.get_properties():
            if d_o.is_open():
                if not player.check_taut_ropes(d_o.get_connection().get_loc()):
                    pront(d_o.get_move_message())
                    player.warp_to(d_o.get_connection().get_loc())
                    player.get_loc().describe()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} closed.')
        else:
            pront(f'{d_o.art_d().capitalize()} cannot be entered.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'enterable' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority += 2
        return (d_o, priority)
enter = Enter('enter', ['enter', 'get in', 'go in', 'go into', 'walk in', 'walk into', 'move in', 'move into', 'climb in', 'climb into'])
enter.set_required_states(['standing'])

class Exit(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Door) and 'exitable' in d_o.get_properties():
            if d_o.is_open():
                if not player.check_taut_ropes(d_o.get_connection().get_loc()):
                    pront(d_o.get_move_message())
                    player.warp_to(d_o.get_connection().get_loc())
                    player.get_loc().describe()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} closed.')
        else:
            pront(f'{d_o.art_d().capitalize()} cannot be exited.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'exitable' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority += 2
        return (d_o, priority)
exit = Exit('exit', ['exit', 'get out of', 'walk out of', 'move out of', 'leave', 'climb out of'])
exit.set_required_states(['standing'])

class Go_through(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Door) and 'portal' in d_o.get_properties():
            if d_o.is_open():
                if not player.check_taut_ropes(d_o.get_connection().get_loc()):
                    pront(d_o.get_move_message())
                    player.warp_to(d_o.get_connection().get_loc())
                    player.get_loc().describe()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} closed.')
        else:
            pront(f'{d_o.art_d().capitalize()} cannot be entered.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'portal' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority += 2
        return (d_o, priority)
go_through = Go_through('go|through', ['go through', 'walk through', 'pass through', 'move through'])
go_through.set_required_states(['standing'])

class Climb_up(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Ladder) and d_o.leads_up():
            if not player.check_taut_ropes(d_o.get_up_destination()):
                pront(d_o.get_move_up_message())
                player.warp_to(d_o.get_up_destination())
                player.get_loc().describe()
                inc_turn()
        else:
            pront(f'You cannot climb up {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Ladder) and d_o.leads_up():
            priority += 5
        return (d_o, priority)
climb_up = Climb_up('climb|up', ['climb up', 'go up', 'walk up', 'travel up'])
climb_up.set_required_states(['standing'])

class Climb_down(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Ladder) and d_o.leads_down():
            if not player.check_taut_ropes(d_o.get_down_destination()):
                pront(d_o.get_move_down_message())
                player.warp_to(d_o.get_down_destination())
                player.get_loc().describe()
                inc_turn()
        else:
            pront(f'You cannot climb down {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Ladder) and d_o.leads_down():
            priority += 5
        return (d_o, priority)
climb_down = Climb_down('climb|down', ['climb down', 'go down', 'walk down', 'travel down'])
climb_down.set_required_states(['standing'])

class Climb(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Ladder) and d_o.leads_up():
            if not player.check_taut_ropes(d_o.get_up_destination()):
                pront(d_o.get_move_up_message())
                player.warp_to(d_o.get_up_destination())
                player.get_loc().describe()
                inc_turn()
        elif isinstance(d_o, Ladder) and d_o.leads_down():
            if not player.check_taut_ropes(d_o.get_down_destination()):
                pront(d_o.get_move_down_message())
                player.warp_to(d_o.get_down_destination())
                player.get_loc().describe()
                inc_turn()
        else:
            pront(f'You cannot climb {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Ladder) and (d_o.leads_up() or d_o.leads_down()):
            priority += 5
        return (d_o, priority)
climb = Climb('climb', ['climb'])
climb.set_required_states(['standing'])

class Open(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Container) and 'openable' in d_o.get_properties():
            if d_o.is_open():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
            else:
                if isinstance(d_o, Ampuole):
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} sealed.')
                elif d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} locked.')
                else:
                    if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                        pront(f'You open {d_o.art_d()}. In doing so, you reveal:')
                        d_o.make_open()
                        d_o.list_contents()
                    else:
                        pront(f'You open {d_o.art_d()}.')
                        d_o.make_open()
                    inc_turn()
        elif isinstance(d_o, Door) and 'openable' in d_o.get_properties():
            if d_o.is_open():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
            else:
                if d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} locked.')
                else:
                    d_o.make_open()
                    pront(f'You open {d_o.art_d()}.')
                    inc_turn()
        elif isinstance(d_o, Door):
            pront(f'You cannot open {d_o.art_d()}.')
        else:
            pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be opened.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'openable' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority -= 5
        if isinstance(d_o, Container) and 'openable' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority -= 5
        return (d_o, priority)
open = Open('open', ['open'])

class Close(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Container) and 'openable' in d_o.get_properties():
            if d_o.is_open():
                d_o.make_closed()
                pront(f'You close {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already closed.')
        elif isinstance(d_o, Door) and 'openable' in d_o.get_properties():
            if d_o.is_open():
                d_o.make_closed()
                pront(f'You close {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already closed.')
        else:
            pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be closed.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'openable' in d_o.get_properties():
            priority += 5
            if not d_o.is_open():
                priority -= 5
        if isinstance(d_o, Container) and 'openable' in d_o.get_properties():
            priority += 5
            if not d_o.is_open():
                priority -= 5
        return (d_o, priority)
close = Close('close', ['close', 'shut'])

class Lock(Verb1):
    def body(self, d_o):
        if isinstance(d_o, LockedDoor) and not isinstance(d_o, KeyedDoor):
            if d_o.is_locked():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already locked.')
            elif d_o.is_open():
                pront(f'{d_o.art_d().capitalize()} cannot be locked while {d_o.pluralize("it is")} open.')
            else:
                pront(f'You lock {d_o.art_d()}.')
                d_o.lock()
                if d_o.get_locklink():
                    d_o.get_connection().lock()
                inc_turn()
        else:
            if isinstance(d_o, KeyedDoor) or (isinstance(d_o, Locker) and not isinstance(d_o, Ampuole)):
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that you can lock by hand.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that you can lock.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, LockedDoor) and not isinstance(d_o, KeyedDoor):
            priority += 5
            if d_o.is_open() or d_o.is_locked():
                priority -= 5
        if isinstance(d_o, KeyedDoor) or (isinstance(d_o, Locker) and not isinstance(d_o, Ampuole)):
            priority +=1
            if d_o.is_open() or d_o.is_locked():
                priority -= 1
        return (d_o, priority)
lock = Lock('lock', ['lock'])

class Unlock(Verb1):
    def body(self, d_o):
        if isinstance(d_o, LockedDoor) and not isinstance(d_o, KeyedDoor):
            if not d_o.is_locked():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already unlocked.')
            else:
                pront(f'You unlock {d_o.art_d()}.')
                d_o.unlock()
                if d_o.get_locklink():
                    d_o.get_connection().unlock()
                inc_turn()
        else:
            if isinstance(d_o, KeyedDoor) or (isinstance(d_o, Locker) and not isinstance(d_o, Ampuole)):
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that you can unlock by hand.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that you can unlock.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, LockedDoor) and not isinstance(d_o, KeyedDoor):
            priority += 5
            if not d_o.is_locked():
                priority -= 5
        if isinstance(d_o, KeyedDoor) or (isinstance(d_o, Locker) and not isinstance(d_o, Ampuole)):
            priority +=1
            if not d_o.is_locked():
                priority -= 1
        return (d_o, priority)
unlock = Unlock('unlock', ['unlock'])

class Shake(Verb1):
    def body(self, d_o):
        if d_o.get_loc() == player:
            if isinstance(d_o, Container) and not isinstance(d_o, Surface):
                if len(d_o.get_contents()) > 1:
                    pront(f'You hear some objects moving around inside {d_o.art_d()}.')
                elif len(d_o.get_contents()) == 1:
                    pront(f'You hear an object moving around inside {d_o.art_d()}.')
                else:
                    pront(f'Shaking {d_o.art_d()} does nothing.')
            elif isinstance(d_o, Surface) and len(d_o.get_contents()) > 0:
                name = []
                temp = []
                for x in d_o.get_contents():
                    temp.append(x)
                for y in temp:
                    name.append(y.art_d())
                    y.warp_to(player.get_loc())
                pront(f'You shake {d_o.art_d()}, causing ' + sequence(name, 'and') + ' to fall to the ground.')
            else:
                pront(f'Shaking {d_o.art_d()} does nothing.')
            inc_turn()
        else:
            pront(f'You are not holding {d_o.art_d()}.')
shake = Shake('shake', ['shake', 'wave', 'agitate', 'rattle'])

class Push(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Lever) or isinstance(d_o, Button):
            d_o.activate()
        else:
            pront(f'You cannot push {d_o.art_d()}.')
push = Push('push', ['press', 'push'])

class Pull(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Lever):
            d_o.activate()
        else:
            pront(f'You cannot pull {d_o.art_d()}.')
pull = Pull('pull', ['pull', 'yank'])

class Eat(Verb1):
    def body(self, d_o):
        if 'edible' in d_o.get_properties():
            pront(f'You eat {d_o.art_d()}. {d_o.pluralize("It is")} tasty.')
            d_o.warp_to(offstage)
            inc_turn()
        else:
            pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} inedible.')

    def prioritize(self, d_o):
        priority = 0
        if 'edible' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
eat = Eat('eat', ['eat', 'bite', 'consume', 'ingest'])

class Read(Verb1):
    def body(self, d_o):
        if 'readable' in d_o.get_properties():
            if player.get_loc().is_illuminated() or d_o.get_brightness() == 1:
                pront(d_o.get_read_description())
                inc_turn()
            else:
                pront('It is too dark to read here.')
        else:
            pront(f'You cannot read {d_o.art_d()}.')
read = Read('read', ['read'])

class Turn_on(Verb1):
    def body(self, d_o):
        if 'lamp' in d_o.get_properties():
            if d_o.get_brightness() == 2:
                pront(f'{d_o.art_d().capitalize()} is already on.')
            else:
                d_o.set_brightness(2)
                pront(f'You turn on {d_o.art_d()}.')
                inc_turn()
        else:
            pront(f'You cannot turn on {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if 'lamp' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
turn_on = Turn_on('turn|on', ['turn on', 'activate', 'light'])

class Turn_off(Verb1):
    def body(self, d_o):
        if 'lamp' in d_o.get_properties():
            if d_o.get_brightness() == 2:
                d_o.set_brightness(0)
                pront(f'You turn off {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} is already off.')
        else:
            pront(f'You cannot turn on {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if 'lamp' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
turn_off = Turn_off('turn|off', ['turn off', 'deactivate', 'inactivate', 'unlight'])

class Untie(Verb1):
    def body(self, d_o):
        if isinstance(d_o, RopeTrail):
            d_o = d_o.get_parent_rope()
        if isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 0:
            if len(d_o.get_tied_objects()) > 1:
                if d_o.get_tied_objects()[0].is_visible() and d_o.get_tied_objects()[1].is_visible():
                    pront(f'You should specify whether you want to untie {d_o.art_d()} from {d_o.get_tied_objects()[0].art_d()} or from {d_o.get_tied_objects()[1].art_d()}.')
                elif d_o.get_tied_objects()[0].is_visible() or d_o.get_tied_objects()[1].is_visible():
                    if d_o.get_tied_objects()[0].is_visible():
                        t = d_o.get_tied_objects()[0]
                    else:
                        t = d_o.get_tied_objects()[1]
                    t.get_child_attachments().remove(d_o)
                    d_o.remove_tied_object(t)
                    if 'plug' in d_o.get_properties():
                        pront(f'You unplug {d_o.art_d()} from {t.art_d()}.')
                    else:
                        pront(f'You untie {d_o.art_d()} from {t.art_d()}.')
                    d_o.update_locations()
                    inc_turn()
                else:
                    pront(f'You cannot see {d_o.get_tied_objects()[0].art_d()} or {d_o.get_tied_objects()[1].art_d()}.')
            else:
                t = d_o.get_tied_objects()[0]
                t.get_child_attachments().remove(d_o)
                d_o.remove_tied_object(t)
                if len(d_o.get_room_order()) > 1:
                    if 'plug' in d_o.get_properties():
                        pront(f'You unplug {d_o.art_d()} from {t.art_d()} and gather it up.')
                    else:
                        pront(f'You untie {d_o.art_d()} from {t.art_d()} and gather it up.')
                    if d_o.find_ultimate_room() is not player.get_loc():
                        d_o.warp_to(player.get_loc())
                else:
                    if 'plug' in d_o.get_properties():
                        pront(f'You unplug {d_o.art_d()} from {t.art_d()}.')
                    else:
                        pront(f'You untie {d_o.art_d()} from {t.art_d()}.')
                d_o.update_locations()
                inc_turn()
        else:
            for x in d_o.get_child_attachments():
                if isinstance(x, Rope):
                    self.body(x)
                    break
            else:
                pront(f'{d_o.art_d().capitalize()} is not tied to anything.')

        def prioritize(self, d_o):
            priority = 0
            if isinstance(d_o, rope) and len(d_o.get_tied_objects()) > 0:
                priority += 5
            return (d_o, priority)
untie = Untie('untie', ['untie', 'unbind', 'untether'])

class Unplug(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Rope) or isinstance(d_o, RopeTrail):
            untie.body(d_o)
        else:
            if hasattr(d_o, 'parent_attachment') and 'plug' in d_o.get_properties():
                t = d_o.get_parent_attachment()
                d_o.detach()
                pront(f'You unplug {d_o.art_d()} from {t.art_d()}.')
                inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not plugged into anything.')

    def prioritize(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment') or (isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 0):
            priority += 3
        if 'plug' in d_o.get_properties():
            priority += 3
        return (d_o, priority)
unplug = Unplug('unplug', ['unplug'])

class Detach(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Rope) or isinstance(d_o, RopeTrail):
            untie.body(d_o)
        elif hasattr(d_o, 'parent_attachment'):
            if 'plug' in d_o.get_properties():
                unplug.body(d_o)
            else:
                t = d_o.get_parent_attachment()
                d_o.detach()
                pront(f'You detach {d_o.art_d()} from {t.art_d()}.')
                inc_turn()
        else:
            pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not attached to anything.')

    def prioritize(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment'):
            priority += 3
        return (d_o, priority)
detach = Detach('detach', ['detach', 'disconnect', 'unfasten'])

class Stand_On(Verb1):
    def body(self, d_o):
        if 'ground' in d_o.get_properties():
            if hasattr(player, 'state_position') and player.get_state() == 'standing':
                pront(f'You step off {player.get_state_position().art_d()}.')
                player.reset_state()
                inc_turn()
            else:
                stand.body()
        elif (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            if player.get_state() == 'standing atop something':
                pront(f'You are already standing on {d_o.art_d()}.')
            else:
                if 'standing atop something' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to standing on {d_o.art_d()}.')
                    player.set_state('standing atop something')
                    inc_turn()
                else:
                    pront(f'You cannot stand on {d_o.art_d()}.')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if 'standing atop something' in d_o.get_allowed_states():
                pront(f'You stand on {d_o.art_d()}.')
                player.set_state('standing atop something')
                player.set_state_position(d_o)
                inc_turn()
            elif 'standing' in d_o.get_allowed_states():
                    pront(f'You stand on {d_o.art_d()}.')
                    player.set_state('standing')
                    player.set_state_position(d_o)
                    inc_turn()
            else:
                pront(f'You cannot stand on {d_o.art_d()}.')
stand_on = Stand_On('stand|on', ['stand on', 'stand on top of', 'stand atop', 'stand up on', 'stand up on top of', 'stand up atop'])

class Sit_On(Verb1):
    def body(self, d_o):
        if 'ground' in d_o.get_properties():
            player.reset_state()
            sit.body()
        elif (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            if player.get_state() == 'sitting':
                pront(f'You are already sitting on {d_o.art_d()}.')
            else:
                if 'sitting' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to sitting on {d_o.art_d()}.')
                    player.set_state('sitting')
                    inc_turn()
                else:
                    pront(f'You cannot sit on {d_o.art_d()}.')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if 'sitting' in d_o.get_allowed_states():
                pront(f'You sit on {d_o.art_d()}.')
                player.set_state('sitting')
                player.set_state_position(d_o)
                inc_turn()
            else:
                pront(f'You cannot sit on {d_o.art_d()}.')
sit_on = Sit_On('sit|on', ['sit on', 'sit up on', 'sit down on', 'sit atop', 'sit on top of', 'sit down on top of', 'sit down atop', 'sit in', 'sit down in'])

class Lie_On(Verb1):
    def body(self, d_o):
        if 'ground' in d_o.get_properties():
            player.reset_state()
            lie.body()
        elif (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            if player.get_state() == 'lying down':
                pront(f'You are already lying down on {d_o.art_d()}.')
            else:
                if 'lying down' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to lying down on {d_o.art_d()}.')
                    player.set_state('lying down')
                    inc_turn()
                else:
                    pront(f'You cannot lie down on {d_o.art_d()}.')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if 'lying down' in d_o.get_allowed_states():
                pront(f'You lie down on {d_o.art_d()}.')
                player.set_state('lying down')
                player.set_state_position(d_o)
                inc_turn()
            else:
                pront(f'You cannot lie down on {d_o.art_d()}.')
lie_on = Lie_On('lie|on', ['lie on', 'lie down on', 'lie on top of', 'lie atop', 'lie down on top of', 'lie down atop'])

class Ride(Verb1):
    def body(self, d_o):
        if (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            if player.get_state() == 'riding a vehicle':
                pront(f'You are already riding {d_o.art_d()}.')
            else:
                if 'riding a vehicle' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to riding {d_o.art_d()}.')
                    player.set_state('riding a vehicle')
                    inc_turn()
                else:
                    pront(f'You cannot ride {d_o.art_d()}.')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if 'riding a vehicle' in d_o.get_allowed_states():
                pront(f'You ride {d_o.art_d()}.')
                player.set_state('riding a vehicle')
                player.set_state_position(d_o)
                inc_turn()
            else:
                pront(f'You cannot ride {d_o.art_d()}.')
ride = Ride('ride', ['ride', 'ride on', 'ride atop', 'board', 'mount'])

class Get_On(Verb1):
    def body(self, d_o):
        if (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            pront(f'You are already on {d_o.art_d()}')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if len(d_o.get_allowed_states()) > 0:
                u = d_o.get_default_state()
                player.set_state(u)
                player.set_state_position(d_o)
                if u == 'standing atop something' or u == 'standing':
                    pront(f'You stand on {d_o.art_d()}.')
                elif u == 'sitting':
                    pront(f'You sit on {d_o.art_d()}.')
                elif u == 'lying down':
                    pront(f'You lie down on {d_o.art_d()}.')
                elif u == 'riding a vehicle':
                    pront(f'You ride {d_o.art_d()}.')
                else:
                    pront(f'You get on {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'You cannot get on {d_o.art_d()}.')
get_on = Get_On('get|on', ['get on', 'get onto', 'get into'])

class Greet(Verb1):
    def body(self, d_o):
        if isinstance(d_o, NPC) and d_o.owngreetingPulser.get_activity():
            d_o.greet_player()
            d_o.owngreetingPulser.reactivate(); d_o.ownwanderPulser.reactivate()
        else:
            pront(f'{d_o.art_d().capitalize()} does not respond.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, NPC):
            priority += 5
        return (d_o, priority)
greet = Greet('greet', ['greet', 'say hello to', 'say hi to'])
greet.set_requires_contact(False)

class Talk_to(Verb1):
    def body(self, d_o):
        if isinstance(d_o, NPC):
            pront(f'You can try asking {obliquefy(d_o.get_pronoun())} about something, or telling {obliquefy(d_o.get_pronoun())} about something.')
        else:
            pront(f'{d_o.art_d().capitalize()} is an inanimate object and will not respond.')
talk_to = Talk_to('talk|to', ['talk to', 'talk with', 'speak to', 'speak with', 'converse with'])
talk_to.set_requires_contact(False)

class Put(Verb2):
    def body(self, d_o, i_o):
        if d_o.get_loc() == player:
            if 'ground' in i_o.get_properties():
                drop.body(d_o)
            elif isinstance(i_o, Container) and not isinstance(i_o, Player) and not isinstance(i_o, NPC):
                if hasattr(i_o, 'whitelist') and d_o not in i_o.whitelist:
                    pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} not designed to accomodate {d_o.art_d()}.')
                elif hasattr(i_o, 'blacklist') and d_o in i_o.blacklist:
                    pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} not designed to accomodate {d_o.art_d()}.')
                elif 'player_anatomy' in d_o.get_properties():
                    pront(f'You are unwilling to attempt separating {d_o.art_d()} from your own body.')
                elif 'component' in d_o.get_properties():
                    if d_o.is_plural():
                        pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                    else:
                        pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
                elif hasattr(d_o, 'parent_attachment'):
                    if d_o.is_plural():
                        pront(f'You cannot put {d_o.art_d()} anywhere while they are attached to {d_o.get_parent_attachment().art_d()}.')
                    else:
                        pront(f'You cannot put {d_o.art_d()} anywhere while it is attached to {d_o.get_parent_attachment().art_d()}.')
                elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 1:
                    if 'plug' in d_o.get_properties():
                        pront(f'You cannot put {d_o.art_d()} anywhere while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged in at both ends.')
                    else:
                        pront(f'You cannot put {d_o.art_d()} anywhere while {d_o.get_pronoun()} {d_o.pluralize("is")} tied at both ends.')
                elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) == 1 and d_o.get_tied_objects()[0].is_within(player):
                    if 'plug' in d_o.get_properties():
                        pront(f'You cannot put {d_o.art_d()} anywhere while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged into {d_o.get_tied_objects()[0].art_d()}.')
                    else:
                        pront(f'You cannot put {d_o.art_d()} anywhere while {d_o.get_pronoun()} {d_o.pluralize("is")} tied to {d_o.get_tied_objects()[0].art_d()}.')
                else:
                    if d_o is i_o:
                        pront('You cannot put something inside itself.')
                    elif i_o.is_within(d_o):
                        pront('Topology forbids such actions.')
                    elif not i_o.is_open():
                        pront('You cannot put something inside a closed container.')
                    elif d_o.get_bulk() > i_o.get_capacity():
                        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} too big to fit in the {i_o.art_d()}.')
                    elif d_o.get_bulk() + i_o.get_content_bulk() > i_o.get_capacity():
                        pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} too full to accomodate {d_o.art_d()}.')
                    else:
                        d_o.warp_to(i_o)
                        if isinstance(i_o, Surface):
                            pront(f'You put {d_o.art_d()} on {i_o.art_d()}.')
                        else:
                            pront(f'You put {d_o.art_d()} inside {i_o.art_d()}.')
                        inc_turn()
            else:
                pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} not a container.')
        else:
            pront(f'You are not holding {d_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if d_o.get_loc() == player:
            priority += 2
        if 'component' in d_o.get_properties():
            priority -= 5
        if 'player_anatomy' in d_o.get_properties():
            priority -= 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(i_o, Container) and not isinstance(i_o, Player) and not isinstance(i_o, NPC):
            priority += 5
            if not i_o.is_open():
                priority -= 4
        return (i_o, priority)
put = Put('put_in', ['put', 'place'], ('in', 'into', 'on', 'inside'))

class Give(Verb2):
    def body(self, d_o, i_o):
        if d_o.get_loc() == player:
            if isinstance(i_o, NPC):
                if 'player_anatomy' in d_o.get_properties():
                    pront(f'You are unwilling to attempt separating {d_o.art_d()} from your own body.')
                elif 'component' in d_o.get_properties():
                    if d_o.is_plural():
                        pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                    else:
                        pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
                else:
                    if d_o is i_o:
                        pront('You cannot put something inside itself.')
                    elif i_o.is_within(d_o):
                        pront('Topology forbids such actions.')
                    elif d_o.get_bulk() > i_o.get_capacity():
                        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} too big for {i_o.art_d()} to carry.')
                    elif d_o.get_bulk() + i_o.get_content_bulk() > i_o.get_capacity():
                        pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} carrying too much to hold {d_o.art_d()}.')
                    else:
                        if d_o in i_o.get_covets():
                            d_o.warp_to(i_o)
                            pront(f'You give {d_o.art_d()} to {i_o.art_d()}.')
                        elif d_o in i_o.get_show_responses() or d_o in i_o.get_show_event_triggers():
                            pront(f'{i_o.art_d().capitalize()} looks at {d_o.art_d()}, but does not take it.')
                            show.body(d_o, i_o)
                        else:
                            pront(f'{i_o.art_d().capitalize()} says "I don\'t want {d_o.art_d()}."')
                        inc_turn()
            else:
                pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} not a person.')
        else:
            pront(f'You are not holding {d_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if d_o.get_loc() == player:
            priority += 2
        if 'component' in d_o.get_properties():
            priority -= 5
        if 'player_anatomy' in d_o.get_properties():
            priority -= 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(i_o, NPC):
            priority += 5
        return (i_o, priority)
give = Give('give_to', ['give', 'hand', 'donate', 'relinquish', 'offer'], ('to',))

class Open2(Verb2):
    def body(self, d_o, i_o):
        if i_o.get_loc() == player:
            if isinstance(d_o, Locker) and 'openable' in d_o.get_properties():
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if i_o in d_o.get_keylist():
                        if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                            pront(f'You open {d_o.art_d()} with {i_o.art_d()}. In doing so, you reveal:')
                            d_o.unlock()
                            d_o.make_open()
                            d_o.list_contents()
                        else:
                            pront(f'You open {d_o.art_d()} with {i_o.art_d()}.')
                            d_o.unlock()
                            d_o.make_open()
                        inc_turn()
                    elif i_o == hands and not d_o.is_locked():
                        if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                            pront(f'You open {d_o.art_d()}. In doing so, you reveal:')
                            d_o.make_open()
                            d_o.list_contents()
                        else:
                            pront(f'You open {d_o.art_d()}.')
                            d_o.make_open()
                        inc_turn()
                    else:
                        pront(f'You cannot open {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, Container) and ('openable' in d_o.get_properties()) and (i_o == hands):
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                        pront(f'You open {d_o.art_d()}. In doing so, you reveal:')
                        d_o.make_open()
                        d_o.list_contents()
                    else:
                        pront(f'You open {d_o.art_d()}.')
                        d_o.make_open()
                    inc_turn()
            elif isinstance(d_o, Container) and ('openable' in d_o.get_properties()):
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                        pront(f'After a brief period of contemplation, you realize that {i_o.art_d()} {i_o.pluralize("is")} unnecessary. Instead, you open {d_o.art_d()} with your hands. In doing so, you reveal:')
                        d_o.make_open()
                        d_o.list_contents()
                    else:
                        pront(f'After a brief period of contemplation, you realize that {i_o.art_d()} {i_o.pluralize("is")} unnecessary. Instead, you open {d_o.art_d()} with your hands.')
                        d_o.make_open()
                    inc_turn()
            elif isinstance(d_o, KeyedDoor):
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You open {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.unlock()
                        if d_o.get_locklink():
                            d_o.get_connection().unlock()
                        d_o.make_open()
                        inc_turn()
                    else:
                        pront(f'You cannot open {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, LockedDoor):
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if i_o == hands:
                        pront(f'You open {d_o.art_d()}.')
                    else:
                        pront(f'You briefly consider attempting to open {d_o.art_d()} with {i_o.art_d()}, but since the locking mechanism is designed to be operated by hand, you settle for doing that instead.')
                    d_o.unlock()
                    if d_o.get_locklink():
                        d_o.get_connection().unlock()
                    d_o.make_open()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be opened.')
        else:
            pront(f'You do not have {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, Door) or isinstance(d_o, Container):
            priority += 3
            if d_o.is_open():
                priority -= 5
            if 'openable' in d_o.get_properties():
                priority += 2
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if i_o.get_loc() == player:
            priority += 1
        return (i_o, priority)
open2 = Open2('open_with', ['open'], ('with', 'using'))

class Unlock2(Verb2):
    def body(self, d_o, i_o):
        if i_o.get_loc() == player:
            if isinstance(d_o, Locker) and not isinstance(d_o, Ampuole):
                if not d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already unlocked.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You unlock {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.unlock()
                        inc_turn()
                    else:
                        pront(f'You cannot unlock {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, KeyedDoor):
                if not d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already unlocked.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You unlock {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.unlock()
                        if d_o.get_locklink():
                            d_o.get_connection().unlock()
                        inc_turn()
                    else:
                        pront(f'You cannot unlock {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, LockedDoor):
                if not d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already unlocked.')
                else:
                    if i_o == hands:
                        pront(f'You unlock {d_o.art_d()}.')
                    else:
                        pront(f'You briefly consider attempting to unlock {d_o.art_d()} with {i_o.art_d()}, but since the locking mechanism is designed to be operated by hand, you settle for doing that instead.')
                    d_o.unlock()
                    if d_o.get_locklink():
                        d_o.get_connection().unlock()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be unlocked.')
        else:
            pront(f'You do not have {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, Door) or isinstance(d_o, Container):
            priority += 3
            if d_o.is_locked():
                priority -= 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if i_o.get_loc() == player:
            priority += 1
        return (i_o, priority)
unlock2 = Unlock2('unlock_with', ['unlock'], ('with', 'using'))

class Lock2(Verb2):
    def body(self, d_o, i_o):
        if i_o.get_loc() == player:
            if isinstance(d_o, Locker) and not isinstance(d_o, Ampuole):
                if d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already locked.')
                elif d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} cannot be locked while {d_o.pluralize("it is")} open.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You lock {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.lock()
                        inc_turn()
                    else:
                        pront(f'You cannot lock {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, KeyedDoor):
                if d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already locked.')
                elif d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} cannot be locked while {d_o.pluralize("it is")} open.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You lock {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.lock()
                        if d_o.get_locklink():
                            d_o.get_connection().lock()
                        inc_turn()
                    else:
                        pront(f'You cannot lock {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, LockedDoor):
                if d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already locked.')
                elif d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} cannot be locked while {d_o.pluralize("it is")} open.')
                else:
                    if i_o == hands:
                        pront(f'You lock {d_o.art_d()}.')
                    else:
                        pront(f'You briefly consider attempting to lock {d_o.art_d()} with {i_o.art_d()}, but since the locking mechanism is designed to be operated by hand, you settle for doing that instead.')
                    d_o.lock()
                    if d_o.get_locklink():
                        d_o.get_connection().lock()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be locked.')
        else:
            pront(f'You do not have {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, Door) or isinstance(d_o, Container):
            priority += 3
            if not d_o.is_locked():
                priority -= 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if i_o.get_loc() == player:
            priority += 1
        return (i_o, priority)
lock2 = Lock2('lock_with', ['lock'], ('with', 'using'))

class Tie(Verb2):
    def body(self, d_o, i_o):
        if d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments():
            self.body(i_o, d_o)
        else:
            if d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments() and isinstance(d_o, Rope):
                l = d_o.get_tied_objects()
                if len(d_o.get_tied_objects()) > 2:
                    if 'plug' in d_o.get_properties():
                        pront(f'{d_o.art_d().capitalize()} is already plugged into {l[0].art_d()} and {l[1].art_d()}.')
                    else:
                        pront(f'{d_o.art_d().capitalize()} is already tied to {l[0].art_d()} and {l[1].art_d()}.')
                elif i_o.get_attachment_limiting_status() and len(i_o.get_child_attachments()) >= i_o.get_attachment_limit():
                    templist = []
                    for x in i_o.get_child_attachments():
                        templist.append(x.art_d())
                    if 'plug' in d_o.get_properties():
                        pront(f'You should unplug {sequence(templist, "or")} first.')
                    else:
                        pront(f'You should untie {sequence(templist, "or")} first.')
                else:
                    d_o.tie_to(i_o)
                    if 'plug' in d_o.get_properties():
                        pront(f'You plug {d_o.art_d()} into {i_o.art_d()}.')
                    else:
                        pront(f'You tie {d_o.art_d()} to {i_o.art_d()}.')
                    inc_turn()
            else:
                if 'plug' in d_o.get_properties() and isinstance(d_o, Rope):
                    pront(f'You cannot plug {d_o.art_d()} into {i_o.art_d()}.')
                else:
                    pront(f'You cannot tie {d_o.art_d()} to {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, Rope):
            priority += 2
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if (d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments()) or (d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments()):
            priority += 5
        return (i_o, priority)
tie = Tie('tie_to', ['tie', 'bind', 'tether'], ('to', 'onto'))

class Plug(Verb2):
    def body(self, d_o, i_o):
        if d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments():
            self.body(i_o, d_o)
        else:
            if d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments() and 'plug' in d_o.get_properties():
                if isinstance(d_o, Rope):
                    tie.body(d_o, i_o)
                else:
                    if d_o in i_o.get_child_attachments():
                        pront(f'{d_o.art_d().capitalize()} is already plugged into {i_o.art_d()}.')
                    elif i_o.get_attachment_limiting_status() and len(i_o.get_child_attachments()) >= i_o.get_attachment_limit():
                        templist = []
                        for x in i_o.get_child_attachments():
                            templist.append(x.art_d())
                        pront(f'You should unplug {sequence(templist, "or")} first.')
                    else:
                        if hasattr(d_o, 'parent_attachment'):
                            pront(f'You unplug {d_o.art_d()} from {d_o.get_parent_attachment().art_d()} and plug {obliquefy(d_o.get_pronoun())} into {i_o.art_d()}.')
                        else:
                            pront(f'You plug {d_o.art_d()} into {i_o.art_d()}.')
                        d_o.attach_to(i_o)
                        inc_turn()
            else:
                pront(f'You cannot plug {d_o.art_d()} into {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if 'plug' in d_o.get_properties():
            priority += 2
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if (d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments()) or (d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments()):
            priority += 5
        return (i_o, priority)
plug = Plug('plug_into', ['plug'], ('into',))

class Attach(Verb2):
    def body(self, d_o, i_o):
        if d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments():
            self.body(i_o, d_o)
        else:
            if d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments():
                if 'plug' in d_o.get_properties():
                    plug.body(d_o, i_o)
                elif isinstance(d_o, Rope):
                    tie.body(d_o, i_o)
                else:
                    if d_o in i_o.get_child_attachments():
                        pront(f'{d_o.art_d().capitalize()} is already attached to {i_o.art_d()}.')
                    elif i_o.get_attachment_limiting_status() and len(i_o.get_child_attachments()) >= i_o.get_attachment_limit():
                        templist = []
                        for x in i_o.get_child_attachments():
                            templist.append(x.art_d())
                        pront(f'You should detach {sequence(templist, "or")} first.')
                    else:
                        if hasattr(d_o, 'parent_attachment'):
                            pront(f'You detach {d_o.art_d()} from {d_o.get_parent_attachment().art_d()} and attach {obliquefy(d_o.get_pronoun())} to {i_o.art_d()}.')
                        else:
                            pront(f'You attach {d_o.art_d()} to {i_o.art_d()}.')
                        d_o.attach_to(i_o)
                        inc_turn()
            else:
                pront(f'You cannot attach {d_o.art_d()} to {i_o.art_d()}.')

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if (d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments()) or (d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments()):
            priority += 5
        return (i_o, priority)
attach = Attach('attach_to', ['attach', 'connect', 'fasten'], ('to',))

class Untie2(Verb2):
    def body(self, d_o, i_o):
        if isinstance(d_o, RopeTrail):
            d_o = d_o.get_parent_rope()
        if isinstance(i_o, RopeTrail):
            i_o = i_o.get_parent_rope()
        if isinstance(i_o, Rope) and i_o in d_o.get_child_attachments():
            self.body(i_o, d_o)
        else:
            if isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 0:
                if d_o in i_o.get_child_attachments():
                    i_o.get_child_attachments().remove(d_o)
                    d_o.remove_tied_object(i_o)
                    if len(d_o.get_room_order()) > 1 and len(d_o.get_tied_objects()) == 0:
                        if 'plug' in d_o.get_properties():
                            pront(f'You unplug {d_o.art_d()} from {i_o.art_d()} and gather it up.')
                        else:
                            pront(f'You untie {d_o.art_d()} from {i_o.art_d()} and gather it up.')
                        if d_o.find_ultimate_room() is not player.get_loc():
                            d_o.warp_to(player.get_loc())
                    else:
                        if 'plug' in d_o.get_properties():
                            pront(f'You unplug {d_o.art_d()} from {i_o.art_d()}.')
                        else:
                            pront(f'You untie {d_o.art_d()} from {i_o.art_d()}.')
                    d_o.update_locations()
                    inc_turn()
                else:
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not tied to {i_o.art_d()}.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not tied to anything.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment'):
            priority += 3
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if d_o in i_o.get_child_attachments():
            priority += 5
        return (i_o, priority)
untie2 = Untie2('untie_from', ['untie', 'unbind', 'untether'], ('from',))

class Unplug2(Verb2):
    def body(self, d_o, i_o):
        if hasattr(i_o, 'parent_attachment') and i_o.get_parent_attachment() == d_o and 'plug' in i_o.get_properties():
            self.body(i_o, d_o)
        else:
            if isinstance(d_o, Rope) or isinstance(d_o, RopeTrail):
                untie2.body(d_o, i_o)
            elif hasattr(d_o, 'parent_attachment') and 'plug' in d_o.get_properties():
                if d_o in i_o.get_child_attachments():
                    d_o.detach()
                    pront(f'You unplug {d_o.art_d()} from {i_o.art_d()}.')
                    inc_turn()
                else:
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not plugged into {i_o.art_d()}.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not plugged into anything.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment'):
            priority += 3
        if 'plug' in d_o.get_properties():
            priority += 3
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if d_o in i_o.get_child_attachments():
            priority += 5
        return (i_o, priority)
unplug2 = Unplug2('unplug_from', ['unplug'], ('from',))

class Detach2(Verb2):
    def body(self, d_o, i_o):
        if hasattr(i_o, 'parent_attachment') and i_o.get_parent_attachment() == d_o:
            self.body(i_o, d_o)
        else:
            if isinstance(d_o, Rope) or isinstance(d_o, RopeTrail):
                untie2.body(d_o, i_o)
            elif hasattr(d_o, 'parent_attachment'):
                if 'plug' in d_o.get_properties():
                    unplug2.body(d_o, i_o)
                else:
                    if d_o in i_o.get_child_attachments():
                        d_o.detach()
                        pront(f'You detach {d_o.art_d()} from {i_o.art_d()}.')
                        inc_turn()
                    else:
                        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not attached to {i_o.art_d()}.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not attached to anything.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment'):
            priority += 3
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if d_o in i_o.get_child_attachments():
            priority += 5
        return (i_o, priority)
detach2 = Detach2('detach_from', ['detach', 'disconnect', 'unfasten', 'remove'], ('from',))

class Ask(Verb2):
    def body(self, d_o, i_o):
        if isinstance(d_o, NPC):
            if i_o.is_known():
                if i_o in d_o.get_ask_responses():
                    q = d_o.get_ask_responses()[i_o]
                    r = q[0]
                    if q[1]:
                        r = '"' + r + '"'
                    pront(r)
                    for x in q[2]:
                        x.make_known()
                elif i_o in d_o.get_ask_event_triggers():
                    d_o.do_ask_event(i_o)
                else:
                    pront(f'"{d_o.get_unknown_ask_msg()}"')
            else:
                pront(f'You have not seen any {i_o.get_name()}.')
            if d_o.owngreetingPulser.get_activity():
                d_o.owngreetingPulser.reactivate()
            if d_o.ownwanderPulser.get_activity():
                d_o.ownwanderPulser.reactivate()
        else:
            pront(f'{d_o.art_d().capitalize()} is an inanimate object and does not respond.')
        inc_turn()

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, NPC):
            priority += 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(d_o, NPC):
            if i_o.is_known():
                priority += 4
            else:
                priority -=8
            if i_o in d_o.get_ask_responses() or i_o in d_o.get_ask_event_triggers():
                priority += 3
            else:
                priority -= 6
        else:
            priority -= 1
        return (i_o, priority)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        if len(new) > 1 and num <= 0:
            return [new[0]]
        return new
ask = Ask('ask_about', ['ask', 'interrogate', 'query'], ('about',))
ask.set_d_o_requires_contact(False)
ask.set_i_o_requires_contact(False)
ask.set_i_o_requires_sight(False)

class Tell(Verb2):
    def body(self, d_o, i_o):
        if isinstance(d_o, NPC):
            if i_o.is_known():
                if i_o in d_o.get_tell_responses():
                    q = d_o.get_tell_responses()[i_o]
                    r = q[0]
                    if q[1]:
                        r = '"' + r + '"'
                    pront(r)
                    for x in q[2]:
                        x.make_known()
                elif i_o in d_o.get_tell_event_triggers():
                    d_o.do_tell_event(i_o)
                else:
                    pront(f'"{d_o.get_unknown_tell_msg()}"')
            else:
                pront(f'You have not seen any {i_o.get_name()}.')
            if d_o.owngreetingPulser.get_activity():
                d_o.owngreetingPulser.reactivate()
            if d_o.ownwanderPulser.get_activity():
                d_o.ownwanderPulser.reactivate()
        else:
            pront(f'{d_o.art_d().capitalize()} is an inanimate object and does not respond.')
        inc_turn()

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, NPC):
            priority += 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(d_o, NPC):
            if i_o.is_known():
                priority += 4
            else:
                priority -=8
            if i_o in d_o.get_tell_responses() or i_o in d_o.get_tell_event_triggers():
                priority += 3
            else:
                priority -= 6
        else:
            priority -= 1
        return (i_o, priority)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        if len(new) > 1 and num <= 0:
            return [new[0]]
        return new
tell = Tell('tell_about', ['tell', 'inform', 'enlighten', 'notify'], ('about',))
tell.set_d_o_requires_contact(False)
tell.set_i_o_requires_contact(False)
tell.set_i_o_requires_sight(False)

class Show(Verb2):
    def body(self, d_o, i_o):
        if isinstance(i_o, NPC):
            if d_o in i_o.get_show_responses():
                q = i_o.get_show_responses()[d_o]
                r = q[0]
                if q[1]:
                    r = '"' + r + '"'
                pront(r)
                for x in q[2]:
                    x.make_known()
            elif d_o in i_o.get_show_event_triggers():
                i_o.do_show_event(d_o)
            else:
                pront(f'"{i_o.get_unknown_show_msg()}"')
            if i_o.owngreetingPulser.get_activity():
                i_o.owngreetingPulser.reactivate()
            if i_o.ownwanderPulser.get_activity():
                i_o.ownwanderPulser.reactivate()
        else:
            pront(f'{i_o.art_d().capitalize()} is an inanimate object and does not respond.')
        inc_turn()

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(i_o, NPC):
            if d_o in i_o.get_show_responses() or d_o in i_o.get_show_event_triggers():
                priority += 3
            else:
                priority -= 6
        else:
            priority -= 1
        return (i_o, priority)
show = Show('show_to', ['show', 'reveal', 'display', 'point out', 'indicate'], ('to',))
show.set_d_o_requires_contact(False)
show.set_i_o_requires_contact(False)

class Say(VerbLit):
    def body(self, d_o):
        if d_o in ['bean', 'beans', 'borgar', 'shak', 'frie', 'hecc', 'meem', 'meme', 'it is wednesday, my dudes', 'duck', 'ducc', 'all birds are ducks', 'plugh', 'xyzzy', 'count leaves', 'kek', 'fr*ck', 'h*ck', 'finsh', 'fonsh', 'sheej', 'sheej tits', 'i hate sand', 'thicc', 'chungus', 'big chungus', 'waluigi', 'luigi', 'did you ever hear the tradgedy of darth plagueis the wise?', 'arma virumque cano', 'arma vivmqve cano', 'beef', 'beeves', 'b', 'leopards ate my face', 'embiggen', 'imbibe', 'succ', 'whomst', 'hewwo', '42', '69', '420', 'heck']:
            pront('You say "' + d_o + '." A hollow voice says, "Fool!"')
        elif d_o == 'it is wednesday my dudes':
            pront('You say "' + d_o + '." An indignant voice says, "You forgot a comma!"')
        else:
            pront('You say "' + d_o + '." Nothing happens.')
        inc_turn()
say = Say('say', ['say', 'announce', 'state', 'declare', 'incant'])

class Write(VerbLit2):
    def body(self, d_o, i_o):
        pront(f'You do not have a pen.')
write = Write('write_on', ['write', 'scrawl', 'scribble', 'jot down'], ('in', 'on'))

class Set(Verb2Lit):
    def body(self, d_o, i_o):
        pront(f'{d_o.art_d().capitalize()} is not something that can be set to anything.')
set = Set('set_to', ['set', 'turn', 'rotate', 'twist'], ('to', 'at', 'towards'))
#Space for remaps
