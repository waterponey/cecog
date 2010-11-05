"""
                           The CellCognition Project
                     Copyright (c) 2006 - 2010 Michael Held
                      Gerlich Lab, ETH Zurich, Switzerland
                              www.cellcognition.org

              CellCognition is distributed under the LGPL License.
                        See trunk/LICENSE.txt for details.
                 See trunk/AUTHORS.txt for author contributions.
"""

__author__ = 'Michael Held'
__date__ = '$Date$'
__revision__ = '$Rev$'
__source__ = '$URL$'

__all__ = ['OutputFrame']

#-------------------------------------------------------------------------------
# standard library imports:
#

#-------------------------------------------------------------------------------
# extension module imports:
#

#-------------------------------------------------------------------------------
# cecog imports:
#
from cecog.traits.analyzer.output import SECTION_NAME_OUTPUT
from cecog.gui.analyzer import _BaseFrame

#-------------------------------------------------------------------------------
# constants:
#


#-------------------------------------------------------------------------------
# functions:
#


#-------------------------------------------------------------------------------
# classes:
#
class OutputFrame(_BaseFrame):

    SECTION_NAME = SECTION_NAME_OUTPUT

    def __init__(self, settings, parent):
        _BaseFrame.__init__(self, settings, parent)

        self.add_group(None,
                       [('rendering_labels_discwrite', (0,0,1,1)),
                        ('rendering_contours_discwrite', (1,0,1,1)),
                        ('rendering_contours_showids', (1,1,1,1)),
                        ('rendering_class_discwrite', (2,0,1,1)),
                        ('rendering_class_showids', (2,1,1,1)),
                        ], link='export_result_images',
                        label='Export result images')
        self.add_group(None,
                       [('export_object_counts', (0,0,1,1)),
                        ('export_object_details', (1,0,1,1)),
                        ('export_track_data', (2,0,1,1)),
                        ], link='statistics', label='Statistics')
        self.add_group('imagecontainer_create_file',
                       [('imagecontainer_reuse_file',),
                        ], layout='flow')
        self.add_group('netcdf_create_file',
                       [('netcdf_reuse_file',),
                        ], layout='flow')
        self.add_expanding_spacer()