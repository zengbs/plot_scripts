import numpy as np

# PositionArray: 1D
# NumericalArray: 1D
# AnalyticalData: 2D

def L1Norm( PositionArray, NumericalArray, AnalyticalData, LowerLimit, UpperLimit, Abs_Or_Rel ):
   Bool = (LowerLimit<PositionArray) & (PositionArray<UpperLimit)
 
   NumericalArray = np.extract( Bool, NumericalArray )
   PositionArray  = np.extract( Bool, PositionArray  )
 
   N = len(NumericalArray)
 
   AnalyticalArray = np.interp(PositionArray,AnalyticalData[0],AnalyticalData[1])
 
   if Abs_Or_Rel == "RelativeError":
     L1Error = sum(abs( 1 - NumericalArray/AnalyticalArray )) / N 
   elif Abs_Or_Rel == "AbsoluteError":
     L1Error = sum(abs( NumericalArray - AnalyticalArray )) / N 
   elif Abs_Or_Rel == "Ratio":
     L1Error = sum(abs( NumericalArray / AnalyticalArray )) / N 
 
 
   return L1Error

