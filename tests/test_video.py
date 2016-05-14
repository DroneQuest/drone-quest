from adetaylor_api.libardrone import h264decoder, paveparser
import mock
import os
import io

print('in test_video')

# def test_h264_decoder():
#     outfileobj = mock.Mock()
#     decoder = h264decoder.H264Decoder(outfileobj)
#     filepath = os.path.join(os.path.dirname(__file__), 'paveparser.output')
#     with io.open(filepath, 'r') as example_video_stream:
#         while True:
#             # Unicodedecode error in both Python 2 and 3
#             data = example_video_stream.read(1000)
#             print('read OK')
#             if len(data) == 0:
#                 break
#             decoder.write(data)

#     assert outfileobj.image_ready.called


def test_misalignment():
    outfile = mock.Mock()
    p = paveparser.PaVEParser(outfile)
    filepath = os.path.join(
        os.path.dirname(__file__),
        'ardrone2_video_example.capture'
    )
    with open(filepath, 'rb') as example_video_stream:
        while True:
            # Unicodedecode error in Python 3
            data = example_video_stream.read(1000000)
            if len(data) == 0:
                break
            p.write(data)

    assert outfile.write.called
    assert p.misaligned_frames < 3


if __name__ == "__main__":
    test_misalignment()
