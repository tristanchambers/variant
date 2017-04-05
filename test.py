# To run this test execute on the command line:
# python3 test.py -v
#
"""
Models for a rythmic sequencer based on repeating base measures and
variations applied to modify them.

Examples:
>>> mypart = Part()
>>> mypart
[blank measure, blank measure, blank measure, blank measure]
>>>
>>> mybasemeasure = mypart.content[0].base_measure
>>> mybasemeasure.set_note(0, Tristate.On)
>>> mybasemeasure
[<Tristate.On: 1>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>]
>>>
>>> mynewmeasure = Measure('other measure')
>>> mypart.content[2].set_base_measure(mynewmeasure)
>>> mynewmeasure.set_note(7,Tristate.On)
>>> mynewmeasure.set_note(8,Tristate.On)
>>> mypart.content[2]
other measure
>>> mypart.content[2].get_base_measure()
[<Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.On: 1>,
 <Tristate.On: 1>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>]
>>>
>>> myvariation = mybasemeasure.make_variation()
>>> myvariation.set_note(0, Tristate.Off)
>>> myvariation.set_note(2, Tristate.On)
>>> mypart.content[3].add_variation(myvariation)
>>> mypart.content[3].get_variations()
[[<Tristate.Off: 2>,
 <Tristate.Unset: 3>,
 <Tristate.On: 1>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>,
 <Tristate.Unset: 3>]]
>>>
>>> mybasemeasure.apply_variation(myvariation)
[<Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.On: 1>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>]
>>>
>>> mypart.render().get_contents()[3].get_base_measure()
[<Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.On: 1>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>,
 <Tristate.Off: 2>]
"""

from variant import *

if __name__ == "__main__":
    import doctest
    doctest.testmod()
