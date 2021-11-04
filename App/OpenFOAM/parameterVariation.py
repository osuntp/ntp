from os import path
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector
from numpy import linspace

if __name__ == "__main__":
    templateCase = SolutionDirectory("template", archive=None, paraviewLink=False)
    uTangential = linspace(0.1,0.8,8)
    for u in uTangential:
        case = templateCase.cloneCase("cavity-u%.1f"%u)
        print(case.name)
        velBC = ParsedParameterFile(path.join(case.name,"0", "U"))
        velBC["boundaryField"]["movingWall"]["value"].setUniform(Vector(u,0,0))
        velBC.writeFile()