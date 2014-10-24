ln -s "$PWD" "$HOME/.config/sublime-text-2/Packages/Theme Extender"
mkdir -p "$HOME/.config/sublime-text-2/Packages/User/Theme Extender"
theme_name="Monokai Extended Bright.extended.tmTheme.plist"
ln -s "$PWD/$theme_name" "$HOME/.config/sublime-text-2/Packages/User/Theme Extender/$theme_name"
