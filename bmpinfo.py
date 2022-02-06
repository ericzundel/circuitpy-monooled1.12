# bmpinfo - a class that reads the data from a monochrome BMP file_handle
# Author: Eric Ayers (ericzundel@gmail.com)
#
# Oddly, no library I could find seems to handle monochrome data.
# See https://en.wikipedia.org/wiki/BMP_file_format
#
# Debug with this in the REPL
# import bmpinfo as bi; fh = open("drew_logo.bmp", "rb") ; bmp = bi.bmpinfo(fh) ; bmp.debug_info()
import time


class BMPInfoException(Exception):
    pass


class bmpinfo:

    _BITMAPCOREHEADER_SIZE = 12
    _BITMAPINFOHEADER = 40
    _BITMAPV4HEADER_SIZE = 108

    def __init__(self, file_handle, **kwargs):
        """
        Read the BMP file into memory

        file_handle - opened with "rb" parameters
        """

        self._width = 0
        self._height = 0
        self._bits_per_pixel = 0
        self._compression = 0
        self._bmp_header_size = 0

        buffer = file_handle.read(2)
        self._magic_number = chr(buffer[0]) + chr(buffer[1])
        if self._magic_number != "BM":
            raise BMPInfoException(
                "bmpinfo.py: Unexpected magic number at beginning of BMP file: %s"
                % buffer
            )

        self._file_size = self._read_int32(file_handle)

        # Skip the next 4 reserved bytes
        file_handle.read(4)

        self._data_offset = self._read_int32(file_handle)

        # The rest of the BMP header before the data has a lot of
        # information, but I think we only care about the bitmap geometry and color depth.
        self._bmp_header_size = self._read_int32(file_handle)

        # There are several different versions of the header, indicated only by the header size
        # This is probably because the initial spec never anticipated versioning. Let this be a
        # lesson to you.
        #
        # A fancy pants way to handle the header would be to create a hierarcy of classes.
        # Seems like overkill at the moment as I just want to read four values that are
        # common to all the headers.
        if self._bmp_header_size == bmpinfo._BITMAPCOREHEADER_SIZE:
            self._read_bitmapcoreheader(file_handle)
        elif self._bmp_header_size == bmpinfo._BITMAPINFOHEADER:
            self._read_bitmapinfoheader(file_handle)
        elif self._bmp_header_size == bmpinfo._BITMAPV4HEADER_SIZE:
            self._read_bitmapv4header(file_handle)
        else:
            raise BMPInfoException("Unhandled header size: %d" % self._bmp_header_size)

        # Since we are only interested in monochrome bitmaps we can
        # do a validation
        if self._bits_per_pixel != 1:
            self.debug_info()
            raise BMPInfoException(
                "bmpinfo.py: only handles monochrome bmp files. Got %d."
                % self._bits_per_pixel
            )
        if self._compression != 0:
            self.debug_info()
            raise BMPInfoException(
                "bmpinfo.py: only handles bmp files without compression. Got %d."
                % self._compression
            )
        if self._width <= 0:
            self.debug_info()
            raise BMPInfoException("bmpinfo.py: Can't handle width: %d" % self._width)
        # Since the header can be different sizes in different version of BMP file,
        # calling seek()  will position the next read at the beginning of the data.
        file_handle.seek(self._data_offset, 0)

        self._read_bitmap_data(file_handle)
        self.debug_bitmap_data()

    def _read_bitmap_data(self, file_handle):
        self._bitmap_data = [[] for i in range(self._height)]
        for row in range(0, abs(self._height)):
            self._bitmap_data[row] = [0 for i in range(self._width)]
        # Calculate the # of bytes to the nearest 4 byte boundary that make up a row.
        # The +31 is a tricky way to get around the remaining bits not evenly divisible by 4
        row_length_bytes = (int((float(self._width) + 31.0) / 32.0)) * 4
        row = 0
        while True:
            buffer = file_handle.read(row_length_bytes)
            if not buffer:
                break
            column = 0
            for byte_val in buffer:
                if column >= self._width:
                        break
                for i in range(0,8):
                    column = column + 1
                    if column >= self._width:
                        break
                    self._bitmap_data[row][column] = ((byte_val >> i) & 1)
                    # if (self._bitmap_data[row][column] == 0):
                    #    print("0 found at %d, %d" % (row, column))
                    #    break
            row = row + 1

    def _read_bitmapcoreheader(self, file_handle):
        self._width = self._read_int16(file_handle)  # Only 2^16? Scandalous.
        self._height = self._read_int16(file_handle)
        self._color_planes = self._read_int16(file_handle)
        self._bits_per_pixel = self._read_int16(file_handle)

    def _read_bitmapinfoheader(self, file_handle):
        self._width = self._read_int32(file_handle)
        self._height = self._read_int32(file_handle)
        self._color_planes = self._read_int16(file_handle)
        self._bits_per_pixel = self._read_int16(file_handle)
        self._compression = self._read_int32(file_handle)

    def _read_bitmapv4header(self, file_handle):
        """See https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapv4header

        Starts with the same data as BITMAPINFO header and we don't care about the
        rest, so just reuse that function.
        """
        return self._read_bitmapinfoheader(file_handle)

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
        return int(buffer[0]) + (int(buffer[1]) << 8)

    def debug_info(self):
        print("Magic number: ", self.magic_number)
        print("File size:    ", self.file_size)
        print("Data offset:  ", self._data_offset)
        print("Header Size:  ", self._bmp_header_size)
        print("Width:        ", self.width)
        print(
            "Height:       ", self.height
        )  # Negative height in BMP header means rows are stored top to bottom. Otherwise bottom to top.
        print("Bits/Pixel:   ", self.bits_per_pixel)
        print("Compression:  ", self._compression)

    def debug_bitmap_data(self):
        for row in range(0, abs(self._height)):
            print("%03d:" % (row), end='')
            for column in range(0, self._width):
                if (self._bitmap_data[row][column] > 0):
                    print(self._bitmap_data[row][column], end='')
                else:
                    print(' ', end='')
            print()
            time.sleep(.05)


    @property
    def magic_number(self):
        return self._magic_number

    @property
    def file_size(self):
        return self._file_size

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def bits_per_pixel(self):
        return self._bits_per_pixel
