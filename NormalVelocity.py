from mpi4py import MPI
import yt
import numpy as np
import derived_field as df
from numpy import linalg as LA
import matplotlib.pyplot as plt
import plyfile
from plyfile import PlyData, PlyElement
import time


df.ds = yt.load('Data_000027')

# start ticking
t0 = time.time()

# add new derived field
df.ds.add_field( ("gamer", 'specific_enthalpy_sr'),function=df._specific_enthalpy_sr, sampling_type="cell", units='' )
df.ds.add_field( ("gamer", '4_velocity_x')        ,function=df._4_velocity_x        , sampling_type="cell", units='code_length/code_time' )
df.ds.add_field( ("gamer", '4_velocity_y')        ,function=df._4_velocity_y        , sampling_type="cell", units='code_length/code_time' )
df.ds.add_field( ("gamer", '4_velocity_z')        ,function=df._4_velocity_z        , sampling_type="cell", units='code_length/code_time' )
df.ds.add_field( ("gamer", 'Lorentz_factor')      ,function=df._lorentz_factor      , sampling_type="cell", units='' )
df.ds.add_field( ("gamer", 'threshold')           ,function=df._threshold           , sampling_type="cell", units='' )
df.ds.add_field( ("gamer", '4_sound_speed')       ,function=df._4_sound_speed       , sampling_type="cell", units='' )
df.ds.add_field( ("gamer", 'Mach_number_x_sr')    ,function=df._Mach_number_x_sr    , sampling_type="cell", units='' )
df.ds.add_field( ("gamer", 'Mach_number_y_sr')    ,function=df._Mach_number_y_sr    , sampling_type="cell", units='' )
df.ds.add_field( ("gamer", 'Mach_number_z_sr')    ,function=df._Mach_number_z_sr    , sampling_type="cell", units='' )
   
df.ds.periodicity = (True, True, True)

ad = df.ds.all_data()

center = df.ds.domain_center
x0 = center[0]
normal_vector = [-1.0, 0.0, 0.0]
radius = 1.875
NumSecPerRank = 2
MostLeftEdge=11
MostRightEdge=30
Length = MostRightEdge - MostLeftEdge

Max = 4.0
Min = 1.0

comm = MPI.COMM_WORLD
TotalRanks = comm.Get_size()
RankIdx = comm.Get_rank()

# this should be a multiple of numer of threads being used
NumCylin =  TotalRanks*NumSecPerRank

# height of section
height = Length / NumCylin           

