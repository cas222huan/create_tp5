'''
Here is the function to create the input tape5 file in MODTRAN 5
Note: some Fx.0 format may not be proper, change to Fx.3 if necessary
'''
import numpy as np
EarthRadius = 6371.23

# CARD 1: MAIN RADIATION TRANSPORT DRIVER (necessary)
# MODTRN, SPEED, BINARY, LYMOLC, MODEL, (T_BEST), ITYPE, IEMSCT, IMULT, M1, M2, M3, M4, M5, M6, MDEF, I_RD2C, NOPRNT, TPTEMP, SURREF
# FORMAT(4A1, I1, 12I5, F8.0, A7)
def create_card1(MODTRN='T', SPEED='M', BINARY='F', LYMOLC=' ', MODEL=8, ITYPE=3,IEMSCT=1, 
                 IMULT=-1, M1_6=6, MDEF=1, I_RD2C=1, NOPRNT=0, TPTEMP=0, SURREF=0.05):
    '''
    LYMOCL: include auxiliary species or not
    MODEL=8: user-defined atmosphere profile, in which altitude is calculated from pressure
    ITYPE=3: vertical or slant path to space or ground
    IEMSCT=1: program executes in spectral thermal radiance (no sun / moon) mode
    IMULT=-1: multiple scattering, for simulation of sensors on satellite platforms
    M1-M6: profiles of supplement default molecular gases
    MDEF=1: default heavy species profiles are used
    I_RD2C=1: when user input data are to be read (card 2c)
    NOPRNT=0: normal writing to tape6 and tape7
    TPTEMP<=0 : uses the temperature of the first atmospheric level as the boundary temperature
    SURREF=-3: albedos set as farm (surface parameters may be set freely since we only need atmospheric parameters)
    '''
    card1 = f'{MODTRN:1s}{SPEED:1s}{BINARY:1s}{LYMOLC:1s}{MODEL:1d}{ITYPE:5d}{IEMSCT:5d}{IMULT:5d}{M1_6:5d}\
{M1_6:5d}{M1_6:5d}{M1_6:5d}{M1_6:5d}{M1_6:5d}{MDEF:5d}{I_RD2C:5d}{NOPRNT:5d}{TPTEMP:8.0f}{str(SURREF):>7s}'
    return card1

# CARD 1A: RADIATIVE TRANSPORT DRIVER CONT'D (necessary)
# DIS, DISAZM, DISALB, NSTR, SFWHM, CO2MX, H2OSTR, O3STR, C_PROF, LSUNFL, LBMNAM, LFLTNM, H2OAER, CDTDIR, SOLCON
# CDASTM, ASTMC, ASTMX, ASTMO, AERRH, NSSALB （aerosol Angstrom Law inputs, may be ignored）
# FORMAT(3A1, I3, F4.0, F10.0, 2A10, 2A1, 4(1X, A1), F10.0, A1, F9.0, 3F10.0, I10)
def create_card1a(DIS='t', DISAZM='f', DISALB='f', NSTR=8, SFWHM=0, CO2MX=365, H2OSTR='1.0', O3STR='1.0',
                  C_PROF=' ', LSUNFL='f', LBMNAM='f', LFLTNM='f', H2OAER='t', CDTDIR='f', SOLCON=0):
    '''
    DIS=t: activate DISORT discrete ordinate multiple scattering algorithm
       =f: activate the less accurate but faster Isaac's two-stream algorithm
    DISAZM=f: no azimuth dependence, should set as false in longwave radiation
    DISALB=f: do not calculate the atmosphere spherical albedo and diffuse transmittance
    NSTR: DISORT streams
    SFWHM=0: Use default TOA solar data
    H2OSTR & O3STR='1.0': do not scale the profile
    C_PROF=' ': Do not scale default profiles
    LSUNFL=f: default solar irradiance data
    LBMNAM=f: default band model data (1 cm-1 bin)
    LFLTNM=f: do not read channel response functions
    H2OAER=t: change or fix H2O properties when water amount has changed (set H2OSTR)
    CDTDIR=f: data files in default 'DATA/'
    SOLCON=0: do not scale TOA solar irradiance
    '''
    card1a = f'{DIS:1s}{DISAZM:1s}{DISALB:1s}{NSTR:3d}{SFWHM:4.0f}{CO2MX:10.0f}{H2OSTR:>10s}\
{O3STR:>10s}{C_PROF:1s}{LSUNFL:1s} {LBMNAM:1s} {LFLTNM:1s} {H2OAER:1s} {CDTDIR:1s}{SOLCON:10.0f}'
    return card1a

