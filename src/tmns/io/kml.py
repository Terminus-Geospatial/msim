#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#*                                                                                    *#
#*                           Copyright (c) 2025 Terminus LLC                          *#
#*                                                                                    *#
#*                                All Rights Reserved.                                *#
#*                                                                                    *#
#*          Use of this source code is governed by LICENSE in the repo root.          *#
#*                                                                                    *#
#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#

# Python Libraries
import logging
import os


class Color_Mode:
    NORMAL=1
    RANDOM=2

    @staticmethod
    def to_string( mode ):
        if mode == Color_Mode.NORMAL:
            return 'normal'
        elif mode == Color_Mode.RANDOM:
            return 'random'
        else:
            raise Exception('Unknown Color Mode')

    @staticmethod
    def from_string( mode ):

        val = str(mode).lower()
        if val == 'normal':
            return Color_Mode.NORMAL

        elif val == 'random':
            return Color_Mode.RANDOM

        else:
            raise Exception('Unknown Color_Mode (' + str(mode) + ')')


class Altitude_Mode:

    CLAMP_TO_GROUND    = 1
    RELATIVE_TO_GROUND = 2
    ABSOLUTE           = 3

    def to_string(mode):

        if mode == Altitude_Mode.CLAMP_TO_GROUND:
            return 'clampToGround'
        elif mode == Altitude_Mode.RELATIVE_TO_GROUND:
            return 'relativeToGround'
        elif mode == Altitude_Mode.ABSOLUTE:
            return 'absolute'
        else:
            raise Exception('Unknown Mode')

    def from_string(mode):

        val = str(mode).lower()
        if val == 'clamptoground':
            return Altitude_Mode.CLAMP_TO_GROUND

        if val == 'relativetoground':
            return Altitude_Mode.RELATIVE_TO_GROUND

        if val == 'absolute':
            return Altitude_Mode.ABSOLUTE

        raise Exception('Unknown Altitude_Mode (' + str(mode) + ')')


class Object:

    def __init__(self, id = None, kml_name = 'Object'):
        self.kml_name = kml_name
        self.id = id

    def get_kml_content(self, offset = 0):
        return ''

    def as_kml( self, offset = 0 ):

        #  Create offset str
        gap = ' ' * offset

        #  Create KML Node
        output = ''
        output += gap + '<' + self.kml_name

        if self.id is not None:
            output += ' id="' + self.id + '"'
        output += '>\n'

        #  Add the content
        output += self.get_kml_content( offset + 2 )

        #  Close the KML Node
        output += gap + '</' + self.kml_name + '>\n'

        return output

    def __str__(self, offset = 0):

        gap = ' ' * offset

        #  Create output
        output = gap + 'Node: ' + self.kml_name

        return output

    #def __repr__(self):
    #    return self.__str__()


class Style_Selector( Object ):

    def __init__(self, id = None, kml_name='StyleSelector'):

        #  Build Parent
        Object.__init__( self, id = id, kml_name = kml_name )


class Sub_Style( Object ):

    def __init__(self, id=None, kml_name='SubStyle'):

        #  Build Parent
        Object.__init__(self, id=id, kml_name=kml_name)


class Color_Style( Sub_Style ):

    def __init__( self, 
                  id    = None,
                  color      = None,
                  color_mode = None,
                  kml_name   = 'ColorStyle' ):

        #  Build Parent
        Sub_Style.__init__( self, id = None, kml_name = kml_name )

        #  Set the Color
        self.color = color
        self.color_mode = color_mode


    def get_kml_content( self, offset = 0 ):

        #  Create gap string
        gap = ' ' * offset

        #  Create output
        output = ''

        #  Add parent stuff
        output += Sub_Style.get_kml_content( self, offset = offset )

        #  Set the Color
        if self.color is not None:
            output += gap + '<color>' + self.color + '</color>\n'

        #  Set the color mode
        if self.color_mode is not None:
            output += gap + '<colorMode>' + Color_Mode.to_string( self.color_mode ) + '</colorMode>\n'


        #  Return output
        return output


class Line_Style( Color_Style ):

    def __init__( self,
                  id         = None,
                  color      = None,
                  color_mode = None,
                  width      = None,
                  kml_name   = 'LineStyle' ):

        #  Build Parent
        Color_Style.__init__( self,
                              id         = id,
                              color      = color,
                              color_mode = color_mode,
                              kml_name   = kml_name )

        #  Set the Width and Color
        self.width = width

    def get_kml_content(self, offset=0):

        #  Create gap string
        gap = ' ' * offset

        #  Create Output
        output = ''

        #  Add Parent stuff
        output += Color_Style.get_kml_content( self, offset )


        #  Add the LineStyle Specific Items
        if self.width is not None:
            output += gap + '<width>' + str(self.width) + '</width>\n'

        #  Return result
        return output


