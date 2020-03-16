from __main__ import *
import argparse
import sys
import yt
import numpy as np
import yt.visualization.eps_writer as eps
import time
import os
import math

Plot__Paramater = {}
Input__TestProb = {}



FilePtr1 = open('Input__TestProb', "r")
FilePtr2 = open('Plot__Paramater', "r")


for line in FilePtr1:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        try:
            Input__TestProb[key] = float(value)
        except ValueError:
            Input__TestProb[key] = value

for line in FilePtr2:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        try:
            Plot__Paramater[key] = float(value)
        except ValueError:
            Plot__Paramater[key] = value

FilePtr1.close()
FilePtr2.close()


if (Plot__Paramater['NormalizedConst_Dens'] == 'auto'):
    normalconst_rho = Input__TestProb['Jet_SrcDens']

if (Plot__Paramater['NormalizedConst_Pres'] == 'auto'):
    normalconst_pres = Input__TestProb['Jet_SrcDens'] * Input__TestProb['Jet_SrcTemp']



import derived_field as df


colormap = 'arbre'
dpi = 150


########################################

SliceMax             = Plot__Paramater['SliceMax'] 
SliceMin             = Plot__Paramater['SliceMin'] 
CutAxis              = Plot__Paramater['CutAxis']  
 
DumpIDMin            = Plot__Paramater['DumpIDMin']  
DumpIDMax            = Plot__Paramater['DumpIDMax']  
DumpIDDelta          = Plot__Paramater['DumpIDDelta']  
Zoom                 = Plot__Paramater['Zoom']  
AxisUnit             = Plot__Paramater['AxisUnit']
NumSlice             = Plot__Paramater['NumSlice']  
FileFormat           = Plot__Paramater['FileFormat']
Title                = Plot__Paramater['Title']
Axis                 = Plot__Paramater['Axis']  
TimeStamp            = Plot__Paramater['TimeStamp']  
TimeUnit             = Plot__Paramater['TimeUnit']
ColorBar             = Plot__Paramater['ColorBar']  
CenterOffset_x       = Plot__Paramater['CenterOffset_x']  
CenterOffset_y       = Plot__Paramater['CenterOffset_y']                    
CenterOffset_z       = Plot__Paramater['CenterOffset_z']
WindowHeight         = Plot__Paramater['WindowHeight'] 
WindowWidth          = Plot__Paramater['WindowWidth'] 
 
NormalizedConst_Pres = Plot__Paramater['NormalizedConst_Pres'] 
NormalizedConst_Dens = Plot__Paramater['NormalizedConst_Dens'] 
Resolution           = Plot__Paramater['Resolution']
FigSize              = Plot__Paramater['FigSize'] 
ColorBarMax          = Plot__Paramater['ColorBarMax']                                                                                                        
ColorBarMin          = Plot__Paramater['ColorBarMin']
NameColorBar         = Plot__Paramater['NameColorBar']
ColorBarUnit         = Plot__Paramater['ColorBarUnit']
LogScale             = Plot__Paramater['LogScale']  
LinThresh            = Plot__Paramater['LinThresh'] 
Grid                 = Plot__Paramater['Grid'] 

Field                = Plot__Paramater['Field'] 




# check parameter
########################################


# choose proper unit for field
########################################
if Field == 'proper_mass_density':
    unit = 'g/cm**3'
    function = df._proper_mass_density
if Field == 'temperature_sr':
    unit = ''
    function = df._temperature_sr
if Field == 'Lorentz_factor':
    unit = ''
    function = df._lorentz_factor
if Field == 'Lorentz_factor_1':
    unit = ''
    function = df._lorentz_factor_1
if Field == 'pressure_sr':
    unit = 'g/cm**3'
    function = df._pressure_sr
if Field == '4_velocity_x':
    unit = ''
    function = df._4_velocity_x
if Field == '4_velocity_y':
    unit = ''
    function = df._4_velocity_y
if Field == '4_velocity_z':
    unit = ''
    function = df._4_velocity_z