# CARD 2: MAIN AEROSOL AND CLOUD OPTIONS (necessary)
# APLUS, IHAZE, CNOVAM, ISEASN, ARUSS, IVULCN, ICSTL, ICLD, IVSA, VIS, WSS, WHH, RAINRT, GNDALT
# FORMAT (A2, I3, A1, I4, A3, I2, 3I5, 5F10.5)
def create_card2(APLUS=' ', IHAZE=1, CNOVAM=' ', ISEASN=0, ARUSS=' ', IVULCN=0, ICSTL=3, ICLD=0, IVSA=0,
                 VIS=0.0, WSS=0.0, WHH=0.0, RAINRT=0.0, GNDALT=0.0):
    '''
    APLUS, CNOVAM, ARUSS: default
    IHAZE=1: RURAL extinction, default VIS = 23 km
    ICLD=0: no clouds or rain
    IVSA=0: do not use Army Vertical Structure Algorithm (VSA)
    VIS=0: set according to IHAZE model
    WSS, WHH, RAINRT: wind speed (current and daily averaged) and rain rate
    GNDALT: Altitude of surface relative to sea level (km). It is set to the first profile altitude when radiosonde data is used (in card2c).
    '''
    card2 = f'{APLUS:2s}{IHAZE:3d}{CNOVAM:1s}{ISEASN:4d}{ARUSS:3s}{IVULCN:2d}{ICSTL:5d}\
{ICLD:5d}{IVSA:5d}{VIS:10.5f}{WSS:10.5f}{WHH:10.5f}{RAINRT:10.5f}{GNDALT:10.5f}'
    return card2

# CARD 2C: user-defined atmosphere profile (optional)
# ML, IRD1, IRD2, HMODEL, REE, NMOLYC, E_MASS, AIRMWT
# FORMAT (3I5, A20, F10.0, I5, 2F10.0)
# CARD 2C1
# ZM, P, T, (WMOL(J), J = 1, 3), (JCHAR(J), J = 1, 14), JCHARX, JCHARY
# FORMAT (F10.0, 5F10.0, 14A1, 1X, 2A1)
def create_card2c(P, T, H20, O3, IRD1=0, IRD2=0, HMODEL=' ', REE=EarthRadius, NMOLYC=0, E_MASS=0, AIRMWT=0,
                  JCHAR='AAC6A666666666', JCHARX=6, JCHARY=6):
    ML = len(P)
    card2c = f'{ML:5d}{IRD1:5d}{IRD2:5d}{HMODEL:20s}{REE:10.3f}{NMOLYC:5d}{E_MASS:10.0f}{AIRMWT:10.0f}'
    ZM = 0 # altitude will be automatically calculated from pressure
    if P[0] < P[-1]:
        P = P[::-1].copy()
        T = T[::-1].copy()
        H20 = H20[::-1].copy()
        O3 = O3[::-1].copy()
    card2c1 = []
    for i in range(ML):
        card2c1_i = f'{ZM:10.3f}{P[i]:10.3f}{T[i]:10.3f}{H20[i]:10.3f}{0.0:10.3f}{O3[i]:10.3f}{JCHAR:14s} {str(JCHARX):1s}{str(JCHARY):1s}'
        card2c1.append(card2c1_i)
    return card2c, card2c1

# CARD 3: LINE-OF-SIGHT GEOMETRY (necessary)
# H1, H2, ANGLE, RANGE, BETA, RO, LENN, PHI
# FORMAT (6F10.0, I5, 5X, 2F10.0)
def create_card3(H1, VZA):
    '''
    H1: sensor altitude (km)
    H2: target altitude (km)
    ANGLE: zenith angle measured from H1 (degree)
    here only input H1 and ANGLE (case 3a for ITYPE=3)
    using VZA (in degrees) to calculate ANGLE
    '''
    r = H1 + EarthRadius
    VZA = np.deg2rad(VZA)
    alpha = np.rad2deg(np.arcsin(EarthRadius / r * np.sin(VZA)))
    ANGLE = 180 - alpha
    H2 = 0
    card3 = f'{H1:10.3f}{H2:10.3f}{ANGLE:10.3f}'
    return card3

# CARD 4: SPECTRAL RANGE AND RESOLUTION (necessary)
# V1, V2, DV, FWHM, YFLAG, XFLAG, DLIMIT, FLAGS, MLFLX, VRFRAC
# FORMAT (4F10.0, 2A1, A8, A7, I3, F10.0)
def create_card4(V1, V2, DV, FWHM, XFLAG, FLAGS, YFLAG='T', DLIMIT=' ', MLFLX=1, VRFRAC=' '):
    '''
    V1 & V2: start and final wavenumber or wavelength
    DV: wavenumber or wavelength interval (spectral resolution), the recommended value for DV is FWHM / 2
    FWHM: Slit function Full Width at Half Maximum (A minimum of twice the bin size will insure proper sampling)
        If don't want the slit function, set DV=FWHM=1 and set don't set FLAGS(1:4)
    XFLAG: W: wavenumbers or M: wavelengths in um
    MLFLX: Number of atmospheric levels for which spectral fluxes [FLAGS(7:7) = 'T' or 'F'] are output, 
        starting from the ground. If MLFLX = 0 or blanck, spectral fluxes are output for all atmospheric levels.
    '''
    card4 = f'{V1:10.3f}{V2:10.3f}{DV:10.3f}{FWHM:10.3f}{YFLAG:1s}{XFLAG:1s}{DLIMIT:>8s}{FLAGS:>7s}{MLFLX:3d}{VRFRAC:>10s}'
    return card4

# CARD 5: REPEAT RUN OPTION (necessary)
# IRPT
# FORMAT (I5)
def create_card5(IRPT):
    '''
    IRPT=0 : end of the run
        =-1: repeat the run and written messages
    '''
    card5 = f'{IRPT:5d}'
    return card5