class Poly_Style( Color_Style ):

    def __init__( self, 
                  id         = None,
                  color      = None,
                  color_mode = None,
                  fill       = None,
                  outline    = None,
                  kml_name   = 'PolyStyle' ):

        #  Build Parent
        Color_Style.__init__( self, 
                              id         = id,
                              color      = color,
                              color_mode = color_mode,
                              kml_name   = kml_name )

        # Set Polygon Attributes
        self.fill = fill
        self.outline = outline

    def get_kml_content( self, offset = 0 ):
        #  Create gap string
        gap = ' ' * offset

        #  Create Output
        output = ''

        #  Add Parent stuff
        output += Color_Style.get_kml_content( self, offset )

        #  Add the fill
        if self.fill:
            output += gap + '<fill>' + str(self.fill) + '</fill>\n'


        #  Return result
        return output

class Icon_Style( Color_Style ):

    def __init__( self, 
                  id         = None,
                  color      = None,
                  color_mode = None,
                  scale      = None,
                  heading    = None,
                  icon       = None,
                  kml_name   = 'PolyStyle' ):

        #  Build Parent
        Color_Style.__init__( self, 
                              id         = id,
                              color      = color,
                              color_mode = color_mode, 
                              kml_name   = kml_name )

        # Set Polygon Attributes
        self.scale = scale
        self.heading = heading
        self.icon = icon


    def get_kml_content(self, offset=0):
        #  Create gap string
        gap = ' ' * offset

        #  Create Output
        output = ''

        #  Add Parent stuff
        output += Color_Style.get_kml_content(self, offset)

        #  Add the


        #  Return result
        return output

class Label_Style(Color_Style):

    def __init__( self,
                  id=None,
                  color=None,
                  color_mode = None,
                  scale=None,
                  kml_name='LabelStyle'):

        #  Build Parent
        Color_Style.__init__( self,
                              id=id,
                              color=color,
                              color_mode=color_mode,
                              kml_name=kml_name)

        # Set Polygon Attributes
        self.scale = scale


    def get_kml_content(self, offset = 0):

        #  Create gap string
        gap = ' ' * offset

        #  Create Output
        output = ''

        #  Add Parent stuff
        output += Color_Style.Get_KML_Content(self, offset)

        #  Add the


        #  Return result
        return output

class Style( Style_Selector ):

    def __init__(self, id=None,
                 line_style=None,
                 poly_style=None,
                 icon_style=None,
                 label_style=None,
                 kml_name='Style'):

        #  Create Parent
        Style_Selector.__init__(self, id=id, kml_name=kml_name)

        #  Set styles
        self.line_style = line_style
        self.poly_style = poly_style
        self.icon_style = icon_style
        self.label_style = label_style


    def get_kml_content( self, offset = 0 ):

        #  Create gap string
        gap = ' ' * offset

        #  Create output
        output = ''

        #  add parent stuff
        output += Style_Selector.get_kml_content(self, offset)

        #  Add Line Style
        if self.line_style is not None:
            output += self.line_style.as_kml( offset=offset)

        #  Add PolyStyle
        if self.poly_style is not None:
            output += self.poly_style.as_kml( offset=offset)

        #  Add Label Style
        if self.label_style is not None:
            output += self.label_style.as_kml(offset=offset)

        #  Add Icon Style
        if self.icon_style is not None:
            output += self.icon_style.as_kml(offset=offset)


        return output