for i in range(NumSecPerRank*RankIdx+1, NumSecPerRank*RankIdx+NumSecPerRank+1):
 
    center[0] = - ( 0.5 * height * (2*i-1) + 0.5 ) * df.ds.length_unit + MostRightEdge * df.ds.length_unit
    
    print("RankIdx=%d" % RankIdx)
    print("LeftEdge=%f, Center=%f, RightEdge=%f" % ( center[0]-0.5*height* df.ds.length_unit, center[0], center[0]+0.5*height* df.ds.length_unit ))
    print("===========================================")

    cylinder=df.ds.disk(center, normal_vector, radius, height)
    
    vertice1_temp, Ux_temp = cylinder.extract_isocontours('threshold', 1.0, sample_values='Mach_number_x_sr')
    vertice2_temp, Uy_temp = cylinder.extract_isocontours('threshold', 1.0, sample_values='Mach_number_y_sr')
    vertice3_temp, Uz_temp = cylinder.extract_isocontours('threshold', 1.0, sample_values='Mach_number_z_sr')

    # compute vectors along triangle mesh's edges 
    vector1 = vertice1_temp[1::3,:] - vertice1_temp[::3,:]
    vector2 = vertice1_temp[2::3,:] - vertice1_temp[::3,:]

    # normal vectors of triangular meshes, which have dimension (np.size(normal),)
    normal_temp = np.cross(vector1,vector2)


    # find out which rows are vanish, ZeroRow have dimension (np.size(ZeroRow))
    ZeroRow = np.where(~normal_temp.any(axis=1))[0]

    # remove the rows which is specified by ZeroRow
    # -> note that np.delete() does NOT occur in-place
    normal = np.delete(normal_temp, ZeroRow, axis=0)
    Ux     = np.delete(Ux_temp    , ZeroRow, axis=0)
    Uy     = np.delete(Uy_temp    , ZeroRow, axis=0)
    Uz     = np.delete(Uz_temp    , ZeroRow, axis=0)


    # create an 1D array
    ZeroRow_vertice1 = np.arange(3*ZeroRow.shape[0])

    
    for i in range(0, ZeroRow.shape[0]):
       ZeroRow_vertice1[3*i  ] = 3*ZeroRow[i]
       ZeroRow_vertice1[3*i+1] = 3*ZeroRow[i] + 1
       ZeroRow_vertice1[3*i+2] = 3*ZeroRow[i] + 2 


    # remove the vertice which are collinear in 'triangle' meshes
    vertice1 = np.delete(vertice1_temp  , ZeroRow_vertice1, axis=0)


    U = np.vstack((Ux, Uy, Uz))
    U = np.transpose(U)
    U = U.to_ndarray()

    # compute the dot product of normal vector and 4-velocity
    NormalDotU = np.sum(U * normal, axis=1)
    
    # compute the 2-norm of normal vector     
    NormSquare = LA.norm( normal, axis=1 )**2    

    # compute the normal component of 4-velocity
    NormalVelocity = np.transpose( [NormalDotU / NormSquare] ) * normal
   
    # compute the Lorentz factor of normal component velocity 
    NormalLorentzFactor = np.sqrt( 1.0 + np.sum ( NormalVelocity**2, axis=1 ) )
    
    #########################################################
    
    # remove duplicate vertice
    UniqueVertice = np.unique(vertice1, axis=0)
   
    # assign an unique index to every vertice
    IdxVertice = np.zeros(vertice1.shape[0],dtype=np.int16)
   
    # convert format 
    for idx in range(vertice1.shape[0]):
        IdxVertice[idx:idx+1] = UniqueVertice.tolist().index(vertice1[idx:idx+1,:].tolist()[0])
   
    # reshape 
    IdxVertice.shape = (int(IdxVertice.shape[0]/3), 3)
    
    
    #########################################################
    # assign color bar    
    colormap = plt.get_cmap('jet')
    

    # colored in linear scale 
    RGB = colormap((NormalLorentzFactor - Min) / (Max-Min))*255
    
    RGB = RGB.astype(int)
    
    RGB = np.delete(RGB, 3, 1)
    
    
    #########################################################
    #Ref:
    # -> https://stackoverflow.com/questions/26634579/convert-array-of-lists-to-array-of-tuples-triple
   
    UniqueVerticeTuple = np.empty(UniqueVertice.shape[0], dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])
    
    # convert array of list to array of tuples 
    UniqueVerticeTuple[:]=[tuple(i) for i in UniqueVertice]
    
    
    #########################################################
    #Ref:
    # -> https://stackoverflow.com/questions/57048757/how-to-combine-list-with-integer-in-an-array-of-tuples
    
    RGBList = RGB.tolist()
    
    IdxVerticeList = IdxVertice.tolist()
    
    Face = [tuple([IdxVerticeList[i]] + RGBList[i]) for i in range(len(IdxVerticeList))]
    
    Face = np.asarray(Face, dtype=[('vertex_indices', 'i4', (3,)),('red', 'u1'), ('green', 'u1'),('blue', 'u1')])
    
    #########################################################
    
    el = PlyElement.describe(UniqueVerticeTuple, "vertex")
    el2 = PlyElement.describe(Face, "face")
    
    FileName = 'binary_{:f}.ply'.format(center[0])
    
    PlyData([el, el2], text=True).write(FileName)
     
if RankIdx is 0:
  t1 = time.time()
  print("BigStuff took %.5e sec" % (t1 - t0))
