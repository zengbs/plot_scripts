import numpy as np
import math
import re
from yt.units import G, kboltz, c, mp, qp, eV
from __main__ import *


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
    Temp *= ( mp * c**2  )
    return Temp

def _gravitational_potential(field, data):
    return data["Pote"]

def _pressure_sr( field, data ):
    #ds = ds1
    #ds = ds2
    Temp = data["Temp"]
    eta = Temp

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)


    Ux = data["MomX"]/(data["Dens"]*h_c2)
    Uy = data["MomY"]/(data["Dens"]*h_c2)
    Uz = data["MomZ"]/(data["Dens"]*h_c2)
    Lorentz_factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
    rho = data["Dens"]/Lorentz_factor

    pres = rho * eta * c**2
    return pres/normalconst

def _proper_mass_density( field, data ):
    #ds = ds1
    #ds = ds2
    Temp = data["Temp"]

    eta = Temp

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)


    Ux = data["MomX"]/(data["Dens"]*h_c2)
    Uy = data["MomY"]/(data["Dens"]*h_c2)
    Uz = data["MomZ"]/(data["Dens"]*h_c2)
    Lorentz_factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
    n = data["Dens"]/Lorentz_factor
    return n/normalconst

def _lorentz_factor( field, data ):
    Temp = data["Temp"]

    eta = Temp

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)


    Ux = data["MomX"]/(data["Dens"]*h_c2)
    Uy = data["MomY"]/(data["Dens"]*h_c2)
    Uz = data["MomZ"]/(data["Dens"]*h_c2)
    Lorentz_factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
    return Lorentz_factor

def _lorentz_factor_1( field, data ):
    Temp = data["Temp"]

    eta = Temp

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)


    Ux = data["MomX"]/(data["Dens"]*h_c2)
    Uy = data["MomY"]/(data["Dens"]*h_c2)
    Uz = data["MomZ"]/(data["Dens"]*h_c2)
    Usqr = (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2
    Lorentz_factor = np.sqrt(1 + Usqr)
    return Usqr / ( Lorentz_factor + 1 )

def _4_velocity_x( field, data ):
    Temp = data["Temp"]
    eta = Temp

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)


    Ux = data["MomX"]/(data["Dens"]*h_c2)
    return Ux


def _4_velocity_y( field, data ):
    Temp = data["Temp"]
    eta = Temp

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)


    Uy = data["MomY"]/(data["Dens"]*h_c2)
    return Uy


def _4_velocity_z( field, data ):
    Temp = data["Temp"]
    eta = Temp

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)


    Uz = data["MomZ"]/(data["Dens"]*h_c2)
    return Uz


def _specific_enthalpy_sr( field, data ):
    Temp = data["Temp"]
    eta = Temp

    if ds["EoS"] == 2:
      h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
    elif ds["EoS"] == 1:
      h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
      print ("Your EoS doesn't support yet!")
      sys.exit(0)

    h = h_c2 * c**2

    return h/normalconst

def _enthalpy_density_sr( field, data ):
    h=data["specific_enthalpy_sr"]
    n = data["Dens"]/data["Lorentz_factor"]
    return h*n/normalconst

def _mass_density_sr(field, data):
   return data["Dens"]/normalconst


def _thermal_energy_density_sr( field, data ):
   h=data["specific_enthalpy_sr"]
   n=data["proper_mass_density"]
   p=data["pressure_sr"]
   ThermalEngyDens = n*m*h-p-n*mp*c**2
   return ThermalEngyDens/normalconst

def _internal_energy_density_sr( field, data ):
   h=data["specific_enthalpy_sr"]
   n=data["proper_mass_density"]
   InternalEngyDens = n*m*h-p
   return InternalEngyDens/normalconst

def _kinetic_energy_density_sr(field, data):
   h=data["specific_enthalpy_sr"]
   P = data["pressure_sr"]
   factor = data["Lorentz_factor"] 
   kinetic_energy_density = ( data["Dens"] * h + P ) * ( factor - 1.0 )
   return kinetic_energy_density/normalconst

def _Bernoulli_const( field, data ):
   Temp = data["Temp"]
   eta = Temp

   if ds["EoS"] == 2:
     h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)

   h = h_c2 * c**2

   Ux = data["MomX"]/(data["Dens"]*h_c2)
   Uy = data["MomY"]/(data["Dens"]*h_c2)
   Uz = data["MomZ"]/(data["Dens"]*h_c2)
   Lorentz_factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)

   BernpulliConst = Lorentz_factor * h
   return BernpulliConst/normalconst

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
   eta = data["Temp"]

   if ds["EoS"] == 2:
     h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)


   Ux = data["MomX"]/(data["Dens"]*h_c2)
   Uy = data["MomY"]/(data["Dens"]*h_c2)
   Uz = data["MomZ"]/(data["Dens"]*h_c2)
   factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
   Vx = Ux / factor
   return Vx

def _3_velocity_y( field, data ):
   eta = data["Temp"]

   if ds["EoS"] == 2:
     h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)


   Ux = data["MomX"]/(data["Dens"]*h_c2)
   Uy = data["MomY"]/(data["Dens"]*h_c2)
   Uz = data["MomZ"]/(data["Dens"]*h_c2)
   factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
   Vy = Uy / factor
   return Vy

def _3_velocity_z( field, data ):
   eta = data["Temp"]

   if ds["EoS"] == 2:
     h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)


   Ux = data["MomX"]/(data["Dens"]*h_c2)
   Uy = data["MomY"]/(data["Dens"]*h_c2)
   Uz = data["MomZ"]/(data["Dens"]*h_c2)
   factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
   Vz = Uz / factor
   return Vz

