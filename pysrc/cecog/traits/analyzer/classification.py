"""
                           The CellCognition Project
        Copyright (c) 2006 - 2012 Michael Held, Christoph Sommer
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

__all__ = ['SectionClassification']

SECTION_NAME_CLASSIFICATION = 'Classification'

from cecog import CHANNEL_PREFIX, CH_PRIMARY, CH_OTHER, CH_VIRTUAL
from cecog.traits.settings import _Section
from cecog.gui.guitraits import StringTrait, BooleanTrait, SelectionTrait2

class SectionClassification(_Section):

    SECTION_NAME = SECTION_NAME_CLASSIFICATION

    OPTIONS = [('%s_classification' % x, [ ('%s_classification_envpath' % x, \
                                       StringTrait('', 1000, label='Classifier folder',
                                                   widget_info=StringTrait.STRING_PATH)),
                                     ('%s_classification_regionname' % x,
                                      SelectionTrait2(None, [], label='Region name')),
                                     ('%s_classification_annotationfileext' % x,
                                      StringTrait('.xml', 50, label='Annotation ext.')) ]) \
                   for x in (CH_PRIMARY+CH_OTHER)] + \
            [('collectsamples', [ ('collectsamples', BooleanTrait(False)),
                                 ('collectsamples_prefix', StringTrait('',100))]),
            ('merged_channel', [ ('primary_channel', BooleanTrait(True, label='primary')),
                                 ('secondary_channel', BooleanTrait(True, label='secondary')),
                                 ('tertiary_channel', BooleanTrait(True, label='tertiary')) ])
            ] + \
            [('%s_classification' %CH_VIRTUAL[0],
              [ ('%s_classification_envpath' %CH_VIRTUAL[0], \
                     StringTrait('', 1000, label='Classifier folder',
                                 widget_info=StringTrait.STRING_PATH)),
                ('%s_primary_region' % CH_VIRTUAL[0],
                 SelectionTrait2(None, [], label='')),
                ('%s_secondary_region' % CH_VIRTUAL[0],
                 SelectionTrait2(None, [], label='')),
                ('%s_tertiary_region' % CH_VIRTUAL[0],
                 SelectionTrait2(None, [], label='')),
                ('%s_classification_annotationfileext' %CH_VIRTUAL[0],
                 StringTrait('.xml', 50, label='Annotation ext.')) ])]
