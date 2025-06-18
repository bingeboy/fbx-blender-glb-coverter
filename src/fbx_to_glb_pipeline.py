#!/usr/bin/env python3
"""
Blender Asset Pipeline: FBX to GLB Converter for Godot 4.4
Usage: blender --background --python fbx_to_glb_pipeline.py
"""

import bpy
import os
import sys
from pathlib import Path

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def import_fbx(fbx_path):
    """Import FBX file into Blender with animation support"""
    try:
        bpy.ops.import_scene.fbx(
            filepath=str(fbx_path),
            use_anim=True,  # Import animations
            anim_offset=1.0,  # Animation offset
            use_subsurf=False,  # Don't add subdivision surface
            use_custom_normals=True,  # Use custom normals
            use_image_search=True,  # Search for images in subdirectories
            use_alpha_decals=False,  # Handle alpha decals
            decal_offset=0.0,  # Decal offset
            use_prepost_rot=True,  # Use pre/post rotation
            axis_forward='-Z',  # Forward axis
            axis_up='Y',  # Up axis
            global_scale=1.0,  # Global scale
            bake_space_transform=False,  # Don't bake space transform
            force_connect_children=False,  # Don't force connect children
            automatic_bone_orientation=False,  # Don't automatically orient bones
            primary_bone_axis='Y',  # Primary bone axis
            secondary_bone_axis='X'  # Secondary bone axis
        )
        print(f"Successfully imported: {fbx_path}")
        return True
    except Exception as e:
        print(f"Error importing FBX {fbx_path}: {e}")
        return False

def debug_animations():
    """Debug and report animation information in the current scene"""
    print("\n=== Animation Debug Info ===")
    
    # Check actions
    if bpy.data.actions:
        print(f"Found {len(bpy.data.actions)} action(s):")
        for i, action in enumerate(bpy.data.actions):
            print(f"  {i+1}. '{action.name}' - {len(action.fcurves)} fcurves, frames {action.frame_range[0]}-{action.frame_range[1]}")
    else:
        print("No actions found")
    
    # Check armatures
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
    if armatures:
        print(f"Found {len(armatures)} armature(s):")
        for armature in armatures:
            has_anim = armature.animation_data is not None
            current_action = armature.animation_data.action.name if has_anim and armature.animation_data.action else "None"
            print(f"  - '{armature.name}': animation_data={has_anim}, action={current_action}")
    else:
        print("No armatures found")
    
    # Total keyframes
    total_keyframes = sum(len(fcurve.keyframe_points) for action in bpy.data.actions for fcurve in action.fcurves)
    print(f"Total keyframes: {total_keyframes}")
    print("=== End Animation Debug ===\n")

def export_glb(output_path):
    """Export scene as GLB with enhanced animation support for Godot 4.4"""
    # Debug animations before export
    debug_animations()
    
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(output_path),
            export_format='GLB',
            export_texcoords=True,
            export_normals=True,
            export_materials='EXPORT',
            export_cameras=False,
            export_yup=True,
            export_apply=True,
            export_animations=True,
            export_frame_range=False,  # Export all animation frames
            export_force_sampling=False,  # Use original keyframes
            export_nla_strips=True,  # Export NLA strips as separate animations
            export_def_bones=False,  # Don't export deformation bones only
            export_current_frame=False,  # Don't limit to current frame
            export_skins=True,  # Export armature deformation
            export_all_influences=False,  # Limit vertex influences for performance
            export_morph=True,  # Export shape keys/morph targets
            export_image_format='AUTO'
        )
        print(f"Successfully exported GLB: {output_path}")
        return True
    except Exception as e:
        print(f"Error exporting GLB {output_path}: {e}")
        return False

def process_fbx_folder(fbx_folder_path, glb_folder_path):
    """Process a single FBX folder containing model and textures"""
    fbx_folder = Path(fbx_folder_path)
    
    # Find FBX file in the folder
    fbx_files = list(fbx_folder.glob("*.fbx"))
    if not fbx_files:
        print(f"No FBX files found in {fbx_folder}")
        return False
    
    if len(fbx_files) > 1:
        print(f"Multiple FBX files found in {fbx_folder}, using first one: {fbx_files[0]}")
    
    fbx_file = fbx_files[0]
    folder_name = fbx_folder.name
    
    # Clear scene before importing
    clear_scene()
    
    # Import FBX
    if not import_fbx(fbx_file):
        return False
    
    # Create output path
    glb_output = Path(glb_folder_path) / f"{folder_name}.glb"
    
    # Export as GLB
    return export_glb(glb_output)

def main():
    """Main pipeline function"""
    script_dir = Path(__file__).parent
    fbx_dir = script_dir / "fbx"
    glb_dir = script_dir / "glb"
    
    # Ensure GLB directory exists
    glb_dir.mkdir(exist_ok=True)
    
    if not fbx_dir.exists():
        print(f"FBX directory not found: {fbx_dir}")
        return
    
    # Process each folder in the FBX directory
    fbx_folders = [item for item in fbx_dir.iterdir() if item.is_dir()]
    
    if not fbx_folders:
        print("No folders found in FBX directory")
        return
    
    print(f"Found {len(fbx_folders)} folders to process")
    
    successful_conversions = 0
    failed_conversions = 0
    
    for fbx_folder in fbx_folders:
        print(f"\nProcessing folder: {fbx_folder.name}")
        
        if process_fbx_folder(fbx_folder, glb_dir):
            successful_conversions += 1
            print(f"✓ Successfully converted {fbx_folder.name}")
        else:
            failed_conversions += 1
            print(f"✗ Failed to convert {fbx_folder.name}")
    
    print(f"\n--- Conversion Summary ---")
    print(f"Successful: {successful_conversions}")
    print(f"Failed: {failed_conversions}")
    print(f"Total: {len(fbx_folders)}")

if __name__ == "__main__":
    main()