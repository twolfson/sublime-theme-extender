from os import makedirs, path
import shutil
import sublime
import sublime_plugin

SUBLIME_ROOT = path.normpath(path.join(sublime.packages_path(), '..'))
THEME_EXTENDER_FILEPATH = path.join('Packages', 'User', 'Theme Extender')
THEME_EXTENDER_FULL_FILEPATH = path.join(SUBLIME_ROOT, THEME_EXTENDER_FILEPATH)

class ThemeExtender():
    @classmethod
    def guarantee_theme_extender_directory(cls):
        """Guarantee the theme extender directory exists so we can write files to it"""
        if not path.exists(THEME_EXTENDER_FULL_FILEPATH):
            makedirs(THEME_EXTENDER_FULL_FILEPATH)

class ThemeExtenderExtendThemeCommand(sublime_plugin.WindowCommand):
    def run(self):
        """Load existing theme, open an extension for it, enter extending mode"""
        # Load our settings and color scheme
        settings = sublime.load_settings('Preferences.sublime-settings')
        scheme_filepath = settings.get('color_scheme')
        scheme_full_filepath = path.join(SUBLIME_ROOT, scheme_filepath)

        # Determine the filename and its parts
        # e.g. 'Packages/Monokai Extended/Monokai Extended Bright.tmTheme' -> 'Monokai Extended Bright', '.tmTheme'
        # TODO: Move theme filepath resolution into class method
        scheme_filename = path.basename(scheme_filepath)
        [scheme_filename_root, scheme_filename_ext] = path.splitext(scheme_filename)

        # Generate our new filepath
        # e.g. 'Packages/User/ThemeExtender/Monokai Extended Bright.extended.tmTheme'
        extended_filepath = path.join(THEME_EXTENDER_FILEPATH,
            scheme_filename_root + '.extended' + scheme_filename_ext)
        extended_full_filepath = path.join(SUBLIME_ROOT, extended_filepath)

        # If the theme was already in the Theme Extender directory, reset it to the current scheme
        if scheme_filepath.startswith(THEME_EXTENDER_FILEPATH):
            extended_filepath = scheme_filepath
            extended_full_filepath = scheme_full_filepath

        # If the ThemeExtender directory doesn't already exist, create it
        ThemeExtender.guarantee_theme_extender_directory()

        # If the color scheme doesn't exist
        if not path.exists(extended_full_filepath):
            # Copy over the existing theme to the new location
            shutil.copyfile(scheme_full_filepath, extended_full_filepath)

            # Point the settings to the extended theme and save
            settings.set('color_scheme', extended_filepath)
            sublime.save_settings('Preferences.sublime-settings')

        # Open a buffer to the file
        # DEV: If it is new, the buffer will save it automagically
        # e.g. 'Packages/User/ThemeExtender/Monokai Extended Bright.extended.tmTheme.plist'
        extension_filepath = path.join(THEME_EXTENDER_FILEPATH,
            scheme_filename_root + '.extended' + scheme_filename_ext + '.plist')
        extension_full_filepath = path.join(SUBLIME_ROOT, extension_filepath)
        # TODO: On fresh buffer add in explanation comments and reference to original file so we an extend it
        view = self.window.open_file(extension_full_filepath)

        # If the view is rendering plain text, change to XML
        if view.settings().get('syntax') == path.join('Packages', 'Text', 'Plain text.tmLanguage'):
            view.set_syntax_file(path.join('Packages', 'XML', 'XML.tmLanguage'))

class ThemeExtenderListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        """When a save occurs to a ThemeExtender extension, re-extend the theme"""
        # If we are in the wrong directory, exit early
        filepath = view.file_name()
        if not filepath.startswith(THEME_EXTENDER_FULL_FILEPATH):
            return

        # If the file is not an extension, exit early
        filename = path.basename(filepath)
        if not filename.endswith('.plist'):
            return

        print "you are an extension. yis."

        # TODO: Attempt to load the file as a plist

        # TODO: If we cannot, complain to the user

        # TODO: Determine the source theme

        # TODO: Attempt to load source theme

        # TODO: If we cannot, complain to the user

        # TODO: Extend the extensions onto the theme

        # TODO: Save the updated theme
