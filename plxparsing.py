import os
import yaml
import numpy as np
from plxscripting.easy import *

def setSoilMaterial(parameters: dict, s_i, g_i):
    '''
    Take parameters from material dictionary from YAML file and put it on Plaxis
    returns Plaxis material object
    '''
    general = [[key, value] for key, value in parameters['general'].items()]
    mechanical = [[key, value] for key, value in parameters['mechanical'].items()]
    groundwater = [[key, value] for key, value in parameters['groundwater'].items()]
    interfaces = [[key, value] for key, value in parameters['interfaces'].items()]
    initial =[[key, value] for key, value in parameters['initial'].items()]
    plaxis_material = g_i.soilmat(
        ['Identification', parameters['Identification']],
        ['SoilModel', parameters['SoilModel']],
        *general, *mechanical, *groundwater, *interfaces, *initial
    )
    return plaxis_material

def makeSoilPolygon(xs, ys, s_i, g_i):
    '''
    Create polygon outof xs and ys
    returns polygon, soil
    '''
    return  g_i.polygon(*zip(xs, ys))

def addPhasePlastic(
        previousPhase, 
        id, 
        g_i, 
        s_i, 
        SumMStage=1, 
        SumMWeight=1, 
        porePressureCalcType="Phreatic", 
        timeInterval=0,
        ignoreUndrained=False,
        resetDisplacement=False,
        resetSmallStrain=False,
        resetStateVar=False,
        resetTime=False,
        updateMesh=False,
        ignoreSuction=True,
        useCavitationCutoff=False,
    ) -> object:
    '''
    set a plastic phase in one go
    returns created phase object
    '''
    CURR_PHASE = g_i.phase(previousPhase)
    CURR_PHASE.Identification = id
    CURR_PHASE.Deform.SumMWeight = SumMWeight
    CURR_PHASE.Deform.Loading.SumMstage = SumMStage
    CURR_PHASE.PorePresCalcType = porePressureCalcType
    CURR_PHASE.TimeInterval = timeInterval
    CURR_PHASE.Deform.IgnoreUndrainedBahvior = ignoreUndrained
    CURR_PHASE.Deform.ResetDisplacementToZero = resetDisplacement
    CURR_PHASE.Deform.ResetSmallStrain = resetSmallStrain
    CURR_PHASE.ResetStateVariables = resetStateVar
    CURR_PHASE.Deform.ResetTime = resetTime
    CURR_PHASE.Deform.UseUpdateMesh = updateMesh
    CURR_PHASE.Deform.IgnoreSuction = ignoreSuction
    CURR_PHASE.Deform.UseCavitationCutOff = useCavitationCutoff

    return CURR_PHASE
    


## Testing Scripts
if  __name__ == "__main__":

    password = '%#U%LyiaH^@i23Mv'
    host = 'localhost'
    port = 10000

    with open("json-templates/material-templates/soil03_HardeningSoil.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        s_i, g_i = new_server(host, port, password=password)

        polygons = [
            [[84.00, 50.00, 50.00, 80.50],
             [-2.90, -2.90, -0.40, -0.40]],
            [[50.00, 50.00, 84.00, 84.50, 85.50, 130.00, 130.00], 
             [-6.50, -2.90, -2.90, -3.33, -3.33, -3.35, -6.50]],
            [[130.00, 50.00, 50.00, 130.00],
             [-8.10, -8.10, -6.50, -6.50]],
            [[130.00, 50.00, 50.00, 130.00],
             [-9.00, -9.00, -8.10, -8.10]],
            [[130.00, 50.00, 50.00, 130.00],
             [-16.00, -16.00, -9.00, -9.00]],
            [[130.00, 50.00, 50.00, 130.00],
             [-25.00, -25.00, -16.00, -16.00]],
            [[85.00, 84.00, 80.50, 81.50],
             [-2.90, -2.90, -0.40, -0.40]],
            [[85.50, 85.00, 84.00, 84.50],
             [-3.33, -2.90, -2.90, -3.33]] 
        ]

        s_i.new()
        # Soil and Structures
        material = setSoilMaterial(data, s_i, g_i)
        polygon = [makeSoilPolygon(polygon[0], polygon[1], s_i, g_i) for polygon in polygons]

        # Set Up Material
        g_i.setmaterial([poly[1] for poly in polygon], material)

        # Meshing
        g_i.gotomesh()
        g_i.mesh()

        # Flow Conditions

        # Staged Construction
        g_i.gotostages()
        addPhasePlastic(g_i.InitialPhase, "testing", g_i, s_i)

        
