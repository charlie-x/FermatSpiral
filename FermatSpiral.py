# @author : charliex 
# @ref https://www.reddit.com/r/Fusion360/comments/1ev74oz/how_do_great_a_fermats_spiral_in_fusion/
# @desc : generates a fermat spiral in autodesk fusion.
#
#         A Fermat spiral is a type of spiral that is defined by the polar equation r = c * sqrt(theta)
#         generates theh spiral with a given value of c, number of points, and angle increment between each point
#         and creates a new sketch in the active fusion design  and adds the spiral to the sketch
#         whcih is created by generating points using the polar equation and then creating a spline curve through those points
#
# https://i.imgur.com/QazGDAo.png

import adsk.core, adsk.fusion, traceback
import math

c = 1.0                     # size of spacing between spiral arms
num_points = 100            # number points to plot on the spiral
theta_increment = 0.1       # angle increment between each point (radians)

# generate spiral points
def generate_fermat_spiral_points(c, num_points, theta_increment):
    """
    generates the points on a fermat spiral

    Args:
        c (float):  determines the scale of the spiral
        num_points (int): number of points to generate
        theta_increment (float):  theta

    Returns:
        list: list of tuples representing the generated points on the spiral
    """
    points = []
    for i in range(num_points):
        theta = i * theta_increment
        r = c * math.sqrt(theta)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y))
    return points

def create_spiral_sketch(sketch, points):
    """
    creates a spiral sketch using the given points
    Parameters:
        sketch (adsk.fusion.Sketch): sketch to create the spiral in
        points (list): list of points representing the spiral
    Returns:
        None
    """

    lines = sketch.sketchCurves.sketchLines
    spline_points = adsk.core.ObjectCollection.create()
    

    previous_point = adsk.core.Point3D.create(points[0][0], points[0][1], 0)
    spline_points.add(previous_point)
    
    for point in points[1:]:
        current_point = adsk.core.Point3D.create(point[0], point[1], 0)
        spline_points.add(current_point)
        previous_point = current_point
    

    sketch.sketchCurves.sketchFittedSplines.add(spline_points)

def run(context):
    """
    generate a fermat spiral in fusion
    Parameters:
        context (object): context
    Returns:
        None
    """
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent


        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)


        points = generate_fermat_spiral_points(c, num_points, theta_increment)


        create_spiral_sketch(sketch, points)

        ui.messageBox('fermat spiral created')

    except Exception as e:
        if ui:
            ui.messageBox('failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
    except:
        pass
