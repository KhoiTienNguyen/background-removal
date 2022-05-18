import unittest
from unittest import mock

import numpy as np

import LoaderWriter

class TestLoaderWriter(unittest.TestCase):
    @mock.patch('cv2.imread')
    def test_load_image_load_check(self, mock_imread):
        mode="bgr_cv"
        dum_path = "dummy_path"

        # Load with wrong mode
        self.assertRaises(NotImplementedError, LoaderWriter.load_image, dum_path, "invalid_mode")

        # Load with sklearn
        self.assertRaises(NotImplementedError, LoaderWriter.load_image, dum_path, "rgb")

        # Load with wrong dtype
        mock_imread.return_value=np.zeros((25, 25, 3)).astype(np.float)
        self.assertRaises(TypeError, LoaderWriter.load_image, dum_path, mode)

        # Load grey scale image aka missing the channel dim
        mock_imread.return_value=np.zeros((25, 25)).astype(np.uint8)
        self.assertRaises(TypeError, LoaderWriter.load_image, dum_path, mode)

        # Load image with 4+ dims
        mock_imread.return_value=np.zeros((25, 25, 3, 2)).astype(np.uint8)
        self.assertRaises(TypeError, LoaderWriter.load_image, dum_path, mode)

        # Load image with 4+ channels
        tc = (np.random.rand(25, 25, 5)*100).astype(np.uint8)
        mock_imread.return_value=tc
        ret = LoaderWriter.load_image(dum_path, mode)
        self.assertEqual(3, ret.ndim)
        self.assertTrue(np.allclose(ret, tc[..., :3]), "Not keeping the first 3 channels (RGB)")

        # Mock san check
        self.assertEqual(mock_imread.call_count, 4, "mock.patch failed.")
    
    @mock.patch('cv2.imwrite')
    def test_write_image(self, mock_imwrite):
        pass


if __name__ == "__main__":
    # Cheat: python -m unittest discover -v -s ./tests
    unittest.main() 