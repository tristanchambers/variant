from pprint import pformat
import yaml
import pickle

class Tristate:
    """States that allow both on off as well as unset steps of a Measure"""
    class On: pass
    class Off: pass
    class Unset: pass

class Measure:
    "A single measure musical notation"
    def __init__(self, name, number_of_steps=16, default=Tristate.Off):
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
        """
        Makes a variation associated with the base Measure. The associated
        variations do not apply or modify the base Measure until they are loaded
        in a Part.Bar
        """
        new_measure = MeasureVariation(self.get_name() + '-' + "variant-%s" % len(self.variations), self.get_length(), default=Tristate.Unset)
        self.variations.append(new_measure)
        return new_measure

    def get_variations(self):
        return self.variations

class MeasureVariation(Measure):
    """
    Different only in name to a Measure, except that by convention the initial
    contents are set to Unset.
    The make_variation method in Measure is the intended way to make a
    MeasureVariation. This will associate it with the base Measure.
    """

    def make_variation(self):
        raise "Use the method in Measure instead"

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

class Part:
    """
    A sequence of Bars
    """
    def __init__(self, number_of_bars=4):
        self.name = ''
        self.content = []
        for _ in range(number_of_bars):
            self.content.append(Part.Bar())

    def __repr__(self):
        return pformat(self.content)

    class Bar:
        """
        A position in the Part which comprises a base Measure and modifying variations
        """
        class Stack(list):
            def move(self, from_index, to_index):
                self.insert(to_index, self.pop(from_index))

        def __init__(self, base_measure=Measure('blank measure')):
            self.base_measure = base_measure
            self.variations = Part.Bar.Stack()

        def set_base_measure(self, measure):
            if type(measure) == type(Measure('blank')):
                self.base_measure = measure
            else:
                raise

        def add_variation(self, variation):
            if type(variation) == type(MeasureVariation('blank')):
                self.variations.append(variation)
            else:
                raise "Not a MeasureVariation"

def main():
    mypart = Part()
    mybasemeasure = mypart.content[0].base_measure

    mybasemeasure.set_note(0, Tristate.On)
    mynewmeasure = Measure('other measure')
    mypart.content[2].set_base_measure(mynewmeasure)
    mynewmeasure.set_note(7,Tristate.On)
    mynewmeasure.set_note(8,Tristate.On)

    myvariation = mybasemeasure.make_variation()
    myvariation.set_note(0, Tristate.Off)
    myvariation.set_note(2, Tristate.On)

    mypart.content[3].add_variation(myvariation)

    myproduct = merge_measures(mybasemeasure, myvariation)

#    output = open('data.pkl', 'wb')
#    pickle.dump(mymeasure, output)
#    output.close()

    print(export_measure(mybasemeasure))
    print(export_measure(myvariation))
    print(export_measure(myproduct))
#    print(yaml.load(yaml.dump(mymeasure, default_flow_style=False)))
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