def _3_velocity_magnitude( field, data ):
   eta = data["Temp"]

   if ds["EoS"] == 2:
     h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)


   Ux = data["MomX"]/(data["Dens"]*h_c2)
   Uy = data["MomY"]/(data["Dens"]*h_c2)
   Uz = data["MomZ"]/(data["Dens"]*h_c2)
   factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)
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
   Cp *= kboltz
   return Cp/normalconst


def _Cv_per_particle( field, data ): 
   if   ds["EoS"] == 2:
     Cv = 1.0 / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     temp = data["Temp"]
     Cv = 1.50 + 2.25 * data["Temp"] / np.sqrt( 2.25 * data["Temp"]**2 + 1.0 )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   Cv *= kboltz
   return Cv/normalconst

def _Cp_per_volume( field, data ): 
   Cp = data["Cp_per_particle"]
   Cp /= data["proper_mass_density"]
   Cp *= mp
   return Cp/normalconst


def _Cv_per_volume( field, data ): 
   Cv = data["Cv_per_particle"]
   Cv /= data["proper_mass_density"]
   Cv *= mp
   return Cv/normalconst

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
     T2=data["Temp"]
     n2=data["proper_mass_density"] * ds.length_unit**3
     A2=1.5*T2+np.sqrt(2.25*T2**2+1.0)
     delta_s=1.5*np.log(T2/T1) + 1.5*np.log(A2/A1) - np.log(n2/n1)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)
   return delta_s/normalconst
   
 
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


def _Mach_number_sr (field, data):
   Temp = data["Temp"]
   eta = Temp


   if ds["EoS"] == 2:
     h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)


   Ux = data["MomX"]/(data["Dens"]*h_c2)
   Uy = data["MomY"]/(data["Dens"]*h_c2)
   Uz = data["MomZ"]/(data["Dens"]*h_c2)

   ratio = eta / h_c2

   if ds["EoS"] == 2:
     Cs_sq = data["Gamma"] * ratio
   elif ds["EoS"] == 1:
     Cs_sq = ( ratio / 3.0 ) * ( ( 5.0 - 8.0 * ratio ) / ( 1.0 - ratio ) )
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)

   Cs = np.sqrt(Cs_sq / (1.0-Cs_sq) )
   Cs *= c

   return np.sqrt (Ux**2 + Uy**2 + Uz**2 ) / Cs


def _threshold (field, data):
   h=data["specific_enthalpy_sr"]
   Ux = data["4_velocity_x"] 
   Uy = data["4_velocity_y"]
   Uz = data["4_velocity_z"]
   LorentzFactor = data["Lorentz_factor"]
#   Ur = data["cylindrical_radial_4velocity"]
#   return np.where( (LorentzFactor>10.0) & (Ur > .00),1.0, 0.0 )
   return np.where( (LorentzFactor>25.0), 1.0, 0.0 )


def _emissivity( field, data ):
   global theta, phi, normal

   fp = open('Input__TestProb', "r")
   for line in iter(fp):                                      
      if ( line[0:10:1] == "Jet_SrcVel" ):                   
         FourVelocity_Src = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", line)[0]
         FourVelocity_Src = float(FourVelocity_Src)
   fp.close()        

   Gamma_Src = np.sqrt( 1.0 + FourVelocity_Src**2 )

   Gamma_Src_1 = FourVelocity_Src**2 / ( 1.0 + Gamma_Src )

#  specific enthalpy
   Temp = data["Temp"]
   eta = Temp

   if ds["EoS"] == 2:
     h_c2 = 1.0 + data["Gamma"] * eta / ( data["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
     sys.exit(0)


#  proper mass density
   Ux = data["MomX"]/(data["Dens"]*h_c2)
   Uy = data["MomY"]/(data["Dens"]*h_c2)
   Uz = data["MomZ"]/(data["Dens"]*h_c2)
   
   Lorentz_factor = np.sqrt(1 + (Ux/c)**2 + (Uy/c)**2 + (Uz/c)**2)

   rho = data["Dens"]/Lorentz_factor

#  pressure
   pres = rho * eta * c**2

#  synchrotron emission
   if ( emission == "synchrotron" ):
     j = pres**2 * np.tanh(eta/Gamma_Src_1)**2
     j *= ds.length_unit * ds.time_unit**7/ ds.mass_unit
   if ( emission == "NR_thermal_Bremss_per_freq" ):
     n = data["Dens"]/Lorentz_factor
     kT = eta * mp * c**2 / (1e3*eV)

     freq1=freq.split(',')
     freq1 = np.asarray(freq1)
     freq1=freq1.astype(np.float)

     sum_exp = 0.0

     for f in freq1:
        idx = np.where(freq1==f)
        sum_exp += np.exp(-freq1[idx]/kT)

     j = (n**2) * (eta**-0.5 ) * sum_exp
     j *= ds.length_unit **5 * ds.time_unit**2 / ds.mass_unit
   if ( emission == "NR_thermal_Bremss_all_freq" ):
     n = data["Dens"]/Lorentz_factor
     j = (n**2) * (eta**+0.5 )
     j *= ds.length_unit **5 * ds.time_unit**3 / ds.mass_unit


#  beaming factor
   Var = Lorentz_factor - (Ux*normal[0]+Uy*normal[1]+Uz*normal[2]) / c
   BeamingFactor = Var**-2.0

   return j * BeamingFactor
