# Write your code here :-)
class bmpinfo:
    def __init__(self,  **kwargs):
        pass


    def do(self, file_handle):
        """ file_handle - opened with "rb" parameters
        """
        buffer = file_handle.read(2)
        magic_number = chr(buffer[0]) + chr(buffer[1])
        print("Magic number:", magic_number);
        buffer = file_handle.read(4)
        file_size = int(buffer[0]) + (int(buffer[1]) << 8) + (int(buffer[2]) << 16) + (int(buffer[3]) << 24)
        print("File size:", buffer, file_size)
