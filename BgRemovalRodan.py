from rodan.jobs.base import RodanTask

from . import background_removal_engine as Engine
from . import LoaderWriter

class BgRemoval(RodanTask):

    name = 'Remove background'
    author = 'author'
    description = "Use Sauvola threshold to remove background"
    settings ={}

    enabled = True
    category = 'Background removal - remove image packground'
    interactive = False

    input_port_types = [{
        'name': 'PNG image',
        'resource_types': ['image/rgb+png'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'RGB PNG image',
        'resource_types': ['image/rgb+png'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):
        mode = 'bgr_cv'
        load_image_path = inputs['PNG image'][0]['resource_path']
        image_bgr = LoaderWriter.load_image(load_image_path, mode=mode) # (W, H, 3)
        # TODO: call engine
        image_processed = image_bgr

        save_image_path = outputs['RGB PNG image'][0]['resource_path']
        LoaderWriter.write_image(save_image_path, image_processed, mode='bgr_cv')
        return True

        # image_result = image_source.to_rgb()
        # image_result.save_PNG(outputs['RGB PNG image'][0]['resource_path'])
        # for i in range(len(outputs['RGB PNG image'])):
            # image_result.save_PNG(outputs['RGB PNG image'][i]['resource_path'])
        # return True
    def my_error_information(self, exc, traceback):
        return