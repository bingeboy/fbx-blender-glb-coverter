#!/bin/bash
# Asset Pipeline Runner for FBX to GLB conversion
# Usage: ./run_pipeline.sh

echo "Starting Blender Asset Pipeline..."
echo "Converting FBX files to GLB for Godot 4.4"
echo "=========================================="

# Check if Blender is installed and accessible
if ! command -v blender &> /dev/null; then
    echo "Error: Blender not found in PATH"
    echo "Please install Blender or add it to your PATH"
    echo ""
    echo "On macOS, you might need to create a symlink:"
    echo "ln -s /Applications/Blender.app/Contents/MacOS/Blender /usr/local/bin/blender"
    echo ""
    echo "Or use the full path:"
    echo "/Applications/Blender.app/Contents/MacOS/Blender --background --python fbx_to_glb_pipeline.py"
    exit 1
fi

# Run the pipeline
blender --background --python fbx_to_glb_pipeline.py

echo ""
echo "Pipeline completed!"
echo "Check the 'glb' folder for converted files."