import h5py
import numpy as np
import yt
import os


def my_create_grps(name):
    fd.create_group(name)



# recursively copy groups
#fs['/'].visit(my_create_grps)


#fs.copy('/GridData',fd['/GridData'])
#fs.copy('/Info'    ,fd['/Info']    )
#fs.copy('/Tree'    ,fd['/Tree']    )


for idx in range(32,33):

   filename = "Data_%06d"%idx

   print('convert '+ filename + ' ...')
   
   fs = h5py.File(filename,"r")
   fd = h5py.File(filename+"_single","w")
   
   Dens=fs['/GridData/Dens']
   MomX=fs['/GridData/MomX']
   MomY=fs['/GridData/MomY']
   MomZ=fs['/GridData/MomZ']
   Engy=fs['/GridData/Engy']
   Temp=fs['/GridData/Temp']
   
   
   Dens_single=np.empty(Dens.shape,dtype=np.float32)
   MomX_single=np.empty(Dens.shape,dtype=np.float32)
   MomY_single=np.empty(Dens.shape,dtype=np.float32)
   MomZ_single=np.empty(Dens.shape,dtype=np.float32)
   Engy_single=np.empty(Dens.shape,dtype=np.float32)
   Temp_single=np.empty(Dens.shape,dtype=np.float32)
   
   
   Dens.read_direct(Dens_single)
   MomX.read_direct(MomX_single)
   MomY.read_direct(MomY_single)
   MomZ.read_direct(MomZ_single)
   Engy.read_direct(Engy_single)
   Temp.read_direct(Temp_single)
   
   fd.create_dataset('GridData/Dens', data=Dens_single)
   fd.create_dataset('GridData/MomX', data=MomX_single)
   fd.create_dataset('GridData/MomY', data=MomY_single)
   fd.create_dataset('GridData/MomZ', data=MomZ_single)
   fd.create_dataset('GridData/Engy', data=Engy_single)
   fd.create_dataset('GridData/Temp', data=Temp_single)
   
   array=fs['Info/InputPara']
   fd.create_dataset('Info/InputPara', data=array)
   
   array=fs['Info/KeyInfo']
   fd.create_dataset('Info/KeyInfo', data=array)
   
   array=fs['Info/Makefile']
   fd.create_dataset('Info/Makefile', data=array)
   
   array=fs['Info/SymConst']
   fd.create_dataset('Info/SymConst', data=array)
   
   array=fs['Tree/Corner']
   fd.create_dataset('Tree/Corner', data=array)
   fd['Tree/Corner'].attrs['Cvt2Phy'] = fs['Tree/Corner'].attrs['Cvt2Phy']
   
   array=fs['Tree/Father']
   fd.create_dataset('Tree/Father', data=array)
   
   array=fs['Tree/LBIdx']
   fd.create_dataset('Tree/LBIdx', data=array)
   
   array=fs['Tree/Sibling']
   fd.create_dataset('Tree/Sibling', data=array)
   
   array=fs['Tree/Son']
   fd.create_dataset('Tree/Son', data=array)
   
   
   fd.flush()
   
   #After you are done
   fs.close()
   fd.close()

   os.remove(filename)
   os.rename(filename+"_single", filename)
