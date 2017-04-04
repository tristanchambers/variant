from pprint import pformat, pprint

class Tristate:
    """
    States that allow both on off as well as unset steps of
    a Measure.

    Examples:
    >>> Tristate.On == Tristate.Off
    False

    >>> Tristate.Off == Tristate.Unset
    False

    >>> Tristate.On == Tristate.On
    True

    >>> Tristate.Unset == Tristate.Unset
    True

    """
    class On: pass
    class Off: pass
    class Unset: pass

class Stack(list):
    """
    An ordered sequence (python list with helper method to move items
    around
    """
    def move(self, from_index, to_index):
        self.insert(to_index, self.pop(from_index))

class Measure:
    "A single measure of musical notation"
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
        Makes a variation associated with the base Measure. The
        associated variations do not apply or modify the base Measure
        until they are loaded in a Part.Bar
        """
        new_measure = MeasureVariation(self.get_name() + '-' + "variant-%s" % len(self.variations), self.get_length(), default=Tristate.Unset)
        self.variations.append(new_measure)
        return new_measure

    def get_variations(self):
        return self.variations

    def apply_variation(self, variation):
        """
        Merge a Measure and a Variation. Returns a new Measure with
        merged product.
        """

        product = Measure(self.get_name() + '-' + variation.get_name(), self.get_length())

        for step in range(self.get_length()):
            if not variation.content[step] == Tristate.Unset:
                product.set_note(step, variation.get_note(step))
            else:
                product.set_note(step, self.get_note(step))

        return product

class MeasureVariation(Measure):
    """
    Different only in name to a Measure, except that by convention
    the initial contents are set to Unset.
    The make_variation method in Measure is the intended way to make a
    MeasureVariation. This will associate it with the base Measure.
    """

    def make_variation(self):
        raise "Use the method in Measure instead"

class Part:
    """
    A sequence of Bars
    """
    def __init__(self, number_of_bars=4):
        self.name = ''
        self.content = []
        for _ in range(number_of_bars):
            self.add_bar(Part.Bar())

    def __repr__(self):
        return pformat(self.content)

    def get_number_of_bars(self):
        return self.number_of_bars

    def get_contents(self):
        return self.content

    def add_bar(self, bar):
        if type(bar) == type(Part.Bar()):
            self.content.append(bar)
        else:
            raise

    def render(self):
        """
        Return a flattened version of the Part which has all the
        variations merged.
        """
        product = Part(number_of_bars=0)
        for bar in self.get_contents():
            product.add_bar(bar.render())
        return product

    class Bar:
        """
        A position in a Part which comprises a base Measure and
        modifying variations
        """

        def __init__(self, base_measure=Measure('blank measure')):
            self.base_measure = base_measure
            self.variations = Stack()

        def __repr__(self):
            description = ''
            description = description + self.get_base_measure().get_name()
            for variation in self.get_variations():
                description = description + ' + ' + variation.get_name()
            return description

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

        def get_variations(self):
            return self.variations

        def get_base_measure(self):
            return self.base_measure

        def render(self):
            """
            Apply variations associated with the base mesaure, as
            indicated in the Bar.
            """
            product = self.get_base_measure()
            for variation in self.get_variations():
                product = product.apply_variation(variation)
            return Part.Bar(base_measure=product)

class Composition:
    """
    A sequence of Parts
    """
    def __init__(self):
        contents = Stack()

    def add_part(self, part):
        if type(part) == type(Part()):
            self.content.append(part)
        else:
            raise

    def remove_part(self, part):
        # TODO
        pass

    def move_part(self, from_index, to_index):
        # TODO
        pass
