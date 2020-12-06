import numpy as np
import math
import re
from yt.units import gravitational_constant_cgs,\
    speed_of_light_cgs,        \
    charge_proton_cgs,         \
    eV,                        \
    boltzmann_constant_cgs,    \
    mass_hydrogen_cgs,         \
    planck_constant_cgs
import sys

eV = 1.6021766208e-12
keV = 1.0e3*eV
GeV = 1.0e9*eV


def _unit (data):
  if data.ds["Opt__Unit"] == 1:
     unit_l = data.ds.length_unit
     unit_v = speed_of_light_cgs
     unit_m = data.ds.mass_unit
     unit_d = data.ds.mass_unit*data.ds.length_unit**-3
     unit_t = data.ds.length_unit/speed_of_light_cgs
  else:
     unit_l = data.ds.length_unit
     unit_v = data.ds.length_unit/data.ds.time_unit
     unit_m = data.ds.mass_unit
     unit_d = data.ds.mass_unit*data.ds.length_unit**-3
     unit_t = data.ds.time_unit

  return unit_l, unit_v, unit_m, unit_d, unit_t


def _mass_density_sr(field, data):
    return data["Dens"]


def _specific_enthalpy_sr(field, data):
    eta = data["Temp"]
    if data.ds["EoS"] == 2:
        h_c2 = 1.0 + data.ds["Gamma"] * eta / (data.ds["Gamma"] - 1.0)
    elif data.ds["EoS"] == 1:
        h_c2 = 2.5*eta+np.sqrt(2.25*eta**2+1.0)
    else:
        print("Your EoS doesn't support yet!")
        sys.exit(0)
    return h_c2

def _specific_enthalpy_1_sr(field, data):
    eta = data["Temp"]
    if data.ds["EoS"] == 2:
        h_c2_1 = data.ds["Gamma"] * eta / (data.ds["Gamma"] - 1.0)
    elif data.ds["EoS"] == 1:
        h_c2_1 = ( 2.5*eta + 2.25*eta**2 ) / ( 1 + np.sqrt( 1 + 2.25*eta**2 ) )
    else:
        print("Your EoS doesn't support yet!")
        sys.exit(0)
    return h_c2_1


def _temperature_sr(field, data):
    Temp = data["Temp"]
    return Temp


def _gravitational_potential(field, data):
    return data["Pote"]


def _pressure_sr(field, data):
    from __main__ import NormalizedConst_Dens, NormalizedConst_Pres
    See  = NormalizedConst_Pres > 0
    See |= NormalizedConst_Dens > 0
    if ( not See ):
       print( "NormalizedConst_Dens=%e, NormalizedConst_Pres=%e" % ( NormalizedConst_Dens, NormalizedConst_Pres ) )
       exit(0)
    eta = data["Temp"]
    rho = _proper_mass_density("", data)*NormalizedConst_Dens
    pres = rho * eta
    return pres/NormalizedConst_Pres


def _proper_mass_density(field, data):
    from __main__ import NormalizedConst_Dens, NormalizedConst_Pres
    See  = NormalizedConst_Pres > 0
    See |= NormalizedConst_Dens > 0
    if ( not See ):
       print( "NormalizedConst_Dens=%e, NormalizedConst_Pres=%e" % ( NormalizedConst_Dens, NormalizedConst_Pres ) )
       exit(0)
    Lorentz_factor = _lorentz_factor("", data)
    rho = data["Dens"]/Lorentz_factor
    return rho/NormalizedConst_Dens


def _lorentz_factor(field, data):
    Ux = _4_velocity_x("", data)
    Uy = _4_velocity_y("", data)
    Uz = _4_velocity_z("", data)
    Lorentz_factor = np.sqrt(1 + Ux**2 + Uy**2 + Uz**2)
    return Lorentz_factor


def _lorentz_factor_1(field, data):
    Ux = _4_velocity_x("", data)
    Uy = _4_velocity_y("", data)
    Uz = _4_velocity_z("", data)
    Usqr = Ux**2 + Uy**2 + Uz**2
    Lorentz_factor = np.sqrt(1 + Usqr)
    return Usqr / (Lorentz_factor + 1)


def _4_velocity_x(field, data):
    h_c2 = _specific_enthalpy_sr("", data)
    Ux = data["MomX"]/(data["Dens"]*h_c2)
    if data.ds["Opt__Unit"] == 0:
      return Ux*data.ds.time_unit/data.ds.length_unit
    else:
      return Ux/speed_of_light_cgs
    #return Ux/UNIT_V


