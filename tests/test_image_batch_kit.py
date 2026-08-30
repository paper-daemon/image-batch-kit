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

    def test_same_stem_inputs_do_not_overwrite(self):
        src=Path(tempfile.mkdtemp()); out=Path(tempfile.mkdtemp())
        Image.new('RGB',(100,50),'white').save(src/'same.jpg')
        Image.new('RGBA',(50,100),(255,0,0,128)).save(src/'same.png')
        r=run(src,out,100,'webp',85)
        self.assertEqual(r['count'],2)
        names=[Path(x['output']).name for x in r['items']]
        self.assertEqual(names,['same.webp','same-2.webp'])
        self.assertTrue((out/'same.webp').exists())
        self.assertTrue((out/'same-2.webp').exists())

    def test_destructive_path_collisions_and_invalid_size_are_rejected(self):
        src=Path(tempfile.mkdtemp())
        Image.new('RGB',(1200,600),'red').save(src/'photo.jpg')
        before=(src/'photo.jpg').read_bytes()
        with self.assertRaisesRegex(ValueError, 'outdir must differ'):
            run(src,src,300,'jpg',70)
        self.assertEqual((src/'photo.jpg').read_bytes(),before)

        out=Path(tempfile.mkdtemp())
        with self.assertRaisesRegex(ValueError, 'contact sheet path'):
            run(src,out,300,'webp',85,out/'photo.webp')
        self.assertFalse((out/'photo.webp').exists())

        with self.assertRaisesRegex(ValueError, 'max_px'):
            run(src,out,0,'webp',85)

    def test_same_directory_webp_rerun_is_blocked_before_output(self):
        src=Path(tempfile.mkdtemp())
        Image.new('RGB',(100,50),'white').save(src/'photo.jpg')
        with self.assertRaisesRegex(ValueError, 'avoid reprocessing generated images'):
            run(src,src,100,'webp',85)
        self.assertEqual(sorted(p.name for p in src.iterdir()),['photo.jpg'])

if __name__=='__main__': unittest.main()
