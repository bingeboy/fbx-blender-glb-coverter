# Blender Asset Pipeline: FBX to GLB Converter

A comprehensive Blender-based pipeline for converting FBX files to GLB format, optimized for Godot 4.4. This toolkit provides two conversion workflows: individual FBX conversion and animation combining for character assets.

## Features

- **Individual FBX Conversion**: Convert standalone FBX models to GLB format
- **Animation Combining**: Merge multiple FBX animation files with a base character model into a single GLB
- **Godot 4.4 Optimization**: Export settings optimized for Godot 4.4 compatibility
- **Batch Processing**: Automated pipeline for processing multiple assets
- **Armature Preservation**: Maintains proper bone structure and skinning data
- **Texture & Material Support**: Preserves all visual assets and PBR materials

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
fbx-blender-glb-converter/
├── fbx/                        # Input folder for individual FBX models
│   ├── model_name_1/           # Each model gets its own folder
│   │   ├── model.fbx           # FBX file
│   │   ├── texture.png         # Texture files
│   │   └── normal.png          # Additional textures
│   └── model_name_2/
│       ├── character.fbx
│       └── skin.jpg
├── fbxAnimation/               # Input folder for character animations
│   ├── Ch20_nonPBR.fbx        # Base character model (T-pose)
│   ├── Running.fbx            # Animation files
│   ├── Left Strafe.fbx
│   └── Right Strafe.fbx
├── glb/                        # Output folder (auto-created)
│   ├── model_name_1.glb        # Individual converted GLB files
│   ├── model_name_2.glb
│   └── Ch20_with_animations.glb # Combined character with animations
├── fbx_to_glb_pipeline.py      # Individual FBX conversion script
├── fbx_animation_combiner.py   # Animation combining script
├── run_pipeline.sh             # Execution wrapper
└── README.md                   # This file
```

## Usage

### Individual FBX Conversion

For converting standalone FBX models with textures:

#### Method 1: Using the Shell Script
```bash
# Make the script executable (first time only)
chmod +x run_pipeline.sh

# Run the pipeline
./run_pipeline.sh
```

#### Method 2: Direct Blender Command
```bash
blender --background --python fbx_to_glb_pipeline.py
```

#### Method 3: Using Full Blender Path (if not in PATH)
```bash
# macOS
/Applications/Blender.app/Contents/MacOS/Blender --background --python fbx_to_glb_pipeline.py

