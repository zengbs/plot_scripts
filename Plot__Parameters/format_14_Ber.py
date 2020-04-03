from __main__ import *
import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import ImageGrid


#################################################

FileName             = 'Data_000008'
Field                = 'Bernoulli_constant'
CutAxis              = 'x'
Coord1               = 34
Coord2               = 39
Coord3               = 44
Coord4               = 48
Xmin                 = 48.7
Xmax                 = 51.3
Ymin                 = 48.7
Ymax                 = 51.3
NormalizedConst_Pres = 1
NormalizedConst_Dens = 1
Resolution           = 800  # number of pixels in horizontal direction
CMap                 = 'arbre'
ColorBarMax          = 26.600
ColorBarMin          = 26.245 
ColorBarLabel        = '$h\gamma/c^{2}$'

#################################################

normalconst_rho  = NormalizedConst_Pres
normalconst_pres = NormalizedConst_Dens
cylindrical_axis = 'x' 

import derived_field as df


WindowHeight         = abs(Xmax-Xmin)
WindowWidth          = abs(Ymax-Ymin)
BufferSize           = [ Resolution, int(Resolution*(WindowHeight/WindowWidth)) ]

FileOut              = FileName + '_' + Field

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



df.ds = yt.load(FileName)


#   add derived field
if Field not in ('total_energy_per_volume', 'momentum_x', 'momentum_y', 'momentum_z'):
    df.ds.add_field(("gamer", Field), function=function, sampling_type="cell", units=unit)

ad = df.ds.all_data()

sl1  = df.ds.slice(CutAxis, Coord1, data_source=ad  )
frb1 = yt.FixedResolutionBuffer(sl1, (Xmin, Xmax, Ymin, Ymax), BufferSize )
frb1 = np.array(frb1[Field])


sl2  = df.ds.slice(CutAxis, Coord2, data_source=ad )
frb2 = yt.FixedResolutionBuffer(sl2, (Xmin, Xmax, Ymin, Ymax), BufferSize)
frb2 = np.array(frb2[Field])

sl3  = df.ds.slice(CutAxis, Coord3, data_source=ad  )
frb3 = yt.FixedResolutionBuffer(sl3, (Xmin, Xmax, Ymin, Ymax), BufferSize )
frb3 = np.array(frb3[Field])

sl4  = df.ds.slice(CutAxis, Coord4, data_source=ad  )
frb4 = yt.FixedResolutionBuffer(sl4, (Xmin, Xmax, Ymin, Ymax), BufferSize )
frb4 = np.array(frb4[Field])

#ColorBarMax = max(np.amax(frb1), np.amax(frb2), np.amax(frb3), np.amax(frb4))
#ColorBarMin = min(np.amin(frb1), np.amin(frb2), np.amin(frb3), np.amin(frb4))


# Matplolib
######################################################

font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 30}

fig = plt.figure(figsize=(20, 5))
#fig, axs = plt.subplots(nrows=1, ncols=4, sharex=True)

# Remove horizontal space between axes
#fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=None)


grid = ImageGrid(fig, 111,          # as in plt.subplot(111)
                 nrows_ncols=(1,4),
                 axes_pad=0.15, 
                 share_all=False, 
                 cbar_location="right", 
                 cbar_mode="single", 
                 cbar_size="7%", 
                 cbar_pad=0.15, )


#im = grid[0].imshow(frb1, cmap=CMap , norm=LogNorm(), extent=[Xmin, Xmax, Ymin, Ymax])
im = grid[0].imshow(frb1, cmap=CMap , extent=[Xmin, Xmax, Ymin, Ymax], vmax=ColorBarMax, vmin=ColorBarMin )
grid[0].get_xaxis().set_ticks([])
grid[0].get_yaxis().set_ticks([])

#im = grid[1].imshow(frb2, cmap=CMap , norm=LogNorm(), extent=[Xmin, Xmax, Ymin, Ymax])
im = grid[1].imshow(frb2, cmap=CMap , extent=[Xmin, Xmax, Ymin, Ymax], vmax=ColorBarMax, vmin=ColorBarMin )
grid[1].get_xaxis().set_ticks([])
grid[1].get_yaxis().set_ticks([])

#im = grid[2].imshow(frb3, cmap=CMap , norm=LogNorm(), extent=[Xmin, Xmax, Ymin, Ymax])
im = grid[2].imshow(frb3, cmap=CMap , extent=[Xmin, Xmax, Ymin, Ymax], vmax=ColorBarMax, vmin=ColorBarMin )
grid[2].get_xaxis().set_ticks([])
grid[2].get_yaxis().set_ticks([])

#im = grid[3].imshow(frb4, cmap=CMap , norm=LogNorm(), extent=[Xmin, Xmax, Ymin, Ymax])
im = grid[3].imshow(frb4, cmap=CMap , extent=[Xmin, Xmax, Ymin, Ymax], vmax=ColorBarMax, vmin=ColorBarMin )
grid[3].get_xaxis().set_ticks([])
grid[3].get_yaxis().set_ticks([])


grid[0].text(0.05,0.85,"A",transform=grid[0].transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
grid[1].text(0.05,0.85,"B",transform=grid[1].transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
grid[2].text(0.05,0.85,"C",transform=grid[2].transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
grid[3].text(0.05,0.85,"D",transform=grid[3].transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )


# Colorbar
cbar = grid[3].cax.colorbar(im)
cbar.ax.tick_params(labelsize=30, color='k', direction='in')
cax = grid.cbar_axes[0]
axis = cax.axis[cax.orientation]
axis.label.set_text(ColorBarLabel)
axis.label.set_size(30)

plt.savefig( FileOut+".eps", bbox_inches='tight', pad_inches=0.05, format='eps',dpi=800 )
