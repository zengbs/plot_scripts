import numpy as np

global ds


def _temperature_sr(field, data):
    return data["Temp"]

def _pressure_sr( field, data ):
   pres = data["proper_number_density"] * data["Temp"]
   return pres*ds.mass_unit*ds.length_unit**2/(ds.time_unit**2)

def _proper_number_density( field, data ):
   n = data["Dens"]/data["Lorentz_factor"]
   return n / ds.mass_unit

def _lorentz_factor( field, data ):
   h=data["specific_enthalpy_sr"]
   Ux = data["4_velocity_x"]
   Uy = data["4_velocity_y"]
   Uz = data["4_velocity_z"]
   factor = np.sqrt(1*(ds.length_unit/ds.time_unit)**2 + Ux**2 + Uy**2 + Uz**2)
   return factor*(ds.time_unit/ds.length_unit)

def _4_velocity_x( field, data ):
   h=data["specific_enthalpy_sr"]
   Ux = data["MomX"]/(data["Dens"]*h)
   return Ux


def _4_velocity_y( field, data ):
   h=data["specific_enthalpy_sr"]
   Uy = data["MomY"]/(data["Dens"]*h)
   return Uy

def _4_velocity_z( field, data ):
   h=data["specific_enthalpy_sr"]
   Uz = data["MomZ"]/(data["Dens"]*h)
   return Uz

def _specific_enthalpy_sr( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + data["Gamma"] * data["Temp"] / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return h

def _enthalpy_density_sr( field, data ):
   h=data["specific_enthalpy_sr"]
   n = data["Dens"]/data["Lorentz_factor"]
   return h*n

def _number_density_sr(field, data):
   return data["Dens"]/ds.mass_unit


def _thermal_energy_density_sr( field, data ):
   h=data["specific_enthalpy_sr"]
   n=data["proper_number_density"]
   ThermalEngyDens = n * (h - 1.0 ) * ( ds.mass_unit ) * ( ds.length_unit / ds.time_unit )**2 - data["pressure_sr"]
   return ThermalEngyDens

def _internal_energy_density_sr( field, data ):
   h=data["specific_enthalpy_sr"]
   n=data["proper_number_density"]
   InternalEngyDens = n * h * ( ds.mass_unit ) * ( ds.length_unit / ds.time_unit )**2 - data["pressure_sr"]
   return InternalEngyDens

def _kinetic_energy_density_sr(field, data):
   h=data["specific_enthalpy_sr"]
   P = data["pressure_sr"]
   factor = data["Lorentz_factor"] 
   kinetic_energy_density = ( data["Dens"] * h * ( ds.length_unit / ds.time_unit )**2 + P ) * ( factor - 1.0 )
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
   x_hat = data["x"] - center[0]
   y_hat = data["y"] - center[1]
   z_hat = data["z"] - center[2]
   r = np.sqrt(x_hat**2+y_hat**2+z_hat**2)
   x_hat /= r
   y_hat /= r
   z_hat /= r
   return Ux*x_hat + Uy*y_hat + Uz*z_hat

# symmetry axis: x
def _cylindrical_radial_4velocity(field, data):
   Ux = data["4_velocity_x"] 
   Uy = data["4_velocity_y"]
   Uz = data["4_velocity_z"]
   center = data.get_field_parameter('center')
   y_hat = data["y"] - center[1]
   z_hat = data["z"] - center[2]
   rho = np.sqrt( y_hat**2 + z_hat**2 )
   y_hat /= rho
   z_hat /= rho
   return Uy*y_hat + Uz*z_hat

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
     temp = data["Temp"]
     Cp = 2.50 + 2.25 * data["Temp"] / np.sqrt( 2.25 * data["Temp"]**2 + 1.0 )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return Cp


def _Cv_per_particle( field, data ): 
   if   ds["EoS"] == 2:
     Cv = 1.0 / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     temp = data["Temp"]
     Cv = 1.50 + 2.25 * data["Temp"] / np.sqrt( 2.25 * data["Temp"]**2 + 1.0 )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return Cv

def _Cp_per_volume( field, data ): 
   if   ds["EoS"] == 2:
     Cp = data["Gamma"] / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     temp = data["Temp"]
     Cp = 2.50 + 2.25 * data["Temp"] / np.sqrt( 2.25 * data["Temp"]**2 + 1.0 )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return Cp / data["proper_number_density"]


def _Cv_per_volume( field, data ): 
   if   ds["EoS"] == 2:
     Cv = 1.0 / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     temp = data["Temp"]
     Cv = 1.50 + 2.25 * data["Temp"] / np.sqrt( 2.25 * data["Temp"]**2 + 1.0 )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return Cv / data["proper_number_density"]

def _Adiabatic_Index( field, data ):
   if ds["EoS"] == 2:
     Cp = data["Gamma"] / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     temp = data["Temp"]
     Cp = 2.50 + 2.25 * data["Temp"] / np.sqrt( 2.25 * data["Temp"]**2 + 1.0 )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return Cp / ( Cp - 1.0 )
  
def _entropy_per_particle(field, data):
   if   ds["EoS"] == 2:
     print ("Your EoS doesn't support yet!")
   elif ds["EoS"] == 1:
     T1=1.0
     n1=2.0
     A1=1.5*T1+np.sqrt(2.25*T1**2+1.0)
     T2=data["Temp"]
     n2=data["proper_number_density"] * ds.length_unit**3
     A2=1.5*T2+np.sqrt(2.25*T2**2+1.0)
     delta_s=1.5*np.log(T2/T1) + 1.5*np.log(A2/A1) - np.log(n2/n1)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return delta_s
   
 
def _sound_speed (field, data):
   h=data["specific_enthalpy_sr"]
   ratio = data["Temp"] / h
   if ds["EoS"] == 2:
     Cs_sq = data["Gamma"] * ratio
   elif ds["EoS"] == 1:
     Cs_sq = ( ratio / 3.0 ) * ( ( 5.0 - 8.0 * ratio ) / ( 1.0 - ratio ) )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return np.sqrt(Cs_sq) * (ds.length_unit/ds.time_unit)

def _4_sound_speed (field, data):
   h=data["specific_enthalpy_sr"]
   ratio = data["Temp"] / h
   if ds["EoS"] == 2:
     Cs_sq = data["Gamma"] * ratio
   elif ds["EoS"] == 1:
     Cs_sq = ( ratio / 3.0 ) * ( ( 5.0 - 8.0 * ratio ) / ( 1.0 - ratio ) )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return np.sqrt(Cs_sq / (1.0-Cs_sq) )


def _Mach_number_x_sr (field, data):
   h=data["specific_enthalpy_sr"]
   Ux = data["MomX"]/(data["Dens"]*h)
   four_Cs = data["4_sound_speed"]
   return ( Ux / four_Cs ) * (ds.time_unit/ds.length_unit)

def _Mach_number_y_sr (field, data):
   h=data["specific_enthalpy_sr"]
   Uy = data["MomY"]/(data["Dens"]*h)
   four_Cs = data["4_sound_speed"]
   return ( Uy / four_Cs ) * (ds.time_unit/ds.length_unit) 

def _Mach_number_z_sr (field, data):
   h=data["specific_enthalpy_sr"]
   Uz = data["MomZ"]/(data["Dens"]*h)
   four_Cs = data["4_sound_speed"]
   return ( Uz / four_Cs ) * (ds.time_unit/ds.length_unit) 

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
   n=data["proper_number_density"] * ds.length_unit**3
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
