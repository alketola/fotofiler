class FotoInfo:
    """
    Collection of photo information
        
    """

    
    def __init__(self, source_path, date, dest_root, dest_dir, filename):
        self.source_path = source_path
        self.date = date
        self.dest_root = dest_root
        self.dest_dir = dest_dir
        self.filename = filename
        self.full_dest_path = dest_root+dest_dir+'\\'+filename


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


    def get_gps_coord_float():
        """ Return from GPS coordinates as a tuple of decimal numbers """
        
        try:
            longsec = eval(self.gps_longitude[2])/3600
        except:
            longsec = 0.0

        try:
            latsec = eval(self.gps_latitude[2])/3600
        except:
            latsec = 0.0
        try:
            longitude = self.gps_longitude[0]+ self.gps_longitude[1]/60 + longsec
        except:
            return (0.0,0.0)

    