if Field == 'specific_enthalpy_sr':
    unit = ''
    function = df._specific_enthalpy_sr
if Field == 'total_energy_per_volume':
    unit = 'g/(cm*s**2)'
if Field == 'gravitational_potential':
    unit = '(cm/s)**2'
    function = df._gravitational_potential
if Field == 'mass_density_sr':
    unit = 'g/cm**3'
    function = df._mass_density_sr
if Field in ('momentum_x', 'momentum_y', 'momentum_z'):
    unit = 'g/(s*cm**2)'
if Field == 'thermal_energy_density_sr':
    unit = 'g/(cm*s**2)'
    function = df._thermal_energy_density_sr
if Field == 'kinetic_energy_density_sr':
    unit = 'g/(cm*s**2)'
    function = df._kinetic_energy_density_sr
if Field == 'Bernoulli_constant':
    unit = ''
    function = df._Bernoulli_const
if Field == 'spherical_radial_4velocity':
    unit = ''
    function = df._spherical_radial_4velocity
if Field == 'cylindrical_radial_4velocity':
    unit = ''
    function = df._cylindrical_radial_4velocity
if Field == '3_velocity_x':
    unit = ''
    function = df._3_velocity_x
if Field == '3_velocity_y':
    unit = ''
    function = df._3_velocity_y
if Field == '3_velocity_z':
    unit = ''
    function = df._3_velocity_z
if Field == '3_velocity_magnitude':
    unit = ''
    function = df._3_velocity_magnitude
if Field == 'entropy_per_particle':
    unit = ''
    function = df._entropy_per_particle
if Field == 'sound_speed':
    unit = ''
    function = df._sound_speed
if Field == 'threshold':
    unit = ''
    function = df._threshold
if Field == 'internal_energy_density_sr':
    unit = 'g/(cm*s**2)'
    function = df._internal_energy_density_sr
if Field == 'Mach_number_sr':
    unit = ''
    function = df._Mach_number_sr


t0 = time.time()

yt.enable_parallelism()


ts = yt.load(['Data_%06d' %  idx for idx in range(int(DumpIDMin), int(DumpIDMax)+1, int(DumpIDDelta))])


