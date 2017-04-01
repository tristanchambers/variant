from pprint import pformat
import yaml
import pickle

class Tristate:
    class On: pass
    class Off: pass
    class Unset: pass

class Measure:
    "A single measure, aka bar of musical notation"
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
        new_measure = Measure(self.get_name() + '-' + "variant-%s" % len(self.variations), self.get_length(), default=Tristate.Unset)
        self.variations.append(new_measure)
        return new_measure

    def get_variations(self):
        return self.variations

def merge_measures(basemeasure, variation):
    "Merge a Measure and a Variation. Returns a new Measure with merged product."

    product = Measure(basemeasure.get_name() + '-' + variation.get_name(), basemeasure.get_length())

    for step in range(basemeasure.get_length()):
        if not variation.content[step] == Tristate.Unset:
            product.set_note(step, variation.get_note(step))
        else:
            product.set_note(step, basemeasure.get_note(step))

    return product

def export_measure(measure):
    flat_content = []
    for note in measure.get_contents():
        if note == Tristate.On:
            flat_content.append(True)
        elif note == Tristate.Off:
            flat_content.append(False)
        elif note == Tristate.Unset:
            flat_content.append(None)
        else:
            flat_content.append('Unknown')
            raise
    return yaml.dump({measure.name: {'type':type(measure).__name__, 'content': flat_content}}, default_flow_style=False)

def main():
    mymeasure = Measure('mymeasure', 8)
    myvariation = mymeasure.make_variation()

    mymeasure.set_note(0, Tristate.On)
    myvariation.set_note(0, Tristate.Off)
    myvariation.set_note(2, Tristate.On)

    myproduct = merge_measures(mymeasure, myvariation)

#    output = open('data.pkl', 'wb')
#    pickle.dump(mymeasure, output)
#    output.close()

    print(export_measure(mymeasure))
    print(export_measure(myvariation))
    import pdb; pdb.set_trace()
#    print(yaml.load(yaml.dump(mymeasure, default_flow_style=False)))

if __name__ == '__main__':
    main()
