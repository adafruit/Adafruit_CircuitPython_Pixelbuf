# SPDX-FileCopyrightText: 2026 Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Tests for PixelBuf slice assignment."""

from adafruit_pixelbuf import PixelBuf


class PixelBufMock(PixelBuf):
    """PixelBuf test double that records transmissions."""

    def __init__(self, *args, **kwargs):
        self.transmissions = 0
        super().__init__(*args, **kwargs)

    def _transmit(self, buffer):
        self.transmissions += 1


def test_rgb_tuple_fills_slice() -> None:
    """An RGB tuple is repeated over every selected pixel."""
    pixels = PixelBufMock(5, byteorder="RGB", auto_write=True)

    pixels[1:4] = (255, 0, 0)

    assert pixels[:] == [
        [0, 0, 0],
        [255, 0, 0],
        [255, 0, 0],
        [255, 0, 0],
        [0, 0, 0],
    ]
    assert pixels.transmissions == 1


def test_packed_color_fills_stepped_reverse_slice() -> None:
    """A packed integer color supports stepped and reversed slices."""
    pixels = PixelBufMock(6, byteorder="RGB")

    pixels[5:0:-2] = 0x010203

    assert pixels[:] == [
        [0, 0, 0],
        [1, 2, 3],
        [0, 0, 0],
        [1, 2, 3],
        [0, 0, 0],
        [1, 2, 3],
    ]


def test_list_keeps_per_pixel_color_semantics() -> None:
    """Lists continue to provide one color for each selected pixel."""
    pixels = PixelBufMock(3, byteorder="RGB")

    pixels[:] = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

    assert pixels[:] == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