def _4_velocity_y(field, data):
    h_c2 = _specific_enthalpy_sr("", data)
    Uy = data["MomY"]/(data["Dens"]*h_c2)
    if data.ds["Opt__Unit"] == 0:
      return Uy*data.ds.time_unit/data.ds.length_unit
    else:
      return Uy/speed_of_light_cgs
    #return Uy/UNIT_V


def _4_velocity_z(field, data):
    h_c2 = _specific_enthalpy_sr("", data)
    Uz = data["MomZ"]/(data["Dens"]*h_c2)
    if data.ds["Opt__Unit"] == 0:
      return Uz*data.ds.time_unit/data.ds.length_unit
    else:
      return Uz/speed_of_light_cgs
    #return Uz/UNIT_V


def _Bernoulli_const(field, data):
    from __main__ import NormalizedConst_h_gamma
    Lorentz_factor = _lorentz_factor("", data)
    h_c2 = _specific_enthalpy_sr("", data)
    BernpulliConst = Lorentz_factor * h_c2
    return BernpulliConst/NormalizedConst_h_gamma

def _Bernoulli_const_1(field, data):
    Lorentz_factor = _lorentz_factor("", data)
    h_c2_1 = _specific_enthalpy_1_sr("", data)
    Ux = _4_velocity_x("", data)
    Uy = _4_velocity_y("", data)
    Uz = _4_velocity_z("", data)
    U_mag2 = Ux**2 + Uy**2 + Uz**2
    HTilde = _specific_enthalpy_1_sr("", data)
    return HTilde*Lorentz_factor + U_mag2 / ( Lorentz_factor + 1 )


def _emissivity(field, data):
    global theta, phi, normal

    Gamma_Src = np.sqrt(1.0 + Input__TestProb['Jet_SrcVel']**2)

    Gamma_Src_1 = FourVelocity_Src**2 / (1.0 + Gamma_Src)

    eta = data["Temp"]
    Lorentz_factor = _lorentz_factor("", data)

#  synchrotron
    if (emission == "synchrotron"):
        pres = _pressure_sr("", data)
        j = pres**2
        j *= np.tanh(eta/Gamma_Src_1)**2
        j *= data.ds.length_unit * data.ds.time_unit / data.ds.mass_unit
#  Bremsstrahlung per frequency
    if (emission == "NR_thermal_Bremss_per_freq"):
        rho = data["Dens"]/Lorentz_factor
        kT = eta * mass_hydrogen_cgs * speed_of_light_cgs**2

        freq1 = freq.split(',')
        freq1 = np.asarray(freq1)
        freq1 = freq1.astype(np.float)

        sum_exp = 0.0

        for f in freq1:
            idx = np.where(freq1 == f)
            sum_exp += np.exp(-freq1[idx]*1e3*eV/kT)

        j = ((rho/mass_hydrogen_cgs)**2) * (kT**-0.5) * sum_exp
        j *= (2**5)*(np.pi)*(charge_proton_cgs**6) / \
            (3*mass_hydrogen_cgs*speed_of_light_cgs**3)
        j *= np.sqrt(2*np.pi/(3*mass_hydrogen_cgs))
#  Bremsstrahlung all frequency
    if (emission == "NR_thermal_Bremss_all_freq"):
        rho = data["Dens"]/Lorentz_factor
        kT = eta * mass_hydrogen_cgs * speed_of_light_cgs**2
        j = ((rho/mass_hydrogen_cgs)**2) * (kT**0.5)
        j *= np.sqrt(2*np.pi/(3*mass_hydrogen_cgs))
        j *= 2**5*np.pi*charge_proton_cgs**6 / \
            (3*planck_constant_cgs*mass_hydrogen_cgs*speed_of_light_cgs**3)


#  beaming factor
    Var = Lorentz_factor - \
        (Ux*normal[0]+Uy*normal[1]+Uz*normal[2]) / speed_of_light_cgs
    BeamingFactor = Var**-2.0

    return j * BeamingFactor


def _3_velocity_x(field, data):
    Lorentz_factor = _lorentz_factor("", data)
    Ux = _4_velocity_x("", data)
    Vx = Ux / Lorentz_factor
    return Vx


def _3_velocity_y(field, data):
    Lorentz_factor = _lorentz_factor("", data)
    Uy = _4_velocity_y("", data)
    Vy = Uy / Lorentz_factor
    return Vy