class Feature( Object ):

    def __init__(self,
                 id = None,
                 name = None,
                 visibility=None,
                 isOpen=None,
                 description=None,
                 styleUrl=None,
                 kml_name='Feature'):

        #  Construct parent
        Object.__init__(self, id=id, kml_name=kml_name)

        #  Set feature name
        self.name = name
        self.visibility = visibility
        self.isOpen = isOpen
        self.description = description
        self.styleUrl = styleUrl


    def get_kml_content( self, offset = 0 ):

        #  Create gap
        gap = ' ' * offset

        #  Create output
        output = ''

        #  Call parent method
        output += Object.get_kml_content( self, offset = offset )

        #  Set name
        if self.name is not None:
            output += gap + '<name>' + self.name + '</name>\n'

        #  Set Style URL
        if self.styleUrl is not None:
            output += gap + '<styleUrl>' + str(self.styleUrl) + '</styleUrl>\n'

        if self.visibility is not None:
            output += gap + '<visibility>'
            if self.visibility == True:
                output += '1'
            else:
                output += '0'
            output += '</visibility>\n'

        #  Process the Description
        if self.description is not None:
            output += gap + '<description>' + self.description + '</description>\n'


        return output

    def __str__( self, offset = 0 ):

        #  Create gap
        gap = ' ' * offset

        #  Create output
        output = Object.__str__( self, offset ) + '\n'

        output += gap + 'Name: ' + str(self.name)

        return output

class Geometry( Object ):

    def __init__( self,
                  id = None,
                  kml_name='Geometry' ):

        #  Call parent
        Object.__init__( self, id = id, kml_name = kml_name )



class Container( Feature ):

    def __init__(self, id = None, features = None, name = None, isOpen=None, kml_name='Container'):

        #  Build Parent
        Feature.__init__( self, 
                          id       = id,
                          name     = name,
                          isOpen   = isOpen,
                          kml_name = kml_name )


        #  Set the features
        if features is not None:
            self.features = features
        else:
            self.features = []


    def append_node(self, new_node):
        self.features.append(new_node)


    def find(self, name):

        #  Split the path
        parts = name.strip().split('/')

        #  Check if name is empty or junk
        if len(name) <= 0 or len(parts) <= 0:
            return []

        #  Check if we are at the base level
        elif len(parts) == 1:

            # Create output
            output = []

            #  Look over internal features
            for f in self.features:

                #  Check name
                if name == f.name:
                    output.append(f)
            return output


        #  If more than one level, call recursively
        else:


            #  Check if base is in node
            output = []
            for f in self.features:

                #  If the item is a container, call recursively
                if f.name == parts[0] and isinstance(f, KML_Container):

                    #  Run the query
                    res = f.Find('/'.join(map(str,parts[1:])))

                    #  Check if we got a list back
                    if (res != None) and isinstance(res, list):
                        output += res

                #  If the item is not a container, skip

            return output

        return []


    def get_kml_content( self, offset = 0 ):

        #  Create gap
        gap = ' ' * offset

        #  Create output
        output = ''

        #  Add parent material
        output += Feature.get_kml_content( self, offset = offset )

        #  Iterate over internal features
        for feature in self.features:
            output += feature.as_kml( offset + 2 )

        #  Return output
        return output


    def __str__(self, offset = 0):

        #  Create gap
        gap = ' ' * offset

        #  Create output
        output = gap + Feature.__str__(self, offset) + '\n'

        output += gap + 'Feature Nodes: Size (' + str(len(self.features)) + ')\n'
        for feature in self.features:
            output += gap + str(feature) + '\n'

        return output


class Folder( Container ):

    def __init__(self, folder_name,
                 id = None,
                 features = None,
                 isOpen=None,
                 kml_name = 'Folder' ):

        #  Construct Parent
        """
        :type kml_name: 'string'
        """
        Container.__init__( self, 
                            id       = id,
                            features = features,
                            name     = folder_name,
                            isOpen   = isOpen,
                            kml_name = kml_name )


    def __str__(self, offset=0):

        #  Create gap
        gap = ' ' * offset

        #  Create output
        output = gap + Container.__str__(self, offset)

        return output


class Document( Container ):

    def __init__( self,
                  name     = None,
                  id       = None,
                  features = None,
                  isOpen   = None,
                  kml_name = 'Document' ):

        #  Construct the parent
        Container.__init__( self, 
                            id       = id,
                            features = features,
                            name     = name,
                            isOpen   = isOpen,
                            kml_name = kml_name )


class Placemark( Feature ):

    def __init__(self,
                 id          = None,
                 name        = None,
                 visibility  = None,
                 isOpen      = None,
                 description = None,
                 styleUrl    = None,
                 kml_name    = 'Placemark',
                 geometry    = None):

        #  Call parent
        Feature.__init__( self,
                          id          = id,
                          name        = name,
                          visibility  = visibility,
                          isOpen      = isOpen,
                          description = description,
                          styleUrl    = styleUrl,
                          kml_name    = kml_name )

        #  Set the geometry
        self.geometry = geometry


    def get_kml_content( self, offset = 0 ):

        #  Create gap
        gap = ' ' * offset

        #  Create output
        output = ''

        #  Add parent material
        output += Feature.get_kml_content(self, offset=offset)

        #  Add Geometry
        if self.geometry is not None:
            output += self.geometry.as_kml( offset )

        # Return output
        return output