for df.ds in ts.piter():

    #  the dimension of window
    if (WindowWidth == 'auto' or WindowHeight == 'auto'):
        if   CutAxis == 'x':
            WindowWidth  = df.ds["BoxSize"][1]
            WindowHeight = df.ds["BoxSize"][2]
        elif CutAxis == 'y':
            WindowWidth  = df.ds["BoxSize"][2]
            WindowHeight = df.ds["BoxSize"][0]
        elif CutAxis == 'z':
            WindowWidth  = df.ds["BoxSize"][0]
            WindowHeight = df.ds["BoxSize"][1]

    #   resolution
    if Resolution == 'max':
        BoxSize    = np.asarray(df.ds["BoxSize"])
        MaxLevel   = np.asarray(df.ds["MaxLevel"])
        NX0_Tot    = np.asarray(df.ds["NX0_Tot"])
        MaxBoxSize = np.amax(BoxSize)

        Area = (FigureSize**2) * (np.amin(WindowWidth, WindowHeight) / max(WindowWidth, WindowHeight))
        dx = MaxBoxSize / (np.amax(NX0_Tot)*2**MaxLevel)
        Resolution = Area / dx**2
    elif Resolution == 'auto':
        Resolution = 150


    #   add derived field
    if Field not in ('total_energy_per_volume', 'momentum_x', 'momentum_y', 'momentum_z'):
        df.ds.add_field(("gamer", Field), function=function, sampling_type="cell", units=unit)

    ad = df.ds.all_data()

    origin = SliceMin

    center = df.ds.domain_center
    center[0] += CenterOffset_x * df.ds.length_unit
    center[1] += CenterOffset_y * df.ds.length_unit
    center[2] += CenterOffset_z * df.ds.length_unit

    while origin <= SliceMax:
 
        # center coordinate of window
        if CutAxis == 'x':
            center[0] = origin
        elif CutAxis == 'y':
            center[1] = origin
        elif CutAxis == 'z':
            center[2] = origin
        else:
            print("CutAxis should be x, y or z!\n")
            sys.exit(0)


        sz = yt.SlicePlot(df.ds, CutAxis, Field, center=center, origin='native', data_source=ad, width=(WindowWidth, WindowHeight))


        # set the range of color bar
        if ( ColorBarMin == 'auto' and not ColorBarMax == 'auto'):
            sz.set_zlim(Field, "min", ColorBarMax)
        elif (not ColorBarMin == 'auto' and ColorBarMax == 'auto'):
            sz.set_zlim(Field, ColorBarMin, "max")
        elif ( ColorBarMin == 'auto' and ColorBarMax == 'auto'):
            sz.set_zlim(Field, "min", "max")
        else:
            sz.set_zlim(Field, ColorBarMin, ColorBarMax)

        # axis
        if ( Axis == 'off'):
            sz.hide_axes()

        # color bar
        if ( ColorBar == 'off' ):
            sz.hide_colorbar()

        # figure size
        if (FigSize != 'auto'):
            sz.set_figure_size(FigSize)

        # set linear scale around zero
        if (LinThresh > 0  and LogScale == 'on'):
            sz.set_log(Field, LogScale, LinThresh)
        elif (LinThresh <= 0):
            sz.set_log(Field, LogScale)

        # zoom in
        sz.zoom(Zoom)

        # colorbar label
        if ( '@' in NameColorBar ):      # with unit
          NameColorBar = NameColorBar.split('@')
          sz.set_colorbar_label( Field, NameColorBar[0] + ' ' + NameColorBar[1] )
        elif ( NameColorBar != 'auto' ): # without unit
          sz.set_colorbar_label( Field, NameColorBar )
    

        if CutAxis == 'x':
            x = '%0.3f' % center[0]
            CutAxis = 'x='+x.zfill(8)
        elif CutAxis == 'y':
            y = '%0.3f' % center[1]
            CutAxis = 'y='+y.zfill(8)
        elif CutAxis == 'z':
            z = '%0.3f' % center[2]
            CutAxis = 'z='+z.zfill(8)

        #  title
        if (Title == 'auto'):
            pwd = os.getcwd()
            pwd = pwd.split('/')
            sz.annotate_title('slice (' + CutAxis + ') ' + pwd[-1])
        else:
            sz.annotate_title(Title)

        # font
        sz.set_font({'weight': 'bold', 'size': '30'})

        # time stamp
        if (TimeStamp == 'on'):
            if (TimeUnit == 'code_time'):
                sz.annotate_timestamp(time_unit='code_time', corner='upper_right',
                                      time_format='t = {time:.4f} ' + AxisUnit + '/$c$', text_args={'color': 'black'})
            else:
                NormalizedTime = df.ds["Time"][0] * Zoom / max(WindowWidth, WindowHeight)

                sz.annotate_timestamp(time_unit='code_time', corner='upper_right', 
                                      time_format='t = ' + str("%.1f" % (NormalizedTime)) + " " + TimeUnit, 
                                      text_args={'color': 'white'})

        sz.set_cmap(Field, colormap)
        sz.set_unit(Field, unit)
        sz.set_axes_unit(AxisUnit)

        # grid
        if Grid == 'on':
            sz.annotate_grids()

        # save figure
        #  mpl_kwargs: A dict to be passed to 'matplotlib.pyplot.savefig'
        sz.save(name='Data_%06d_' % df.ds["DumpID"] + str(CutAxis), suffix=FileFormat,
                mpl_kwargs={"dpi": Resolution, "facecolor": 'w', "edgecolor": 'w',"bbox_inches":'tight', "pad_inches": 0.0})

        if NumSlice > 1:
            origin += np.fabs(SliceMin-SliceMax)/(NumSlice-1)
        else:
            origin = SliceMax + 1

t1 = time.time()

print("Done! it took %.5e sec" % (t1 - t0))
