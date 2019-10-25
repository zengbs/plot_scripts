import numpy as np
from yt.units import G, kboltz, c, mp, qp


global ds1, ds2, ds

#ds = ds1
#ds = ds2

eV  = 1.6021766208e-12
keV = 1.0e3*eV
GeV = 1.0e9*eV

#UNIT_L = ds["Unit_L"]*ds.length_unit
#UNIT_V = ds["Unit_V"]*ds.length_unit/ds.time_unit
#UNIT_M = ds["Unit_M"]*ds.mass_unit
#UNIT_D = ds["Unit_D"]*ds.mass_unit*ds.length_unit**-3
#UNIT_T = ds["Unit_T"]*ds.time_unit




def _temperature_sr(field, data):
    Temp = data["Temp"]
    Temp *= ( mp * c**2 / kboltz )
    return Temp

def _gravitational_potential(field, data):
    return data["Pote"]

def _pressure_sr( field, data ):
    Temp = data["Temp"]
    Temp *= ( mp * c**2 / kboltz )

    eta = kboltz * Temp / ( mp * c**2 )

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)

    h = h_c2 * c**2

    Ux = data["MomX"]*c**2/(data["Dens"]*h)
    Uy = data["MomY"]*c**2/(data["Dens"]*h)
    Uz = data["MomZ"]*c**2/(data["Dens"]*h)
    Lorentz_factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
    rho = data["Dens"]/Lorentz_factor

    pres = rho * Temp * kboltz
    pres *= 1.0 / mp
    return pres

def _proper_mass_density( field, data ):
    #ds = ds1
    #ds = ds2
    Temp = data["Temp"]
    Temp *= ( mp * c**2 / kboltz )

    eta = kboltz * Temp / ( mp * c**2 )

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)

    h = h_c2 * c**2

    Ux = data["MomX"]*c**2/(data["Dens"]*h)
    Uy = data["MomY"]*c**2/(data["Dens"]*h)
    Uz = data["MomZ"]*c**2/(data["Dens"]*h)
    Lorentz_factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
    n = data["Dens"]/Lorentz_factor
    return n

def _lorentz_factor( field, data ):
    Ux = data["4_velocity_x"]
    Uy = data["4_velocity_y"]
    Uz = data["4_velocity_z"]
    factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
    return factor

def _4_velocity_x( field, data ):
    Temp = data["Temp"]
    Temp *= ( mp * c**2 / kboltz )

    eta = kboltz * Temp / ( mp * c**2 )

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)

    h = h_c2 * c**2

    Ux = data["MomX"]*c**2/(data["Dens"]*h)
    return Ux


def _4_velocity_y( field, data ):
   h=data["specific_enthalpy_sr"]
   Uy = data["MomY"]*c**2/(data["Dens"]*h)
   return Uy

def _4_velocity_z( field, data ):
    h=data["specific_enthalpy_sr"]
    Uz = data["MomZ"]*c**2/(data["Dens"]*h)
    return Uz

def _specific_enthalpy_sr( field, data ):
    Temp = data["temperature_sr"]
    eta = kboltz * Temp / ( mp * c**2 )

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)

    h = h_c2 * c**2

    return h

def _enthalpy_density_sr( field, data ):
    h=data["specific_enthalpy_sr"]
    n = data["Dens"]/data["Lorentz_factor"]
    return h*n

def _mass_density_sr(field, data):
   return data["Dens"]


def _thermal_energy_density_sr( field, data ):
   h=data["specific_enthalpy_sr"]
   n=data["proper_mass_density"]
   p=data["pressure_sr"]
   ThermalEngyDens = n*m*h-p-n*mp*c**2
   return ThermalEngyDens

def _internal_energy_density_sr( field, data ):
   h=data["specific_enthalpy_sr"]
   n=data["proper_mass_density"]
   InternalEngyDens = n*m*h-p
   return InternalEngyDens

def _kinetic_energy_density_sr(field, data):
   h=data["specific_enthalpy_sr"]
   P = data["pressure_sr"]
   factor = data["Lorentz_factor"] 
   kinetic_energy_density = ( data["Dens"] * h + P ) * ( factor - 1.0 )
   return kinetic_energy_density