def _3_velocity_z(field, data):
    Lorentz_factor = _lorentz_factor("", data)
    Uz = _4_velocity_z("", data)
    Vz = Uz / Lorentz_factor
    return Vz


def _3_velocity_magnitude(field, data):
    Lorentz_factor = _lorentz_factor("", data)
    Ux = _4_velocity_x("", data)
    Vx = Ux / Lorentz_factor
    Uy = _4_velocity_y("", data)
    Vy = Uy / Lorentz_factor
    Uz = _4_velocity_z("", data)
    Vz = Uz / Lorentz_factor
    V = np.sqrt(Vx**2.0 + Vy**2.0 + Vz**2.0)
    return V


def _spherical_radial_4velocity(field, data):
    center = data.get_field_parameter('center')
    Ux = _4_velocity_x("", data)
    Uy = _4_velocity_y("", data)
    Uz = _4_velocity_z("", data)
    x_uni = data["x"] - center[0]
    y_uni = data["y"] - center[1]
    z_uni = data["z"] - center[2]
    r = np.sqrt(x_uni**2+y_uni**2+z_uni**2)
    x_uni /= r
    y_uni /= r
    z_uni /= r
    return Ux*x_uni + Uy*y_uni + Uz*z_uni


def _cylindrical_radial_4velocity(field, data):
    from __main__ import cylindrical_axis

    center = data.get_field_parameter('center')

    if ( cylindrical_axis == "x" ):
      U1   = _4_velocity_y("", data)
      U2   = _4_velocity_z("", data)
      uni1 = data["y"] - center[1]
      uni2 = data["z"] - center[2]
    if ( cylindrical_axis == "y" ):
      U1   = _4_velocity_x("", data)
      U2   = _4_velocity_z("", data)
      uni1 = data["x"] - center[1]
      uni2 = data["z"] - center[2]
    if ( cylindrical_axis == "z" ):
      U1   = _4_velocity_y("", data)
      U2   = _4_velocity_x("", data)
      uni1 = data["y"] - center[1]
      uni2 = data["x"] - center[2]
    
    rho = np.sqrt(uni1**2 + uni2**2)
    uni1 /= rho
    uni2 /= rho
    return U1*uni1 + U2*uni2


def _cylindrical_radial_Mach_number(field, data):
    from __main__ import cylindrical_axis

    center = data.get_field_parameter('center')

    if ( cylindrical_axis == "x" ):
      U1   = _4_velocity_y("", data)
      U2   = _4_velocity_z("", data)
      uni1 = data["y"] - center[1]
      uni2 = data["z"] - center[2]
    if ( cylindrical_axis == "y" ):
      U1   = _4_velocity_x("", data)
      U2   = _4_velocity_z("", data)
      uni1 = data["x"] - center[1]
      uni2 = data["z"] - center[2]
    if ( cylindrical_axis == "z" ):
      U1   = _4_velocity_y("", data)
      U2   = _4_velocity_x("", data)
      uni1 = data["y"] - center[1]
      uni2 = data["x"] - center[2]
    
    rho = np.sqrt(uni1**2 + uni2**2)
    uni1 /= rho
    uni2 /= rho

    U_R = U1*uni1 + U2*uni2

    U_s = _4_sound_speed("", data)

    return U_R / U_s 



def _sound_speed(field, data):
    Cs_sq = _sound_speed_sqr("", data)
    Cs = np.sqrt(Cs_sq)
    return Cs


def _sound_speed_sqr(field, data):
    h_c2 = _specific_enthalpy_sr("", data)
    eta = data["Temp"]
    ratio = eta / h_c2

    if data.ds["EoS"] == 2:
        Cs_sq = data.ds["Gamma"] * ratio
    elif data.ds["EoS"] == 1:
        Cs_sq = (ratio / 3.0) * ((5.0 - 8.0 * ratio) / (1.0 - ratio))
    else:
        print("Your EoS doesn't support yet!")
        sys.exit(0)
    return Cs_sq


def _4_sound_speed(field, data):
    Cs_sq = _sound_speed_sqr("", data)
    Cs4 = np.sqrt(Cs_sq / (1-Cs_sq))
    return Cs4


def _Mach_number_sr(field, data):
    eta = data["Temp"]
    Ux = _4_velocity_x("", data)
    Uy = _4_velocity_y("", data)
    Uz = _4_velocity_z("", data)
    Cs = np.sqrt(Cs_sq / (1.0-Cs_sq))
    Cs *= speed_of_light_cgs
    Cs4 = _4_sound_speed("", data)
    return np.sqrt(Ux**2 + Uy**2 + Uz**2) / Cs4


