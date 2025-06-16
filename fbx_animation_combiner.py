#!/usr/bin/env python3
"""
Blender Animation Combiner: Combine FBX character with multiple animation files
Usage: blender --background --python fbx_animation_combiner.py
"""

import bpy
import os
from pathlib import Path

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def import_fbx_with_animations(base_fbx_path, animation_fbx_paths):
    """Import base character and merge animations"""
    
    # Import base character (T-pose)
    print(f"Importing base character: {base_fbx_path}")
    bpy.ops.import_scene.fbx(filepath=str(base_fbx_path))
    
    # Find armature object
    armature_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            armature_obj = obj
            break
    
    if not armature_obj:
        print("Error: No armature found in base character!")
        return False
    
    print(f"Found armature: {armature_obj.name}")
    
    # Import each animation file and merge actions
    for i, anim_path in enumerate(animation_fbx_paths):
        print(f"Processing animation: {anim_path}")
        
        # Store current objects to identify new imports
        existing_objects = set(bpy.context.scene.objects)
        
        # Import animation FBX
        bpy.ops.import_scene.fbx(filepath=str(anim_path))
        
        # Find newly imported armature
        new_objects = set(bpy.context.scene.objects) - existing_objects
        imported_armature = None
        for obj in new_objects:
            if obj.type == 'ARMATURE':
                imported_armature = obj
                break
        
        if imported_armature and imported_armature.animation_data:
            # Copy animation action to base armature
            if imported_armature.animation_data.action:
                action = imported_armature.animation_data.action
                action_name = Path(anim_path).stem
                action.name = action_name
                print(f"Copied animation action: {action_name}")
        
        # Clean up imported objects (keep only the animation data)
        for obj in new_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
    
    return True

def export_glb_with_animations(output_path):
    """Export as GLB with all animations for Godot 4.4"""
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(output_path),
            export_format='GLB',
            export_texcoords=True,
            export_normals=True,
            export_materials='EXPORT',
            export_cameras=False,
            export_lights=False,
            export_yup=True,
            export_apply=True,
            export_animations=True,
            export_frame_range=False,
            export_nla_strips=True,
            export_image_format='AUTO',
            export_optimize_animation_size=True
        )
        print(f"Successfully exported GLB with animations: {output_path}")
        return True
    except Exception as e:
        print(f"Error exporting GLB: {e}")
        return False

def main():
    """Main function to combine FBX animations"""
    script_dir = Path(__file__).parent
    fbx_anim_dir = script_dir / "fbxAnimation"
    glb_dir = script_dir / "glb"
    
    # Ensure GLB directory exists
    glb_dir.mkdir(exist_ok=True)
    
    if not fbx_anim_dir.exists():
        print(f"FBX Animation directory not found: {fbx_anim_dir}")
        return
    
    # Find base character file (T-pose)
    base_fbx = fbx_anim_dir / "Ch20_nonPBR.fbx"
    if not base_fbx.exists():
        print(f"Base character file not found: {base_fbx}")
        return
    
    # Find animation files
    animation_files = []
    for fbx_file in fbx_anim_dir.glob("*.fbx"):
        if fbx_file.name != "Ch20_nonPBR.fbx":
            animation_files.append(fbx_file)
    
    if not animation_files:
        print("No animation files found!")
        return
    
    print(f"Found {len(animation_files)} animation files:")
    for anim_file in animation_files:
        print(f"  - {anim_file.name}")
    
    # Clear scene
    clear_scene()
    
    # Import and combine animations
    if import_fbx_with_animations(base_fbx, animation_files):
        # Export combined GLB
        output_glb = glb_dir / "Ch20_with_animations.glb"
        if export_glb_with_animations(output_glb):
            print(f"\n✓ Successfully created: {output_glb}")
            print("Ready for use in Godot 4.4!")
        else:
            print("✗ Failed to export GLB")
    else:
        print("✗ Failed to combine animations")

if __name__ == "__main__":
    main()