import derived_field as df

def ChooseUnit ( Field):

  unit =  ""
  function = ""
  
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
  if Field == 'Bernoulli_constant_1':
      unit = ''
      function = df._Bernoulli_const_1
  if Field == 'spherical_radial_4velocity':
      unit = ''
      function = df._spherical_radial_4velocity
  if Field == 'cylindrical_radial_4velocity':
      unit = ''
      function = df._cylindrical_radial_4velocity
  if Field == 'cylindrical_radial_Mach_number':
      unit = ''
      function = df._cylindrical_radial_Mach_number
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
  if Field == 'UserDefined':
      unit = ''
      function = df._UserDefined
 
  return function, unit 
