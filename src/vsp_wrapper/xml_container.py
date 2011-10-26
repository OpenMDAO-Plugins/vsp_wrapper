import string
import xml.etree.cElementTree as ElementTree

from enthought.traits.trait_base import not_none

from openmdao.main.api import Container

# Used for making a legal OpenMDAO container name from a VSP component name.
XLATE = string.maketrans(' -.', '___')


class XMLContainer(Container):
    """
    A container for XML parameters. XML parameters are designated by an
    `xmltag` metadata item in a trait.
    """

    def __init__(self, xmltag):
        super(XMLContainer, self).__init__()
        self._xmltag = xmltag

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        for name, obj in self.items(xmltag=not_none):
            self.read_element(this, name, obj)

    def read_element(self, this, name, obj=None):
        """ Read one parameter from XML tree element `this`. """
        if obj is None:
            obj = getattr(self, name)
        trait = self.trait(name)
        text = this.findtext(trait.xmltag, trait.default)
        if isinstance(obj, bool):
            setattr(self, name, int(text) != 0)
        elif isinstance(obj, float):
            setattr(self, name, float(text))
        elif isinstance(obj, int):
            setattr(self, name, int(text))
        elif isinstance(obj, str):
            setattr(self, name, text)
        else:
            self.raise_exception('%s is of an unsupported type %s'
                                 % (name, type(obj)), TypeError)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = ElementTree.Element(self._xmltag)
        this.text = self.tail(nesting+1)
        this.tail = self.tail(nesting)
        for name, obj in sorted(self.items(xmltag=not_none),
                                key=lambda x: x[0]):
            trait = self.trait(name)
            child = ElementTree.Element(trait.xmltag)
            if isinstance(obj, bool):
                child.text = '1' if obj else '0'
            else:
                child.text = str(obj)
            child.tail = self.tail(nesting+1)
            this.append(child)

        if parent is not None:
            parent.append(this)

        return this

    @staticmethod
    def tail(nesting=0):
        """ Return string to make XML tree dump more readable. """
        return '\n%s' % ('  ' * nesting)