def _Bernoulli_const( field, data ):
   h=data["specific_enthalpy_sr"]
   factor = data["Lorentz_factor"]
   BernpulliConst = factor * h
   return BernpulliConst

def _spherical_radial_4velocity(field, data):
   Ux = data["4_velocity_x"] 
   Uy = data["4_velocity_y"]
   Uz = data["4_velocity_z"]
   center = data.get_field_parameter('center')
   x_uni = data["x"] - center[0]
   y_uni = data["y"] - center[1]
   z_uni = data["z"] - center[2]
   r = np.sqrt(x_uni**2+y_uni**2+z_uni**2)
   x_uni /= r
   y_uni /= r
   z_uni /= r
   return Ux*x_uni + Uy*y_uni + Uz*z_uni

# symmetry axis: x
def _cylindrical_radial_4velocity(field, data):
   Ux = data["4_velocity_x"] 
   Uy = data["4_velocity_y"]
   Uz = data["4_velocity_z"]
   center = data.get_field_parameter('center')
   y_uni = data["y"] - center[1]
   z_uni = data["z"] - center[2]
   rho = np.sqrt( y_uni**2 + z_uni**2 )
   y_uni /= rho
   z_uni /= rho
   return Uy*y_uni + Uz*z_uni

def _3_velocity_x( field, data ):
   Ux = data["4_velocity_x"] 
   factor = data["Lorentz_factor"]
   Vx = Ux / factor
   return Vx

def _3_velocity_y( field, data ):
   Uy = data["4_velocity_y"] 
   factor = data["Lorentz_factor"]
   Vy = Uy / factor
   return Vy

def _3_velocity_z( field, data ):
   Uz = data["4_velocity_z"] 
   factor = data["Lorentz_factor"]
   Vz = Uz / factor
   return Vz

def _3_velocity_magnitude( field, data ):
   Ux = data["4_velocity_x"] 
   Uy = data["4_velocity_y"] 
   Uz = data["4_velocity_z"] 
   factor = data["Lorentz_factor"]
   Vx = Ux / factor
   Vy = Uy / factor
   Vz = Uz / factor
   V = np.sqrt( Vx**2.0 + Vy**2.0 + Vz**2.0 )
   return V

def _Cp_per_particle( field, data ): 
   if   ds["EoS"] == 2:
     Cp = data["Gamma"] / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     temp = data["temperature_sr"]
     Cp = 2.50 + 2.25 * data["temperature_sr"]*kboltz / np.sqrt( 2.25 * (kboltz*data["temperature_sr"])**2 + (mp*c**2)**2 )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   Cp *= kboltz
   return Cp


def _Cv_per_particle( field, data ): 
   if   ds["EoS"] == 2:
     Cv = 1.0 / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     temp = data["temperature_sr"]
     Cv = 1.50 + 2.25 * data["temperature_sr"]*kboltz / np.sqrt( 2.25 * (kboltz*data["temperature_sr"])**2 + (mp*c**2)**2 )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   Cv *= kboltz
   return Cv

def _Cp_per_volume( field, data ): 
   Cp = data["Cp_per_particle"]
   Cp /= data["proper_mass_density"]
   Cp *= mp
   return Cp


def _Cv_per_volume( field, data ): 
   Cv = data["Cv_per_particle"]
   Cv /= data["proper_mass_density"]
   Cv *= mp
   return Cv

def _Adiabatic_Index( field, data ):
   Cp = data["Cp_per_particle"]
   Cv = data["Cv_per_particle"]
   return Cp / ( Cp - 1.0 )
  
def _entropy_per_particle(field, data):
   if   ds["EoS"] == 2:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   elif ds["EoS"] == 1:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
     T1=1.0
     n1=2.0
     A1=1.5*T1+np.sqrt(2.25*T1**2+1.0)
     T2=data["temperature_sr"]
     n2=data["proper_mass_density"] * ds.length_unit**3
     A2=1.5*T2+np.sqrt(2.25*T2**2+1.0)
     delta_s=1.5*np.log(T2/T1) + 1.5*np.log(A2/A1) - np.log(n2/n1)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return delta_s
   
 
