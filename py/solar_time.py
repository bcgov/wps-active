def local_solar_time_single(dt, lon):  # from Mark De Jong
    """
    from weidong's wxutils.py adapted from https://stackoverflow.com/a/13424528, and 
ultimately NOAA https://www.esrl.noaa.gov/gmd/grad/solcalc/solareqns.PDF

    This func seems to be approx +/- 15 min vs the longitude-based calculation.

    I added a leap_year test (https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-2.php) which apparently affects the denominator in calculation of gamma. Testing suggest this seems to only make difference on order of milliseconds, so possibly not worth it?
    
    NOTE: that decl isn't actually used here; only used in solar zenith angle sun set/rise calculations
          need to implement these from NOAA doc if needed

    :param dt: datetime object
    :param lon: float, believe this should be [-180, 180]. NOAA doc says 'longitude is in degrees (positive to the east of the Prime Meridian)', and their spreadsheet/online calculator shows negative longitude values and doesn't work > 180 
    :return:
    """
    from datetime import datetime, time, timedelta
    
    def leap_year(y):
        if y % 400 == 0:
            return True
        if y % 100 == 0:
            return False
        if y % 4 == 0:
            return True
        else:
            return False
    
    if leap_year(dt.year):
        denominator = 366
    else:
        denominator = 365

    gamma = 2 * np.pi / denominator * (dt.timetuple().tm_yday - 1 + float(dt.hour - 12) / 24)
    eqtime = 229.18 * (0.000075 + 0.001868 * np.cos(gamma) - 0.032077 * np.sin(gamma) \
             - 0.014615 * np.cos(2 * gamma) - 0.040849 * np.sin(2 * gamma))
    #decl = 0.006918 - 0.399912 * np.cos(gamma) + 0.070257 * np.sin(gamma) \
    #       - 0.006758 * np.cos(2 * gamma) + 0.000907 * np.sin(2 * gamma) \
    #       - 0.002697 * np.cos(3 * gamma) + 0.00148 * np.sin(3 * gamma)
    time_offset = eqtime + 4 * lon
    tst = dt.hour * 60 + dt.minute + dt.second / 60 + time_offset
    solar_time = datetime.combine(dt.date(), time(0)) + timedelta(minutes=tst)
    return solar_time
