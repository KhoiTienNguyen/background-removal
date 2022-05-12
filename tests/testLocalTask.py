import unittest
from unittest import mock

import numpy as np

#from BgRemovalLocalTask import load_image
import BgRemovalLocalTask

class TestLocalTask(unittest.TestCase):
    @mock.patch('skimage.io.imread')
    def test_load_image(self, mock_imread):
        # Load grey scale image aka missing the channel dimension
        mock_imread.return_value = np.zeros((25, 25)).astype(np.uint8)
        self.assertRaises(TypeError,BgRemovalLocalTask. load_image, "dummy_path", "rgb")

        # Load the wrong type
        mock_imread.return_value = np.zeros((25, 25, 3)).astype(np.float)
        self.assertRaises(TypeError, BgRemovalLocalTask.load_image, "dummy_path", "rgb")

        # Invalid mode
        self.assertRaises(NotImplementedError, BgRemovalLocalTask.load_image, "dummy_path", "bgr")

        # Remove alpha channel
        mock_imread.return_value = np.zeros((25, 25, 4)).astype(np.uint8)
        self.assertEqual(BgRemovalLocalTask.load_image("dummy_path", "rgb").shape, (25, 25, 3), "Failed to keep 3 channels, remove the alpha channel!")

        # Mock san check
        self.assertEqual(mock_imread.call_count, 3, "mock.patch failed.")

    @mock.patch('BgRemovalLocalTask.grabImagePathList')
    @mock.patch('BgRemovalLocalTask.load_image')
    def test_load(self, mock_load_image, mock_grabImagePathList):
        mock_load_image.return_value = -1.0
        mock_grabImagePathList.return_value = ["./tmp/a.png", "./tmp/b.png", "tmp/c.png", "d.png", "./e.png"]
        ans = ['a.png', 'b.png', 'c.png', 'd.png', 'e.png']

        for idx, (name, _) in enumerate(BgRemovalLocalTask.loader(None)):
            self.assertEqual(name, ans[idx])

        self.assertTrue(mock_load_image.called, "Mock failed")
        self.assertTrue(mock_grabImagePathList.called, "Mock failed")

if __name__ == "__main__":
    unittest.main() 