def _enthalpy_density_sr(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    h_c2 = _specific_enthalpy_sr("", data)
    rho = data["Dens"]/data["Lorentz_factor"]
    return h*rho/normalconst


def _thermal_energy_density_sr(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    h = data["specific_enthalpy_sr"]
    n = data["proper_mass_density"]
    p = data["pressure_sr"]
    ThermalEngyDens = n*m*h-p-n*mass_hydrogen_cgs*speed_of_light_cgs**2
    return ThermalEngyDens/normalconst


def _internal_energy_density_sr(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    h = data["specific_enthalpy_sr"]
    n = data["proper_mass_density"]
    InternalEngyDens = n*m*h-p
    return InternalEngyDens/normalconst


def _kinetic_energy_density_sr(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    h = data["specific_enthalpy_sr"]
    P = data["pressure_sr"]
    factor = data["Lorentz_factor"]
    kinetic_energy_density = (data["Dens"] * h + P) * (factor - 1.0)
    return kinetic_energy_density/normalconst


def _Cp_per_particle(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    if data.ds["EoS"] == 2:
        Cp = data.ds["Gamma"] / (data.ds["Gamma"] - 1.0)
    elif data.ds["EoS"] == 1:
        temp = data["Temp"]
        Cp = 2.50 + 2.25 * data["Temp"] / np.sqrt(2.25 * data["Temp"]**2 + 1.0)
    else:
        print("Your EoS doesn't support yet!")
        sys.exit(0)
    Cp *= boltzmann_constant_cgs
    return Cp/normalconst


def _Cv_per_particle(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    if data.ds["EoS"] == 2:
        Cv = 1.0 / (data.ds["Gamma"] - 1.0)
    elif data.ds["EoS"] == 1:
        temp = data["Temp"]
        Cv = 1.50 + 2.25 * data["Temp"] / np.sqrt(2.25 * data["Temp"]**2 + 1.0)
    else:
        print("Your EoS doesn't support yet!")
        sys.exit(0)
    Cv *= boltzmann_constant_cgs
    return Cv/normalconst


def _Cp_per_volume(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    Cp = data["Cp_per_particle"]
    Cp /= data["proper_mass_density"]
    Cp *= mass_hydrogen_cgs
    return Cp/normalconst


def _Cv_per_volume(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    Cv = data["Cv_per_particle"]
    Cv /= data["proper_mass_density"]
    Cv *= mass_hydrogen_cgs
    return Cv/normalconst


def _Adiabatic_Index(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    Cp = data["Cp_per_particle"]
    Cv = data["Cv_per_particle"]
    return Cp / (Cp - 1.0)


def _entropy_per_particle(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    if data.ds["EoS"] == 2:
        print("Your EoS doesn't support yet!")
        sys.exit(0)
    elif data.ds["EoS"] == 1:
        print("Your EoS doesn't support yet!")
        sys.exit(0)
        T1 = 1.0
        n1 = 2.0
        A1 = 1.5*T1+np.sqrt(2.25*T1**2+1.0)
        T2 = data["Temp"]
        n2 = data["proper_mass_density"] * data.ds.length_unit**3
        A2 = 1.5*T2+np.sqrt(2.25*T2**2+1.0)
        delta_s = 1.5*np.log(T2/T1) + 1.5*np.log(A2/A1) - np.log(n2/n1)
    else:
        print("Your EoS doesn't support yet!")
        sys.exit(0)
    return delta_s/normalconst


def _threshold(field, data):
    print("doesn't support yet!")
    sys.exit(0)
    h = data["specific_enthalpy_sr"]
    Ux = data["4_velocity_x"]
    Uy = data["4_velocity_y"]
    Uz = data["4_velocity_z"]
    LorentzFactor = data["Lorentz_factor"]
#   Ur = data["cylindrical_radial_4velocity"]
#   return np.where( (LorentzFactor>10.0) & (Ur > .00),1.0, 0.0 )
    return np.where((LorentzFactor > 25.0), 1.0, 0.0)

def _UserDefined(field, data):
    from __main__ import NormalizedConst_h_gamma
    HGamma_1 = _Bernoulli_const_1("",data)
    return np.abs(1-HGamma_1/(NormalizedConst_h_gamma-1))