class Point( Geometry ):

    def __init__( self,
                  id       = None,
                  lat      = None,
                  lon      = None,
                  elev     = None,
                  alt_mode = None, 
                  kml_name = 'Point' ):

        Geometry.__init__(self, id=id, kml_name = kml_name)

        #  Set the coordinates
        self.lat = lat
        self.lon = lon
        self.elev = elev
        self.alt_mode = alt_mode


    def as_kml_simple( self ):

        output = str(self.lon) + ',' + str(self.lat) + ','
        if self.elev is None:
            output += '0'
        else:
            output += str(self.elev)
        return output


    def get_kml_content( self, offset = 0 ):

        #  Create gap
        gap = ' ' * offset

        #  Create output
        output = ''

        #  Add Parent Stuff
        output += Geometry.get_kml_content( self, offset = offset )

        #  Add the altitude mode
        if self.alt_mode is not None:
            output += gap + '<altitudeMode>' + str(self.alt_mode) + '</altitudeMode>\n'

        #  Add coordinates
        output += gap + '<coordinates>\n'
        output += gap + ' ' + str(self.lon) + ',' + str(self.lat)
        if self.elev is not None:
            output += ',' + str(self.elev)
        output += '\n' + gap + '</coordinates>\n'


        #  Return output
        return output


class Line_String( Geometry ):

    def __init__( self,
                  id       = None,
                  points   = None,
                  kml_name = 'LineString' ):

        #  Build parent
        Geometry.__init__( self, id = id, kml_name = kml_name )

        #  Set points
        if points is None:
            self.points = []
        else:
            self.points = points


class Polygon( Geometry ):

    def __init__(self,
                 id          = None,
                 innerPoints = None,
                 outerPoints = None,
                 kml_name    = "Polygon" ):

        #  Build Parent
        Geometry.__init__( self, id = id, kml_name = kml_name )

        #  Set inner points
        if innerPoints is None:
            self.innerPoints = []
        else:
            self.innerPoints = innerPoints

        #  Set outer points
        if outerPoints is None:
            self.outerPoints = []
        else:
            self.outerPoints = outerPoints


    def get_kml_content( self, offset = 0 ):

        #  Create gap
        gap = ' ' * offset

        #  Create output
        output = ''

        #  Add Parent Stuff
        output += Geometry.get_kml_content( self, offset = offset )

        #  Add the outer loop
        if len(self.outerPoints) > 0:

            #  Add the xml stuff
            output += gap + '<outerBoundaryIs>\n'
            output += gap + '  <LinearRing>\n'
            output += gap + '    <coordinates>\n'
            output += gap + '       '
            for p in self.outerPoints:
                output += p.as_kml_simple() + ' '
            output += '\n' + gap + '    </coordinates>\n'
            output += gap + '  </LinearRing>\n'
            output += gap + '</outerBoundaryIs>\n'

        #  Add the inner loop
        if len(self.innerPoints) > 0:

            #  Add the xml stuff
            output += gap + '<innerBoundaryIs>\n'
            output += gap + '  <LinearRing>\n'
            output += gap + '    <coordinates>\n'
            output += gap + '       '
            for p in self.innerPoints:
                output += p.as_kml_simple() + ' '
            output += '\n' + gap + '    </coordinates>\n'
            output += gap + '  </LinearRing>\n'
            output += gap + '</innerBoundaryIs>\n'

        return output


class Writer:

    #  List of nodes
    nodes = []

    document = None

    def __init__(self):

        #  Default nodes
        self.nodes = []

        self.document = Document()


    def add_node(self, node):

        #  Append to node
        self.document.append_node( node )

    def add_nodes( self, nodes ):

        for node in nodes:
            self.add_node( node )


    def to_string( self ):

        output  = '<?xml version="1.0" encoding="UTF-8"?>\n'
        output += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
        output += self.document.as_kml()
        output += '</kml>\n'
        return output

    def write(self, input_path, logger = None ):

        if logger is None:
            logger = logging.getLogger( 'kml.Writer' )

        #  Create output path
        output_pathname = os.path.splitext(input_path)[0] + '.kml'

        #  Open file for output
        logger.debug( f'Writing to {output_pathname}')
        with open(output_pathname, 'w') as fout:
            fout.write(self.to_string())

