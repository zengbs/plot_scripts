from __main__ import *
import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec


#################################################

FileName             = 'Data_000008'
Field                = 'temperature_sr'

CutAxis0             = 'z'
Coord0               = 50
Xmin0                = 22.5
Xmax0                = 77.5
Ymin0                = 42
Ymax0                = 58

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
Resolution           = 1000  # number of pixels in horizontal direction
CMap                 = 'arbre'
ColorBarLabel        = r'$U_{R}/c$'
norm = LogNorm()
aspect='auto'
FigSize              = 0.2

#################################################

normalconst_rho  = NormalizedConst_Pres
normalconst_pres = NormalizedConst_Dens
cylindrical_axis = 'x' 

import derived_field as df

WindowHeight0         = abs(Ymax0-Ymin0)
WindowWidth0          = abs(Xmax0-Xmin0)
BufferSize0           = [ int(Resolution), int(Resolution*WindowHeight0/WindowWidth0) ]

WindowHeight         = abs(Ymax-Ymin)
WindowWidth          = abs(Xmax-Xmin)
BufferSize           = [ int(BufferSize0[0]*0.25), int(BufferSize0[0]*0.25*WindowHeight/WindowWidth)  ]

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

sl0  = df.ds.slice(CutAxis0, Coord0, data_source=ad  )
frb0 = yt.FixedResolutionBuffer(sl0, (Xmin0, Xmax0, Ymin0, Ymax0), BufferSize0 )
frb0 = np.array(frb0[Field])

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

ColorBarMax = max(np.amax(frb0), np.amax(frb1), np.amax(frb2), np.amax(frb3), np.amax(frb4))
ColorBarMin = min(np.amin(frb0), np.amin(frb1), np.amin(frb2), np.amin(frb3), np.amin(frb4))


# Matplolib
######################################################

font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 30}

FigSize_X = WindowWidth0*FigSize
FigSize_Y = (WindowHeight0 + WindowWidth0*0.25)*FigSize

fig = plt.figure(figsize=( FigSize_X*4.3/4 , FigSize_Y ), constrained_layout=False)
gs = fig.add_gridspec(2,6,wspace=0.0, hspace=0.0, height_ratios=[WindowHeight0, WindowWidth0*0.25], width_ratios=[1,1,1,1,0.1,0.2])


ax0 = fig.add_subplot(gs[0,0:4])
im = ax0.imshow(frb0, cmap=CMap, norm=norm, aspect=aspect,  extent=[Xmin0, Xmax0, Ymin0, Ymax0], vmax=ColorBarMax, vmin=ColorBarMin )
ax0.get_xaxis().set_ticks([])
ax0.get_yaxis().set_ticks([])


ax1 = fig.add_subplot(gs[1, 0])
im = ax1.imshow(frb1, cmap=CMap, norm=norm, aspect=aspect, extent=[Xmin, Xmax, Ymin, Ymax], vmax=ColorBarMax, vmin=ColorBarMin )
ax1.get_xaxis().set_ticks([])
ax1.get_yaxis().set_ticks([])

ax2 = fig.add_subplot(gs[1, 1])
im = ax2.imshow(frb2, cmap=CMap, norm=norm, aspect=aspect, extent=[Xmin, Xmax, Ymin, Ymax], vmax=ColorBarMax, vmin=ColorBarMin )
ax2.get_xaxis().set_ticks([])
ax2.get_yaxis().set_ticks([])

ax3 = fig.add_subplot(gs[1, 2])
im = ax3.imshow(frb3, cmap=CMap, norm=norm, aspect=aspect, extent=[Xmin, Xmax, Ymin, Ymax], vmax=ColorBarMax, vmin=ColorBarMin )
ax3.get_xaxis().set_ticks([])
ax3.get_yaxis().set_ticks([])

ax4 = fig.add_subplot(gs[1, 3])
im = ax4.imshow(frb4, cmap=CMap, norm=norm, aspect=aspect, extent=[Xmin, Xmax, Ymin, Ymax], vmax=ColorBarMax, vmin=ColorBarMin )
ax4.get_xaxis().set_ticks([])
ax4.get_yaxis().set_ticks([])


ax5 = fig.add_subplot(gs[:, 5])

ax1.text(0.05,0.95,"A",horizontalalignment='left',verticalalignment='top',transform=ax1.transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
ax2.text(0.05,0.95,"B",horizontalalignment='left',verticalalignment='top',transform=ax2.transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
ax3.text(0.05,0.95,"C",horizontalalignment='left',verticalalignment='top',transform=ax3.transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
ax4.text(0.05,0.95,"D",horizontalalignment='left',verticalalignment='top',transform=ax4.transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
 
 
# Colorbar
cbar = fig.colorbar(im,cax=ax5, use_gridspec=True)
cbar.ax.tick_params(labelsize=30, color='k', direction='in', which='both')
cbar.set_label(ColorBarLabel, size=30)


#plt.show()
plt.savefig( FileOut+".eps", bbox_inches='tight', pad_inches=0.05, format='eps',dpi=800 )
