'''
AMMM Lab Heuristics v1.2
Instance file validator.
Copyright 2018 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['nServices', 'sStartTime', 'sMin', 'sKM', 'sLoad', 'nBuses', 'bCap', 'bCPM', 'bCPKm', 'maxBuses', 'nDrivers', 'dMaxMin', 'BM', 'CBM', 'CEM']:
            if(paramName not in data.__dict__):
                raise Exception('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate nServices
        nServices = data.nServices
        if(not isinstance(nServices, (int)) or (nServices <= 0)):
            raise Exception('nServices(%s) has to be a positive integer value.' % str(nServices))

        # Validate sStartTime
        sStartTime = data.sStartTime
        if(len(sStartTime) != nServices):
            raise Exception('Size of sStartTime(%d) does not match with value of nServices(%d).' % (len(sStartTime), nServices))        
        # Validate sMin
        sMin = data.sMin
        if(len(sMin) != nServices):
            raise Exception('Size of sMin(%d) does not match with value of nServices(%d).' % (len(sMin), nServices))
        # Validate sKM
        sKM = data.sKM
        if(len(sKM) != nServices):
            raise Exception('Size of sKM(%d) does not match with value of nServices(%d).' % (len(sKM), nServices))
        # Validate sLoad
        sLoad = data.sLoad
        if(len(sLoad) != nServices):
            raise Exception('Size of sLoad(%d) does not match with value of nServices(%d).' % (len(sLoad), nServices))
        # Validate nBuses
        nBuses = data.nBuses
        if(not isinstance(nBuses, (int)) or (nBuses <= 0)):
            raise Exception('nBuses(%s) has to be a positive integer value.' % str(nBuses))
        # Validate bCap
        bCap = data.bCap
        if(len(bCap) != nBuses):
            raise Exception('Size of bCap(%d) does not match with value of nBuses(%d).' % (len(bCap), nBuses))        
        # Validate bCPM
        bCPM = data.bCPM
        if(len(bCPM) != nBuses):
            raise Exception('Size of bCPM(%d) does not match with value of nBuses(%d).' % (len(bCPM), nBuses))  
        # Validate bCPKm
        bCPKm = data.bCPKm
        if(len(bCPKm) != nBuses):
            raise Exception('Size of bCPKm(%d) does not match with value of nBuses(%d).' % (len(bCPKm), nBuses))  
        # Validate maxBuses
        maxBuses = data.maxBuses
        if(not isinstance(maxBuses, (int)) or (maxBuses <= 0)):
            raise Exception('maxBuses(%s) has to be a positive integer value.' % str(maxBuses))
        # Validate nDrivers
        nDrivers = data.nDrivers
        if(not isinstance(nDrivers, (int)) or (nDrivers <= 0)):
            raise Exception('nDrivers(%s) has to be a positive integer value.' % str(nDrivers))
        # Validate dMaxMin
        dMaxMin = data.dMaxMin
        if(len(dMaxMin) != nDrivers):
            raise Exception('Size of dMaxMin(%d) does not match with value of nDrivers(%d).' % (len(dMaxMin), nDrivers))  
        # Validate BM
        BM = data.BM
        if(not isinstance(BM, (int)) or (BM <= 0)):
            raise Exception('BM(%s) has to be a positive integer value.' % str(BM))
        # Validate CBM
        CBM = data.CBM
        if(not isinstance(CBM, (int, float)) or (CBM <= 0)):
            raise Exception('CBM(%s) has to be a positive integer/float value.' % str(CBM))
        # Validate CEM
        CEM = data.CEM
        if(not isinstance(CEM, (int, float)) or (CEM <= 0)):
            raise Exception('CEM(%s) has to be a positive integer/float value.' % str(CEM))