def _sound_speed (field, data):
   h=data["specific_enthalpy_sr"]
   ratio = data["pressure_sr"] / (h*data["proper_mass_density"])
   if ds["EoS"] == 2:
     Cs_sq = data["Gamma"] * ratio
   elif ds["EoS"] == 1:
     Cs_sq = ( ratio / 3.0 ) * ( ( 5.0 - 8.0 * ratio ) / ( 1.0 - ratio ) )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   Cs = np.sqrt(Cs_sq)
   Cs *= c
   return Cs

def _4_sound_speed (field, data):
   h=data["specific_enthalpy_sr"]
   ratio = data["pressure_sr"] / (h*data["proper_mass_density"])
   if ds["EoS"] == 2:
     Cs_sq = data["Gamma"] * ratio
   elif ds["EoS"] == 1:
     Cs_sq = ( ratio / 3.0 ) * ( ( 5.0 - 8.0 * ratio ) / ( 1.0 - ratio ) )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   Cs = np.sqrt(Cs_sq / (1.0-Cs_sq) )
   Cs *= c
   return Cs


def _Mach_number_x_sr (field, data):
   h=data["specific_enthalpy_sr"]
   Ux = data["4_velocity_x"]
   four_Cs = data["4_sound_speed"]
   return Ux / four_Cs

def _Mach_number_y_sr (field, data):
   h=data["specific_enthalpy_sr"]
   Uy = data["4_velocity_y"]
   four_Cs = data["4_sound_speed"]
   return Uy / four_Cs

def _Mach_number_z_sr (field, data):
   h=data["specific_enthalpy_sr"]
   Uz = data["4_velocity_z"]
   four_Cs = data["4_sound_speed"]
   return Uz / four_Cs

def _threshold (field, data):
   h=data["specific_enthalpy_sr"]
   Ux = data["4_velocity_x"] 
   Uy = data["4_velocity_y"]
   Uz = data["4_velocity_z"]
   LorentzFactor = data["Lorentz_factor"]
#   Ur = data["cylindrical_radial_4velocity"]
#   return np.where( (LorentzFactor>10.0) & (Ur > .00),1.0, 0.0 )
   return np.where( (LorentzFactor>25.0), 1.0, 0.0 )


def _synchrotron_emissivity( field, data ):
   global theta, phi, normal

#  number density ratio between non-thermal particles to thermal particles
   e1=1e-3
#  energy density ratio between non-thermal particles to thermal particles
   e2=1.0
#  energy density ratio between magneticity and thermal particles
   eB=1e-3
#  ratio of the maximum and minimum non-thermal energy
   C=1e3
#  power-law index ( p != 2.0)
   p=2.1

#  internal energy density of fluid
   h=data["specific_enthalpy_sr"]
   n=data["proper_mass_density"] * ds.length_unit**3
   InternalEngyDens = n * h - data["pressure_sr"] * ( ds.length_unit * ds.time_unit**2 ) / ds.mass_unit

#  normalization constant for power law distribution
   A=( (e2*InternalEngyDens*(p-2.0)) / (1.0-C**(2.0-p)) )**(p-1.0)
   B=(              (1.0-C**(1.0-p)) / (e1*n*(p-1.0))   )**(p-2.0)
   N0=A/B

#  magnetic energy density
   uB = eB*InternalEngyDens

#  magnitude of magnetic field
   B= np.sqrt(8.0*np.pi*uB)

#  critical frequency / Lorentz factor (TBD!)
   Nu0=B

#  observed frequency
   Nu= 1.0

#  emissivity
   j=N0*uB* ( Nu0**(-1.5+0.5*p) ) * (1.0-data["Lorentz_factor"]**-2) * Nu**(0.5-0.5*p)
#   v = data["3_velocity_magnitude"] * ds.time_unit / ds.length_unit
#   j=N0*uB* ( Nu0**(-1.5+0.5*p) ) * Nu**(0.5-0.5*p) * (0.5*np.tanh( 10*v-7 )+0.5)

#  beaming factor
   Ux = data["4_velocity_x"] 
   Uy = data["4_velocity_y"]
   Uz = data["4_velocity_z"]
   Var = data["Lorentz_factor"] - (Ux*normal[0]+Uy*normal[1]+Uz*normal[2])*(ds.time_unit/ds.length_unit)
   BeamingFactor = Var**-2.0

   return j * BeamingFactor*( ds.mass_unit ) / ( ds.length_unit * ds.time_unit**2 )
