from os import makedirs, path
import shutil
import sublime
import sublime_plugin

SUBLIME_ROOT = path.join(sublime.packages_path(), '../')
THEME_EXTENDER_FOLDER = 'Packages/User/Theme Extender/'

class ThemeExtender():
    @classmethod
    def guarantee_theme_extender_folder(cls):
        if not path.exists(THEME_EXTENDER_FOLDER):
            makedirs(THEME_EXTENDER_FOLDER)

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
        extended_filepath = path.join(THEME_EXTENDER_FOLDER,
            scheme_filename_root + '.extended' + scheme_filename_ext)
        extended_full_filepath = path.join(SUBLIME_ROOT, extended_filepath)

        # If the ThemeExtender folder doesn't already exist, create it
        ThemeExtender.guarantee_theme_extender_folder()

        # TODO: If a color scheme already exists, open the extension

        # Copy over the existing theme to the new location
        shutil.copyfile(scheme_full_filepath, extended_full_filepath)

        # TODO: Generate an extension file

        # Point the settings to the extended theme and save
        settings.set('color_scheme', extended_filepath)
        sublime.save_settings('Preferences.sublime-settings')
