import zipfile
import bpy
import random
import os
import pathlib
import sys

def CreateFoldersVisuals():
    if not os.path.exists('VisualStems/Background'):
        os.mkdir('VisualStems/Background')
    
    if not os.path.exists('VisualStems/Eyes'):
        os.mkdir('VisualStems/Eyes')

    if not os.path.exists('VisualStems/Hat'):
        os.mkdir('VisualStems/Hat')

    if not os.path.exists('VisualStems/Head'):
        os.mkdir('VisualStems/Head')

    if not os.path.exists('VisualStems/Mouth'):
        os.mkdir('VisualStems/Mouth')

    if not os.path.exists('VisualStems/Nose'):
        os.mkdir('VisualStems/Nose')


def RandomizeColor():
    headMat = bpy.data.materials.get('head')
    eyesMat = bpy.data.materials.get('eyes')
    noseMat = bpy.data.materials.get('nose')
    mouthMat = bpy.data.materials.get('mouth')
    hatMat = bpy.data.materials.get('hat')
    backgroundMat = bpy.data.materials.get('background')
   
    headMat.use_nodes = True
    eyesMat.use_nodes= True
    noseMat.use_nodes= True
    mouthMat.use_nodes= True
    hatMat.use_nodes= True
    backgroundMat.use_nodes= True

    MatList = [headMat, eyesMat, noseMat, mouthMat, hatMat]
    for step in range(5):
        x = MatList[step]
        print(x)
        principled_node = x.node_tree.nodes.get('Principled BSDF')
        principled_node.inputs[0].default_value = (random.random(), random.random(), random.random(),1)

    data_node = backgroundMat.node_tree.nodes.get('Musgrave Texture')
    print(x)
    data_node.inputs[2].default_value = (random.uniform(0.3, 15))
    
    color_node = backgroundMat.node_tree.nodes.get('ColorRamp')
    
    for step in range(6):
        color_node.color_ramp.elements[step].color = (random.random(), random.random(), random.random(),1)

def rendermulti(script_dir, output_file_pattern_string = 'render%d.jpg'):
    import os 
    #Number of unique layers
    for step in range(12):
            RandomizeColor()
            bpy.context.scene.render.filepath = os.path.join(script_dir, (output_file_pattern_string % step))    
            bpy.ops.render.render(write_still=True)
            DeleteCam()
            CreateCamera()



def DeleteCam():
    
    if bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Camera'].select_set(True)
    bpy.ops.object.delete()

def CreateCamera():
    from bpy import context
    scene = context.scene
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(7.35889, -6.92579, 4.95831), rotation=(1.10932, 0, 0.814927), scale=(1, 1, 1))
    scene.camera = context.object

def rendermultilayer(script_dir, layer,):
    y = str(layer)
    print(y)
    bpy.data.objects["Hat"].hide_render = True
    bpy.data.objects["Head"].hide_render = True
    bpy.data.objects["Mouth"].hide_render = True
    bpy.data.objects["Nose"].hide_render = True
    bpy.data.objects["Eyes"].hide_render = True
    bpy.data.objects["Background"].hide_render = True
    bpy.data.objects[y].hide_render = False
    #Number of unique Layers
    for step in range(12):
            w = str(step)
            z = str(y + w)
            print(z)
            RandomizeColor()
            bpy.context.scene.render.filepath = os.path.join(str(script_dir), "VisualStems", y, (y + str(step)))    
            bpy.ops.render.render(write_still=True)
            DeleteCam()
            CreateCamera()

def renderAll(script_dir):
    bins = [ 'Hat', 'Head', 'Mouth', 'Nose', 'Eyes', 'Background' ] 
    for step in range (6):
        x = bins[step]
        rendermultilayer(script_dir, x)

script_path = bpy.context.space_data.text.filepath
script_dir = pathlib.Path(script_path).resolve().parent
os.chdir(script_dir)
print(script_dir)


CreateFoldersVisuals()

CreateCamera()
renderAll(script_dir)


rendermultilayer(script_dir, 'Background')

#rendermulti(script_dir, 'render%d.jpg') -Fix this layer, redunant
