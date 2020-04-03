from __main__ import *
import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
from string import ascii_uppercase


#################################################

FileName             = 'Data_000000'
Field                = 'temperature_sr'

CutAxis0             = 'z'
Coord0               = 50
Xmin0                = 22.5
Xmax0                = 77.5
Ymin0                = 42
Ymax0                = 58

CutAxis1             = 'x'
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
aspect='equal'
FigSize              = 1

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
BufferSize1          = [ int(BufferSize0[0]*0.25), int(BufferSize0[0]*0.25*WindowHeight/WindowWidth)  ]

FileOut              = FileName + '_' + Field

Coord      = [ Coord0, Coord1, Coord2, Coord3, Coord4 ]
CutAxis    = [ CutAxis0, CutAxis1, CutAxis1, CutAxis1, CutAxis1 ]
Extent0    = [Xmin0, Xmax0, Ymin0, Ymax0]
Extent1    = [Xmin , Xmax , Ymin , Ymax ]

Extent     = [     Extent0,     Extent1,     Extent1,     Extent1,     Extent1 ]
BufferSize = [ BufferSize0, BufferSize1, BufferSize1, BufferSize1, BufferSize1 ]

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

sl  = [None]*5
frb = [None]*5

for i in range(0,5):
  sl[i]  =  df.ds.slice(CutAxis[i], Coord[i], data_source=ad  ) 
  frb[i] = yt.FixedResolutionBuffer(sl[i], Extent[i],  BufferSize[i] )
  frb[i] = np.array(frb[i][Field])


ColorBarMax = max(np.amax(frb[0]), np.amax(frb[1]), np.amax(frb[2]), np.amax(frb[3]), np.amax(frb[4]))
ColorBarMin = min(np.amin(frb[0]), np.amin(frb[1]), np.amin(frb[2]), np.amin(frb[3]), np.amin(frb[4]))


# Matplolib
######################################################

font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 30}

WidthRatio0 = WindowWidth0*WindowWidth/WindowHeight0 
WidthRatio1 = WindowWidth
WidthRatio2 = WindowWidth
WidthRatio3 = WindowWidth
WidthRatio4 = WindowWidth
WidthRatio5 = 0.2*WindowWidth

# The amount of width/height reserved for space between subplots,
# expressed as a fraction of the average axis width/height
wspace = 0.05
hspace = 0.05

WithRatio=[WidthRatio0, WidthRatio1, WidthRatio2, WidthRatio3, WidthRatio4, WidthRatio5]

Sum_wspace = 5*wspace*sum(WithRatio)/6
Sum_hspace = 4*hspace

FigSize_X = sum(WithRatio)*FigSize + Sum_wspace
FigSize_Y = WindowHeight*FigSize + Sum_hspace

fig = plt.figure(figsize=( FigSize_X , FigSize_Y ), constrained_layout=False)


gs = fig.add_gridspec(1,6,wspace=wspace, hspace=hspace, width_ratios=WithRatio)


ax = fig.add_subplot(gs[0, 0])
im = ax.imshow(frb[0], cmap=CMap, norm=norm, aspect=aspect, extent=Extent[0], vmax=ColorBarMax, vmin=ColorBarMin )
ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])

for i,a in zip(range(1,5),ascii_uppercase):
  ax = fig.add_subplot(gs[0,i])
  im = ax.imshow(frb[i], cmap=CMap, norm=norm, aspect=aspect,  extent=Extent[i], vmax=ColorBarMax, vmin=ColorBarMin )
  ax.get_xaxis().set_ticks([])
  ax.get_yaxis().set_ticks([])
  ax.text(0.05,0.95,a,horizontalalignment='left',verticalalignment='top',transform=ax.transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )


 
# Colorbar
ax5 = fig.add_subplot(gs[0, 5])
cbar = fig.colorbar(im,cax=ax5, use_gridspec=True)
cbar.ax.tick_params(labelsize=30, color='k', direction='in', which='both')


#plt.show()
plt.savefig( FileOut+".eps", bbox_inches='tight', pad_inches=0.05, format='eps',dpi=800 )
