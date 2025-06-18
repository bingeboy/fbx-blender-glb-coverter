# Blender Asset Pipeline: FBX to GLB Converter

A streamlined asset pipeline for converting FBX models with textures to GLB format, optimized for Godot 4.4. Features a dynamic CLI that automatically discovers and processes all FBX assets without hardcoded filenames.

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
root/
├── fbx/                     # Input folder for FBX models
│   ├── character_model/     # Each model gets its own folder
│   │   ├── model.fbx        # FBX file
│   │   ├── texture.png      # Texture files
│   │   └── normal.png       # Additional textures
│   └── weapon_sword/
│       ├── weapon.fbx
│       └── metal_texture.jpg
├── glb/                     # Output folder (auto-created)
│   ├── character_model.glb  # Converted GLB files
│   └── weapon_sword.glb
├── src/                     # Source scripts directory
│   ├── asset_pipeline_cli.py    # Dynamic CLI tool
│   ├── fbx_to_glb_pipeline.py   # Main conversion script
│   └── run_pipeline.sh          # Shell wrapper
└── README.md                # This file
```

## Usage

### Method 1: Using the Dynamic CLI (Recommended)

The CLI automatically discovers all FBX folders and provides flexible conversion options:

```bash
# List all available assets
python src/asset_pipeline_cli.py --list

# Convert all assets
python src/asset_pipeline_cli.py --convert

# Convert specific assets
python src/asset_pipeline_cli.py --convert character_model weapon_sword

# Convert with verbose output
python src/asset_pipeline_cli.py --convert --verbose

# Show help
python src/asset_pipeline_cli.py --help
```

### Method 2: Using the Shell Script
```bash
# Make the script executable (first time only)
chmod +x src/run_pipeline.sh

# Run the pipeline (converts all assets)
./src/run_pipeline.sh
```

### Method 3: Direct Blender Command
```bash
blender --background --python src/fbx_to_glb_pipeline.py
```

### Method 4: Using Full Blender Path (if not in PATH)
```bash
# macOS
/Applications/Blender.app/Contents/MacOS/Blender --background --python src/fbx_to_glb_pipeline.py

# Windows
"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe" --background --python src/fbx_to_glb_pipeline.py
```

## How It Works

1. **Discovers** all folders in the `fbx/` directory dynamically
2. **Imports** each FBX file found in the folders
3. **Preserves** all textures and materials
4. **Exports** as GLB with Godot 4.4 optimized settings
5. **Saves** converted files to the `glb/` folder

## CLI Features

- **Dynamic Discovery**: Automatically finds all FBX folders without hardcoded names
- **Selective Processing**: Convert specific assets or all at once
- **Status Reporting**: Shows which assets have been converted
- **Verbose Logging**: Detailed output for debugging
- **Blender Validation**: Checks if Blender is properly installed

## Supported Features

- ✅ FBX model import with textures
- ✅ Material preservation
- ✅ Texture coordinate mapping
- ✅ Normal maps and surface data
- ✅ Animation sequences (walk, run, idle, etc.)
- ✅ Skeletal animations and armatures
- ✅ Multiple animation clips in single FBX
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

For more detailed output, use the CLI verbose mode:
```bash
python src/asset_pipeline_cli.py --convert --verbose
```

## Adding New Models

1. Create a new folder in `fbx/` with your model name
2. Place the FBX file and all textures in that folder
3. Run the CLI to see your new asset
4. Convert it using the CLI

Example:
```bash
mkdir fbx/space_ship
cp path/to/ship.fbx fbx/space_ship/
cp path/to/hull_texture.png fbx/space_ship/

# List to see your new asset
python src/asset_pipeline_cli.py --list

# Convert just this asset
python src/asset_pipeline_cli.py --convert space_ship
```

## Working with Animated FBX Files

The pipeline fully supports FBX files with animations, including multiple animation sequences and complex skeletal rigs.

### Animated Model Structure

```
fbx/
└── animated_character/
    ├── character.fbx           # FBX with multiple animations
    ├── diffuse_texture.png     # Character textures
    ├── normal_map.png
    └── specular_map.png
```

### Animation Support

The tool preserves all animations from your FBX file:
- **Multiple Animation Clips**: Walk, run, idle, attack, etc.
- **Skeletal Animations**: Full bone hierarchy and weights
- **Keyframe Data**: All animation timing and curves
- **Animation Names**: Preserves original clip names from FBX

### Converting Animated Models

```bash
# Check your animated asset
python src/asset_pipeline_cli.py --list
# Output shows:
#   1. animated_character
#      FBX files: 1
#      Textures: 3
#      Status: ✗ No GLB

# Convert the animated character
python src/asset_pipeline_cli.py --convert animated_character

# For detailed animation processing info
python src/asset_pipeline_cli.py --convert animated_character --verbose
```

### Common Animated FBX Workflows

**Character with Multiple Animations:**
```bash
mkdir fbx/hero_character
# Copy FBX containing: idle, walk, run, jump, attack animations
cp path/to/hero_with_anims.fbx fbx/hero_character/
cp path/to/character_textures/*.png fbx/hero_character/

python src/asset_pipeline_cli.py --convert hero_character
```

**Batch Converting Multiple Animated Characters:**
```bash
# Convert all animated characters at once
python src/asset_pipeline_cli.py --convert hero_character enemy_orc companion_mage

# Or convert everything
python src/asset_pipeline_cli.py --convert
```

### Animation Optimization Tips

- **FBX Preparation**: Ensure animations are properly named in your 3D software
- **Frame Rate**: Use consistent frame rates (30fps recommended for games)
- **Animation Length**: Keep clips concise to reduce file size
- **Bone Count**: Minimize bone count while maintaining quality
- **Keyframe Reduction**: Clean up unnecessary keyframes before export

## Godot 4.4 Integration

The generated GLB files are ready to use in Godot 4.4:

1. Copy GLB files to your Godot project's asset folder
2. Godot will automatically import them
3. Materials and textures should be preserved
4. **Animations are automatically available** in the AnimationPlayer node
5. No additional configuration needed

### Using Animations in Godot

For animated GLB files:
- Drag the GLB into your scene
- The model will have an **AnimationPlayer** node attached
- All animation clips from the FBX will be available in the AnimationPlayer
- Animation names match those from your original FBX file
- Use `animation_player.play("walk")` to play specific animations

## Performance Tips

- Keep texture sizes reasonable (1024x1024 or 2048x2048 for most use cases)
- Use power-of-2 texture dimensions when possible
- Consider using PNG for textures with transparency, JPG for opaque textures
- Remove unused materials and textures from FBX files before conversion

## License

This tool is provided as-is for asset pipeline automation. Ensure you have proper licenses for any FBX files and textures you process.
