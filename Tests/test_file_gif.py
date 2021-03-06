from tester import *

from PIL import Image

codecs = dir(Image.core)

if "gif_encoder" not in codecs or "gif_decoder" not in codecs:
    skip("gif support not available") # can this happen?

# sample gif stream
file = "Images/lena.gif"
with open(file, "rb") as f:
    data = f.read()

def test_sanity():
    im = Image.open(file)
    im.load()
    assert_equal(im.mode, "P")
    assert_equal(im.size, (128, 128))
    assert_equal(im.format, "GIF")

def test_optimize():
    def test(optimize):
        im = Image.new("L", (1, 1), 0)
        file = BytesIO()
        im.save(file, "GIF", optimize=optimize)
        return len(file.getvalue())
    assert_equal(test(0), 800)
    assert_equal(test(1), 38)

def test_roundtrip():
    out = tempfile('temp.gif')
    im = lena()
    im.save(out)
    reread = Image.open(out)

    assert_image_similar(reread.convert('RGB'), im, 50)

def test_roundtrip2():
    #see https://github.com/python-imaging/Pillow/issues/403
    out = 'temp.gif'#tempfile('temp.gif')
    im = Image.open('Images/lena.gif')
    im2 = im.copy()
    im2.save(out)
    reread = Image.open(out)

    assert_image_similar(reread.convert('RGB'), lena(), 50)

