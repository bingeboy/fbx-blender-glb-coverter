# Blender Asset Pipeline: FBX to GLB Converter

A streamlined asset pipeline for converting FBX models with textures to GLB format, optimized for Godot 4.4.

## Overview

This tool automatically processes FBX model folders and converts them to GLB format with textures preserved. It's designed to work with Godot 4.4's asset requirements and handles batch processing of multiple models.

## Prerequisites

- **Blender 4.0+** installed on your system
- Blender accessible via command line (see setup instructions below)

### Blender Setup

#### macOS
```bash
# Create a symlink to make Blender accessible from terminal
ln -s /Applications/Blender.app/Contents/MacOS/Blender /usr/local/bin/blender

# Or add to your PATH in ~/.zshrc or ~/.bash_profile
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"
```

#### Windows
```batch
# Add Blender installation directory to your PATH
# Usually: C:\Program Files\Blender Foundation\Blender [version]\
```

#### Linux
```bash
# Install via package manager
sudo apt install blender  # Ubuntu/Debian
sudo pacman -S blender     # Arch
```

## Project Structure

```
assetPipeline/
├── fbx/                     # Input folder for FBX models
│   ├── model_name_1/        # Each model gets its own folder
│   │   ├── model.fbx        # FBX file
│   │   ├── texture.png      # Texture files
│   │   └── normal.png       # Additional textures
│   └── model_name_2/
│       ├── character.fbx
│       └── skin.jpg
├── glb/                     # Output folder (auto-created)
│   ├── model_name_1.glb     # Converted GLB files
│   └── model_name_2.glb
├── fbx_to_glb_pipeline.py   # Main conversion script
├── run_pipeline.sh          # Execution wrapper
└── README.md                # This file
```

## Usage

### Method 1: Using the Shell Script
```bash
# Make the script executable (first time only)
chmod +x run_pipeline.sh

# Run the pipeline
./run_pipeline.sh
```

### Method 2: Direct Blender Command
```bash
blender --background --python fbx_to_glb_pipeline.py
```

### Method 3: Using Full Blender Path (if not in PATH)
```bash
# macOS
/Applications/Blender.app/Contents/MacOS/Blender --background --python fbx_to_glb_pipeline.py

# Windows
"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe" --background --python fbx_to_glb_pipeline.py
```

## How It Works

1. **Scans** the `fbx/` directory for model folders
2. **Imports** each FBX file found in the folders
3. **Preserves** all textures and materials
4. **Exports** as GLB with Godot 4.4 optimized settings
5. **Saves** converted files to the `glb/` folder

## Supported Features

- ✅ FBX model import with textures
- ✅ Material preservation
- ✅ Texture coordinate mapping
- ✅ Normal maps and surface data
- ✅ Animations (if present in FBX)
- ✅ Batch processing of multiple models
- ✅ Godot 4.4 compatibility
- ✅ Automatic Y-up coordinate conversion

## GLB Export Settings

The pipeline uses these optimized settings for Godot 4.4:

- **Format**: GLB (binary)
- **Textures**: Preserved with automatic format detection
- **Materials**: Full export with PBR compatibility
- **Coordinates**: Y-up (Godot standard)
- **Animations**: Included if present
- **Compression**: Disabled for maximum compatibility

## Troubleshooting

### Common Issues

**"Blender not found in PATH"**
- Ensure Blender is installed and accessible via command line
- Follow the Blender setup instructions above

**"No FBX files found in folder"**
- Check that your FBX files are directly inside the model folders
- Ensure folder structure matches the expected format

**"Failed to convert [model]"**
- Check that the FBX file is not corrupted
- Ensure all referenced textures are in the same folder
- Try opening the FBX in Blender manually to verify it's valid

**"Permission denied"**
- Make sure the script has execute permissions: `chmod +x run_pipeline.sh`
- Check that you have write permissions in the project directory

### Debugging

For more detailed output, run Blender with verbose logging:
```bash
blender --background --python fbx_to_glb_pipeline.py --debug
```

## Adding New Models

1. Create a new folder in `fbx/` with your model name
2. Place the FBX file and all textures in that folder
3. Run the pipeline
4. Check `glb/` for the converted file

Example:
```bash
mkdir fbx/my_character
cp path/to/character.fbx fbx/my_character/
cp path/to/texture.png fbx/my_character/
./run_pipeline.sh
```

## Godot 4.4 Integration

The generated GLB files are ready to use in Godot 4.4:

1. Copy GLB files to your Godot project's asset folder
2. Godot will automatically import them
3. Materials and textures should be preserved
4. No additional configuration needed

## Performance Tips

- Keep texture sizes reasonable (1024x1024 or 2048x2048 for most use cases)
- Use power-of-2 texture dimensions when possible
- Consider using PNG for textures with transparency, JPG for opaque textures
- Remove unused materials and textures from FBX files before conversion

## License

This tool is provided as-is for asset pipeline automation. Ensure you have proper licenses for any FBX files and textures you process.