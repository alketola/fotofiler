class FotoInfo:
    """
    Collection of photo information

    """
    
    
    def __init__(self, source_path, date, dest_root, dest_dir, filename):
        """
        Class constructor. Stores photo information.

        >>> f=FotoInfo(r'C:/users',"12345678", r"D:/", "7", "1.txt")
        >>> f.source_path
        'C:/users'
        >>> f.date
        '12345678'
        >>> f.dest_root
        'D:/'
        >>> f.dest_dir
        '7'
        >>> f.filename
        '1.txt'
        >>> f.full_dest_path
        'D:/7/1.txt'
        >>>
            
        """
        self.source_path = source_path
        self.date = date
        self.dest_root = dest_root
        self.dest_dir = dest_dir
        self.filename = filename 
        self.full_dest_path = dest_root+dest_dir+'/'+filename


    def set_exif_gps_coord(self,
                           gps_longitude,
                           gps_longitude_ref,
                           gps_latitude,
                           gps_latitude_ref):

        """ Store GPS coordinates quickly without processing.

        It is presumed that there's more time to process data
        before reading.
        """
        
        self.gps_longitude = gps_longitude
        self.gps_longitude_ref = gps_longitude_ref
        self.gps_latitude = gps_latitude
        self.gps_latitude_ref = gps_latitude_ref


    def set_date(self, date):
        """ Store ISO 8601 date quickly without processing.

        It is presumed that there's more time to process data
        before reading.
        """

        self.date = date


    def get_date(self):
        return (self.gps_date, self.gps_timestamp)


    def get_gps_coord_float(self):
        """ Return from GPS coordinates as a tuple of decimal numbers 
            (longitude_d, latitude_d)

            returns None, if something goes wrong
        """
        
        try:
            longsec = eval(self.gps_longitude[2])/3600
            latsec = eval(self.gps_latitude[2])/3600
            longitude_d = self.gps_longitude[0]+ self.gps_longitude[1]/60 + longsec
            latitude_d = self.gps_latitude[0]+ self.gps_latitude[1]/60 + latsec
        except:
            return None

        return (longitude_d, latitude_d)

    
if __name__ == '__main__':
  import doctest
  doctest.testmod()
  print("ran doctests")
