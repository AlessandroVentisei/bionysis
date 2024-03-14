"""
Model exported as python.
Name : DEM
Group : 
With QGIS : 32815
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing


class Dem(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('dtm', 'DTM', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('dsm', 'DSM', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('osm', 'OSM', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Dem_ex_buildings', 'DEM_ex_buildings', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Buildings', 'buildings', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Dem', 'DEM', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # Raster calculator
        alg_params = {
            'CELLSIZE': 0,
            'CRS': QgsCoordinateReferenceSystem('EPSG:27700'),
            'EXPRESSION': '"DSM@1" - "DTM@1"',
            'EXTENT': None,
            'LAYERS': None,
            'OUTPUT': parameters['Dem']
        }
        outputs['RasterCalculator'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Dem'] = outputs['RasterCalculator']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Assign projection
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:27700'),
            'INPUT': parameters['dtm']
        }
        outputs['AssignProjection'] = processing.run('gdal:assignprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': '"building" is not null',
            'INPUT': parameters['osm'],
            'OUTPUT': parameters['Buildings']
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Buildings'] = outputs['ExtractByExpression']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Assign projection
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:27700'),
            'INPUT': parameters['dsm']
        }
        outputs['AssignProjection'] = processing.run('gdal:assignprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Clip raster by extent
        alg_params = {
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': outputs['RasterCalculator']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': '',
            'OVERCRS': False,
            'PROJWIN': outputs['ExtractByExpression']['OUTPUT'],
            'OUTPUT': parameters['Dem_ex_buildings']
        }
        outputs['ClipRasterByExtent'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Dem_ex_buildings'] = outputs['ClipRasterByExtent']['OUTPUT']
        return results

    def name(self):
        return 'DEM'

    def displayName(self):
        return 'DEM'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Dem()
