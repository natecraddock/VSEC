"""
VSE Crossfades
Copyright (C) 2015 Nathan Craddock

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

bl_info = {
    "name": "VSE Crossfades",
    "author": "Nathan Craddock",
    "version": (1, 0, 0),
    "blender": (2, 7, 3),
    "location": "Object Mode >> Tool Shelf >> VSE Crossfade (Tab)",
    "description": "Allows the user to select a directory, and it adds the files in the directory to the VSE with crossfades.",
    "category": "Tools"
}

import bpy

class vseCrossfadesPanel(bpy.types.Panel):
    """VSE Crossfade Addon Panel"""
    bl_category = "VSE Crossfade"
    bl_idname = "tools.vse_crossfade_panel"
    bl_context = "objectmode"
    bl_label = "VSE Crossfades"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(context.scene, "vsec_crossfade_length")
        row = layout.row()
        row.operator("tools.vse_crossfade_addon")
        

class vseCrossfades(bpy.types.Operator):
    """Add files to the Video Sequence Editor using the values above"""
    bl_idname = "tools.vse_crossfade_addon"
    bl_label = "Add files to VSE"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        strip1 = "C:\\Users\\Nate\\Desktop\\Gavin Harrison and Justin Rivest Raining Men Intro.mov"
        strip2 = "C:\\Users\\Nate\\Desktop\\render0001-0250.mp4"
        strip3 = "C:\\Users\\Nate\\Desktop\\Gavin Harrison and Justin Rivest Raining Men Intro.mov"
        strip4 = "C:\\Users\\Nate\\Desktop\\render0001-0250.mp4"

        frame_offset = 10

        strips = []
        strips.append(strip1)
        strips.append(strip2)
        strips.append(strip3)
        strips.append(strip4)

        print()

        #Add the strips
        bpy.context.area.type = 'SEQUENCE_EDITOR'
        bpy.context.scene.sequence_editor_clear()

        offset = 1
        channel_offset = 1
        strip_number = 1

        for i in range(0, len(strips)):
            
            #Change the channel offset
            if strip_number % 2 == 1:
                channel_offset = 1
            else:
                channel_offset = 2
            
            
            print(strips[i])
            print(offset)
            bpy.ops.sequencer.movie_strip_add(filepath = strips[i], frame_start = offset)
            
            #Make into meta strip
            bpy.ops.sequencer.meta_make()
            
            bpy.context.selected_sequences[0].name = str(strip_number)
            
            #Alternate what channel to make the strip on for the crossfade to work.
            bpy.context.selected_sequences[0].channel = channel_offset
            
            #crossfade
            if len(bpy.context.sequences) > 1:
                print("adding crossfade")
                
                #Deselect everything
                bpy.ops.sequencer.select_all()
                
                bpy.data.scenes["Scene"].sequence_editor.sequences_all[str(strip_number)].select = True
                bpy.data.scenes["Scene"].sequence_editor.sequences_all[str(strip_number - 1)].select = True
                
                bpy.ops.sequencer.effect_strip_add(type='CROSS')
                
                bpy.ops.sequencer.select_all()
                
                bpy.data.scenes["Scene"].sequence_editor.sequences_all[str(strip_number)].select = True
            
            
            #Add the length of the current stip to the offset
            offset += bpy.context.selected_sequences[0].frame_final_duration - 10
            
            strip_number += 1

            
        #Set the length of the timeline to the duration
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.frame_end = bpy.context.sequences[0].frame_final_duration

        bpy.context.area.type = 'VIEW_3D'
        
def register():
    bpy.utils.register_class(vseCrossfades)
    bpy.utils.register_class(vseCrossfadesPanel)
    bpy.types.Scene.vsec_crossfade_length = bpy.props.IntProperty(name="Crossfade Length", description="Length in frames of the crossfade", default=10, min = 1)

def unregister():
    bpy.utils.unregister_class(vseCrossfades)
    bpy.utils.unregister_class(vseCrossfadesPanel)
    
if __name__ == "__main__":
    register()