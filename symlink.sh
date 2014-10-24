ln -s "$PWD" "~/.config/sublime-text-2/Packages/theme-extender"
mkdir -p "Packages/User/Theme Extender"
theme_name="Monokai Extended Bright.extended.tmTheme.plist"
ln -s "$PWD/$theme_name" "~/.config/sublime-text-2/Packages/theme-extender/$theme_name"
