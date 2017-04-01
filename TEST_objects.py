from pprint import pformat
import yaml

class Tristate(object):
    class On: pass
    class Off: pass
    class Unset: pass

class Bar:
    "A single bar, aka measure of musical notation"
    def __init__(self, name, number_of_steps, default=Tristate.Off):
        self.name = name
        self.content = []
        self.number_of_steps = number_of_steps
        self.variations = []
        for _ in range(self.number_of_steps):
            self.content.append(default)

    def __repr__(self):
        return pformat(self.content)

    def set_note(self, position, state):
        "Set the value of a note at a given position"
        try:
            self.content[position] = state
        except IndexError:
            # do some error handling stuff here
            return("you can't do that")

    def get_note(self, position):
        return self.content[position]

    def get_length(self):
        return len(self.content)

    def get_contents(self):
        return self.content

    def get_name(self):
        return self.name

    def make_variation(self):
        new_bar = Bar(self.get_name() + '-' + "variant-%s" % len(self.variations), self.get_length(), default=Tristate.Unset)
        self.variations.append(new_bar)
        return new_bar

    def get_variations(self):
        return self.variations

def diff_bars(basebar, variation):
    "Merge a Bar and a Variation. Returns a new Bar with merged product."

    product = Bar(basebar.get_name() + '-' + variation.get_name(), basebar.get_length())

    for step in range(basebar.get_length()):
        if not variation.content[step] == Tristate.Unset:
            product.set_note(step, variation.get_note(step))
        else:
            product.set_note(step, basebar.get_note(step))

    return product

mybar = Bar('mybar', 3)
myvariation = mybar.make_variation()

mybar.set_note(0, Tristate.On)
myvariation.set_note(0, Tristate.Off)
myvariation.set_note(2, Tristate.On)

myproduct = diff_bars(mybar, myvariation)

def export_yaml(bar):
    flat_content = []
    for note in bar.get_contents():
        if note == Tristate.On:
            flat_content.append(True)
        elif note == Tristate.Off:
            flat_content.append(False)
        elif note == Tristate.Unset:
            flat_content.append(None)
        else:
            flat_content.append('Unknown')
            raise
    return yaml.dump({bar.name: {'type':type(bar).__name__, 'content': flat_content}}, default_flow_style=False)

print(export_yaml(mybar))
print(export_yaml(myvariation))

import pdb; pdb.set_trace()
