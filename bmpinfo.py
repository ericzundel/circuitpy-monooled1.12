# bmpinfo - a class that reads the data from a monochrome BMP file_handle
# Author: Eric Ayers (ericzundel@gmail.com)
#
# Oddly, no library I could find seems to handle monochrome data.
# See https://en.wikipedia.org/wiki/BMP_file_format

class BMPException(Exception):
    pass

class bmpinfo:
    def __init__(self, file_handle, **kwargs):
        """
        Read the BMP file into memory

        file_handle - opened with "rb" parameters
        """
        buffer = file_handle.read(2)

        self._magic_number = chr(buffer[0]) + chr(buffer[1])
        # print("Magic number:", self._magic_number)
        if self._magic_number != "BM":
            raise BMPException("bmpinfo.py: Unexpected magic number at beginning of BMP file: %s" % buffer)

        self._file_size = self._read_int32(file_handle)

        # print("File size:", buffer, self._file_size)

        # Skip the next 4 reserved bytes
        file_handle.read(4)

        self._data_offset = self._read_int32(file_handle)

        # The rest of the BMP header before the data has a lot of
        # information, but I think we only care about the 12 bytes of
        # BITMAPCOREHEADER which will tell us the bitmap geometry and color depth.
        # Since we are only interested in monochrome bitmaps we can
        # do a validation
        self._bmp_header_size = self._read_int32(file_handle)
        self._width = self._read_int16(file_handle)  # Only 2^16? Scandalous.
        self._height = self._read_int16(file_handle)
        self._color_planes = self._read_int16(file_handle)
        self._bits_per_pixel = self._read_int16(file_handle)
        if (self._bits_per_pixel != 1):
            self.debug_info()
            raise BMPException("bmpinfo.py: only handles monochrome bmp files. Got %d." % self._bits_per_pixel)

    def _read_int32(self, file_handle):
        buffer = file_handle.read(4)
        return (
            int(buffer[0])
            + (int(buffer[1]) << 8)
            + (int(buffer[2]) << 16)
            + (int(buffer[3]) << 24)
        )

    def _read_int16(self, file_handle):
        buffer = file_handle.read(2)
        return (
            int(buffer[0])
            + (int(buffer[1]) << 8)
        )

    def debug_info(self):
        print("Magic number: ", self.magic_number)
        print("File size:    ", self.file_size)
        print("Data offset:  ", self.data_offset)
        print("Width:        ", self.width)
        print("Height:       ", self.height)
        print("Bits per Pixel", self.bits_per_pixel)

    @property
    def magic_number(self):
        return self._magic_number

    @property
    def file_size(self):
        return self._file_size

    @property
    def data_offset(self):
        return self._data_offset

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def bits_per_pixel(self):
        return self._bits_per_pixel
