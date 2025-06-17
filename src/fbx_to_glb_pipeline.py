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
    """Import FBX file into Blender"""
    try:
        bpy.ops.import_scene.fbx(filepath=str(fbx_path))
        print(f"Successfully imported: {fbx_path}")
        return True
    except Exception as e:
        print(f"Error importing FBX {fbx_path}: {e}")
        return False

def export_glb(output_path):
    """Export scene as GLB with Godot 4.4 optimized settings"""
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