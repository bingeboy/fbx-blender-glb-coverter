# Blender Asset Pipeline: FBX to GLB Converter

A streamlined asset pipeline for converting FBX models with textures to GLB format, optimized for Godot.

## Overview

This tool automatically processes FBX model folders and converts them to GLB format with textures preserved. It's designed to work with Godot 4 asset requirements and handles batch processing of multiple models.

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
├── fbxAnimation/            # Input folder for FBX animation combining
│   ├── Ch20_nonPBR.fbx      # Base character (T-pose)
│   ├── Walking.fbx          # Individual animation files
│   ├── Running.fbx
│   └── Idle.fbx
├── glb/                     # Output folder (auto-created)
│   ├── character_model.glb  # Converted GLB files
│   ├── weapon_sword.glb
│   └── Ch20_nonPBR_with_animations.glb  # Combined animation GLB
├── src/                     # Source scripts directory
│   ├── asset_pipeline_cli.py        # Dynamic CLI tool
│   ├── fbx_to_glb_pipeline.py       # Main conversion script
│   ├── fbx_animation_combiner.py    # Animation combining script
│   └── run_pipeline.sh              # Shell wrapper
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

# Combine FBX animations (from fbxAnimation folder)
python src/asset_pipeline_cli.py --combine-animations

# Combine animations with custom base character
python src/asset_pipeline_cli.py --combine-animations --base-character MyChar.fbx --verbose

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

## Working with Animated FBX Files

The pipeline supports two animation workflows:

### Option 1: Single FBX with Multiple Animations (Standard)

For FBX files that already contain multiple animation clips:

```
fbx/
└── animated_character/
    ├── character.fbx           # FBX with multiple animations
    ├── diffuse_texture.png     # Character textures
    ├── normal_map.png
    └── specular_map.png
```

**Converting Single FBX with Animations:**
```bash
# Convert the animated character
python src/asset_pipeline_cli.py --convert animated_character

# For detailed animation processing info
python src/asset_pipeline_cli.py --convert animated_character --verbose
```

### Option 2: Combining Separate Animation Files

For workflows where you have a base character and separate animation FBX files:

```
fbxAnimation/
├── Ch20_nonPBR.fbx      # Base character (T-pose)
├── Walking.fbx          # Individual animation files
├── Running.fbx
├── Idle.fbx
├── Jumping.fbx
└── Attack.fbx
```

**Combining Separate Animation Files:**
```bash
# Combine all animations with default base character (Ch20_nonPBR.fbx)
python src/asset_pipeline_cli.py --combine-animations

# Use a custom base character
python src/asset_pipeline_cli.py --combine-animations --base-character MyChar.fbx

# With verbose output for debugging
python src/asset_pipeline_cli.py --combine-animations --base-character MyChar.fbx --verbose
```

This creates a single GLB file (e.g., `Ch20_nonPBR_with_animations.glb`) containing the base character with all animations combined.


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


### Animation Support

Both workflows preserve:
- **Multiple Animation Clips**: Walk, run, idle, attack, etc.
- **Skeletal Animations**: Full bone hierarchy and weights
- **Keyframe Data**: All animation timing and curves
- **Animation Names**: Preserves original clip names from FBX

### Common Animation Workflows

**Standard Single FBX Workflow:**
```bash
mkdir fbx/hero_character
# Copy FBX containing: idle, walk, run, jump, attack animations
cp path/to/hero_with_anims.fbx fbx/hero_character/
cp path/to/character_textures/*.png fbx/hero_character/

python src/asset_pipeline_cli.py --convert hero_character
```

**Separate Files Workflow:**
```bash
# Create fbxAnimation directory if it doesn't exist
mkdir fbxAnimation

# Copy base character (T-pose) and individual animation files
cp path/to/character_tpose.fbx fbxAnimation/BaseCharacter.fbx
cp path/to/walk_anim.fbx fbxAnimation/
cp path/to/run_anim.fbx fbxAnimation/
cp path/to/idle_anim.fbx fbxAnimation/

# Combine them into a single GLB
python src/asset_pipeline_cli.py --combine-animations --base-character BaseCharacter.fbx
```

### Animation Optimization Tips

- **FBX Preparation**: Ensure animations are properly named in your 3D software
- **Frame Rate**: Use consistent frame rates
- **Animation Length**: Keep clips concise to reduce file size
- **Bone Count**: Minimize bone count while maintaining quality
- **Keyframe Reduction**: Clean up unnecessary keyframes before export
- **Bone Hierarchy**: Ensure all animation files use the same bone structure as the base character

## License

This tool is provided as-is for asset pipeline automation. Ensure you have proper licenses for any FBX files and textures you process.