# Windows
"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe" --background --python fbx_to_glb_pipeline.py
```

### Animation Combining

For combining a character model with multiple animation files:

1. **Prepare your files** in the `fbxAnimation/` directory:
   - Place your base character model (T-pose) as `Ch20_nonPBR.fbx`
   - Add animation files: `Running.fbx`, `Left Strafe.fbx`, `Right Strafe.fbx`, etc.

2. **Run the animation combiner**:
   ```bash
   blender --background --python fbx_animation_combiner.py
   ```

3. **Output**: Creates `glb/Ch20_with_animations.glb` with all animations combined

#### Animation Requirements
- FBX format files
- 30fps animations (or any consistent framerate)
- Skinned meshes with armature
- All animation files should use the same bone structure as the base character

## How It Works

### Individual Conversion Pipeline
1. **Scans** the `fbx/` directory for model folders
2. **Imports** each FBX file found in the folders
3. **Preserves** all textures and materials
4. **Exports** as GLB with Godot 4.4 optimized settings
5. **Saves** converted files to the `glb/` folder

### Animation Combining Pipeline
1. **Imports** the base character model (T-pose) from `fbxAnimation/`
2. **Identifies** the armature and bone structure
3. **Processes** each animation FBX file sequentially
4. **Extracts** animation data and merges with base character
5. **Exports** a single GLB with all animations as separate action clips
6. **Optimizes** for Godot 4.4 AnimationPlayer compatibility

## Supported Features

- ✅ FBX model import with textures
- ✅ Material preservation and PBR compatibility
- ✅ Texture coordinate mapping
- ✅ Normal maps and surface data
- ✅ Individual FBX to GLB conversion
- ✅ **Multi-animation combining** (NEW)
- ✅ Armature and bone structure preservation
- ✅ Animation action separation for Godot
- ✅ Batch processing of multiple models
- ✅ Godot 4.4 compatibility
- ✅ Automatic Y-up coordinate conversion
- ✅ Optimized joint influences (max 4 per vertex)

## GLB Export Settings

The pipeline uses these optimized settings for Godot 4.4:

- **Format**: GLB (binary)
- **Textures**: Preserved with automatic format detection
- **Materials**: Full export with PBR compatibility
- **Coordinates**: Y-up (Godot standard)
- **Animations**: Multiple actions exported as separate clips
- **NLA Strips**: Enabled for proper animation separation
- **Joint Influences**: Limited to 4 per vertex (Godot standard)
- **Animation Optimization**: Size-optimized keyframes
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

**"No armature found in base character"** (Animation Combining)
- Ensure your base character FBX contains a proper armature/skeleton
- Verify the character is rigged and skinned correctly
- Check that the base file is named `Ch20_nonPBR.fbx` (or update the script)

**"Animation actions not showing in Godot"**
- Verify animations were properly combined by checking the GLB file size
- In Godot, check the AnimationPlayer node for available animation clips
- Ensure all animation FBX files have compatible bone structures

**"Permission denied"**
- Make sure the script has execute permissions: `chmod +x run_pipeline.sh`
- Check that you have write permissions in the project directory

### Debugging

For more detailed output, run Blender with verbose logging:
```bash
blender --background --python fbx_to_glb_pipeline.py --debug
```

## Adding New Assets

### Adding Individual Models

1. Create a new folder in `fbx/` with your model name
2. Place the FBX file and all textures in that folder
3. Run the individual conversion pipeline
4. Check `glb/` for the converted file

Example:
```bash
mkdir fbx/my_character
cp path/to/character.fbx fbx/my_character/
cp path/to/texture.png fbx/my_character/
./run_pipeline.sh
```

### Adding Character Animations

1. Place your base character (T-pose) in `fbxAnimation/` as `Ch20_nonPBR.fbx`
2. Add animation files to the same directory: `Running.fbx`, `Walking.fbx`, etc.
3. Run the animation combiner
4. Check `glb/` for `Ch20_with_animations.glb`

Example:
```bash
cp path/to/base_character.fbx fbxAnimation/Ch20_nonPBR.fbx
cp path/to/run_anim.fbx fbxAnimation/Running.fbx
cp path/to/walk_anim.fbx fbxAnimation/Walking.fbx
blender --background --python fbx_animation_combiner.py
```

## Godot 4.4 Integration

The generated GLB files are ready to use in Godot 4.4:

### Individual Models
1. Copy GLB files to your Godot project's asset folder
2. Godot will automatically import them
3. Materials and textures should be preserved
4. No additional configuration needed

### Animated Characters
1. Import the combined GLB file into your Godot project
2. Add an AnimationPlayer node to your character scene
3. The AnimationPlayer will automatically detect all animation clips:
   - `Running`
   - `Left Strafe`
   - `Right Strafe`
   - (Plus any other animations you included)
4. Play animations using: `$AnimationPlayer.play("Running")`

### Animation Example in Godot
```gdscript
# In your character script
extends CharacterBody3D

@onready var animation_player = $AnimationPlayer

func _ready():
    # Play the running animation on start
    animation_player.play("Running")

func _input(event):
    if event.is_action_pressed("ui_right"):
        animation_player.play("Right Strafe")
    elif event.is_action_pressed("ui_left"):
        animation_player.play("Left Strafe")
```

## Performance Tips

- Keep texture sizes reasonable (1024x1024 or 2048x2048 for most use cases)
- Use power-of-2 texture dimensions when possible
- Consider using PNG for textures with transparency, JPG for opaque textures
- Remove unused materials and textures from FBX files before conversion

## License

This tool is provided as-is for asset pipeline automation. Ensure you have proper licenses for any FBX files and textures you process.