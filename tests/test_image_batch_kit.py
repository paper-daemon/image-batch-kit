import tempfile, unittest
from pathlib import Path
from PIL import Image
from image_batch_kit import run

class T(unittest.TestCase):
    def test_resize_convert_sheet(self):
        src=Path(tempfile.mkdtemp()); out=Path(tempfile.mkdtemp())
        Image.new('RGB',(2000,1000),'white').save(src/'a.jpg')
        Image.new('RGBA',(400,800),(255,0,0,128)).save(src/'b.png')
        r=run(src,out,600,'webp',85,out/'sheet.jpg')
        self.assertEqual(r['count'],2)
        self.assertTrue((out/'a.webp').exists())
        self.assertTrue((out/'b.webp').exists())
        self.assertTrue((out/'sheet.jpg').exists())
        self.assertLessEqual(max(r['items'][0]['after']),600)

if __name__=='__main__': unittest.main()
