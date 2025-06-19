#!/usr/bin/env python3
"""
Asset Pipeline CLI - Dynamic FBX to GLB Converter
Usage: python asset_pipeline_cli.py [options]
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional

class AssetPipelineCLI:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.fbx_dir = self.project_root / "fbx"
        self.fbx_anim_dir = self.project_root / "fbxAnimation"
        self.glb_dir = self.project_root / "glb"
        self.pipeline_script = self.script_dir / "fbx_to_glb_pipeline.py"
        self.animation_combiner_script = self.script_dir / "fbx_animation_combiner.py"
    
    def discover_fbx_folders(self) -> List[Path]:
        """Dynamically discover all folders in the fbx directory"""
        if not self.fbx_dir.exists():
            print(f"Error: FBX directory not found: {self.fbx_dir}")
            return []
        
        folders = [item for item in self.fbx_dir.iterdir() if item.is_dir()]
        return sorted(folders)
    
    def list_assets(self) -> None:
        """List all available assets in the fbx directory"""
        folders = self.discover_fbx_folders()
        
        if not folders:
            print("No asset folders found in fbx directory")
            return
        
        print(f"Available assets in {self.fbx_dir}:")
        for i, folder in enumerate(folders, 1):
            fbx_files = list(folder.glob("*.fbx"))
            texture_files = list(folder.glob("*.png")) + list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg"))
            
            print(f"  {i:2d}. {folder.name}")
            print(f"      FBX files: {len(fbx_files)}")
            print(f"      Textures: {len(texture_files)}")
            
            # Show GLB status
            glb_file = self.glb_dir / f"{folder.name}.glb"
            if glb_file.exists():
                print(f"      Status: ✓ GLB exists")
            else:
                print(f"      Status: ✗ No GLB")
            print()
    
    def check_blender(self) -> bool:
        """Check if Blender is available"""
        try:
            result = subprocess.run(["blender", "--version"], 
                                 capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def run_conversion(self, folders: Optional[List[str]] = None, verbose: bool = False) -> None:
        """Run the conversion pipeline"""
        if not self.check_blender():
            print("Error: Blender not found in PATH")
            print("Please install Blender or add it to your PATH")
            print("\nOn macOS, you might need to create a symlink:")
            print("ln -s /Applications/Blender.app/Contents/MacOS/Blender /usr/local/bin/blender")
            return
        
        if not self.pipeline_script.exists():
            print(f"Error: Pipeline script not found: {self.pipeline_script}")
            return
        
        # Ensure GLB directory exists
        self.glb_dir.mkdir(exist_ok=True)
        
        available_folders = self.discover_fbx_folders()
        if not available_folders:
            return
        
        # Filter folders if specific ones requested
        if folders:
            target_folders = []
            for folder_name in folders:
                matching_folders = [f for f in available_folders if f.name == folder_name]
                if matching_folders:
                    target_folders.extend(matching_folders)
                else:
                    print(f"Warning: Folder '{folder_name}' not found in fbx directory")
            
            if not target_folders:
                print("No valid folders to process")
                return
        else:
            target_folders = available_folders
        
        print(f"Processing {len(target_folders)} asset folder(s)...")
        if verbose:
            print("Target folders:", [f.name for f in target_folders])
        
        # Create a temporary script that processes only specific folders
        temp_script_content = f'''#!/usr/bin/env python3
import sys
sys.path.append(r"{self.script_dir}")
from fbx_to_glb_pipeline import process_fbx_folder, clear_scene
from pathlib import Path

def main():
    project_root = Path(r"{self.project_root}")
    glb_dir = project_root / "glb"
    glb_dir.mkdir(exist_ok=True)
    
    target_folders = {[str(f) for f in target_folders]}
    
    successful = 0
    failed = 0
    
    for folder_path in target_folders:
        folder = Path(folder_path)
        print(f"\\nProcessing: {{folder.name}}")
        
        if process_fbx_folder(folder, glb_dir):
            successful += 1
            print(f"✓ Successfully converted {{folder.name}}")
        else:
            failed += 1
            print(f"✗ Failed to convert {{folder.name}}")
    
    print(f"\\n--- Summary ---")
    print(f"Successful: {{successful}}")
    print(f"Failed: {{failed}}")
    print(f"Total: {{len(target_folders)}}")

if __name__ == "__main__":
    main()
'''
        
        temp_script = self.project_root / "temp_pipeline.py"
        try:
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(temp_script_content)
            
            # Run Blender with the temporary script
            cmd = ["blender", "--background", "--python", str(temp_script)]
            
            if verbose:
                print(f"Running command: {' '.join(cmd)}")
                result = subprocess.run(cmd)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
                if result.stderr and result.returncode != 0:
                    print("Errors:", result.stderr)
            
            print("\nConversion completed!")
        
        finally:
            # Clean up temporary script
            if temp_script.exists():
                temp_script.unlink()
    
    def combine_animations(self, base_character: str = "Ch20_nonPBR.fbx", verbose: bool = False) -> None:
        """Combine FBX animations into a single GLB file"""
        if not self.check_blender():
            print("Error: Blender not found in PATH")
            print("Please install Blender or add it to your PATH")
            print("\nOn macOS, you might need to create a symlink:")
            print("ln -s /Applications/Blender.app/Contents/MacOS/Blender /usr/local/bin/blender")
            return
        
        if not self.animation_combiner_script.exists():
            print(f"Error: Animation combiner script not found: {self.animation_combiner_script}")
            return
        
        if not self.fbx_anim_dir.exists():
            print(f"Error: FBX Animation directory not found: {self.fbx_anim_dir}")
            print(f"Please create the directory: {self.fbx_anim_dir}")
            print("And place your base character and animation FBX files there.")
            return
        
        # Ensure GLB directory exists
        self.glb_dir.mkdir(exist_ok=True)
        
        # Check if base character exists
        base_fbx = self.fbx_anim_dir / base_character
        if not base_fbx.exists():
            print(f"Error: Base character file not found: {base_fbx}")
            print(f"Available FBX files in {self.fbx_anim_dir}:")
            fbx_files = list(self.fbx_anim_dir.glob("*.fbx"))
            if fbx_files:
                for fbx_file in fbx_files:
                    print(f"  - {fbx_file.name}")
                print(f"\nTry specifying one of these as the base character:")
                print(f"python asset_pipeline_cli.py --combine-animations --base-character FILENAME.fbx")
            else:
                print("  No FBX files found!")
            return
        
        # Count animation files
        animation_files = [f for f in self.fbx_anim_dir.glob("*.fbx") if f.name != base_character]
        if not animation_files:
            print(f"No animation files found (excluding base character {base_character})")
            return
        
        print(f"Combining animations from {len(animation_files)} files with base character {base_character}")
        if verbose:
            print("Animation files:")
            for anim_file in animation_files:
                print(f"  - {anim_file.name}")
        
        # Create a temporary script that processes the animation combination
        temp_script_content = f'''#!/usr/bin/env python3
import sys
sys.path.append(r"{self.script_dir}")
from fbx_animation_combiner import process_fbx_animation_folder
from pathlib import Path

def main():
    fbx_anim_dir = Path(r"{self.fbx_anim_dir}")
    glb_dir = Path(r"{self.glb_dir}")
    base_character = r"{base_character}"
    
    success = process_fbx_animation_folder(fbx_anim_dir, glb_dir, base_character)
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
'''
        
        temp_script = self.project_root / "temp_animation_combiner.py"
        try:
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(temp_script_content)
            
            # Run Blender with the temporary script
            cmd = ["blender", "--background", "--python", str(temp_script)]
            
            if verbose:
                print(f"Running command: {' '.join(cmd)}")
                result = subprocess.run(cmd)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
                if result.stderr and result.returncode != 0:
                    print("Errors:", result.stderr)
            
            if result.returncode == 0:
                print("\nAnimation combination completed successfully!")
            else:
                print("\nAnimation combination failed!")
        
        finally:
            # Clean up temporary script
            if temp_script.exists():
                temp_script.unlink()

def main():
    parser = argparse.ArgumentParser(
        description="Asset Pipeline CLI - Convert FBX assets to GLB format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python asset_pipeline_cli.py --list                              # List all available assets
  python asset_pipeline_cli.py --convert                           # Convert all assets
  python asset_pipeline_cli.py --convert male_casual               # Convert specific asset
  python asset_pipeline_cli.py --convert male_casual female_casual --verbose
  python asset_pipeline_cli.py --combine-animations                # Combine animations (default base: Ch20_nonPBR.fbx)
  python asset_pipeline_cli.py --combine-animations --base-character MyChar.fbx --verbose
        """
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available assets in the fbx directory"
    )
    
    parser.add_argument(
        "--convert", "-c",
        nargs="*",
        metavar="FOLDER",
        help="Convert assets to GLB. If no folder names specified, converts all."
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--combine-animations",
        action="store_true",
        help="Combine FBX animations from fbxAnimation directory into a single GLB"
    )
    
    parser.add_argument(
        "--base-character",
        default="Ch20_nonPBR.fbx",
        help="Base character FBX file for animation combining (default: Ch20_nonPBR.fbx)"
    )
    
    args = parser.parse_args()
    
    cli = AssetPipelineCLI()
    
    if args.list:
        cli.list_assets()
    elif args.convert is not None:
        folders = args.convert if args.convert else None
        cli.run_conversion(folders, args.verbose)
    elif args.combine_animations:
        cli.combine_animations(args.base_character, args.verbose)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()