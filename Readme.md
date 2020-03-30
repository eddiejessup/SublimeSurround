# Surround: A package for Sublime Text 3

Change or delete the characters surrounding your selection.

## Intent

To do things like:

- Swap `"` quotes for `'`
- Remove unused parantheses

Those are the main uses I can think of, but they're pretty common.

## Installation

### Recommended option: Use the Package Control plugin

- Follow [these instructions](http://wbond.net/sublime_packages/package_control) to install the Package Control plugin
- In Sublime Text, pick `Package Control: Install Package` from the command palette, then search for and select the package `Surround`.

### Alternative option: Clone the repository

Clone the repository containing the plugin into `Sublime Text 3/Packages`, whose location depends on your operating system:

MacOS:

`git clone git://github.com/eddiejessup/Surround.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Surround`

Windows:

`git clone git://github.com/eddiejessup/Surround.git "%APPDATA%\Sublime Text 3\Packages\Surround"`

Linux:

`git clone git://github.com/eddiejessup/Surround.git ~/.config/sublime-text-3/Packages/Surround`

## Usage

TODO: Test and Document 'add surroundings'

### Low-level functionality

The package provides the command, `surround_change_with_prompt`. This asks for two inputs: the character to search for (the 'match'), and the character to swap it with (the 'replacement'). It will then look up a pair of characters for the match character, and look for the nearest enclosing pair of those characters, and swap them with the pair of characters represented by the replacement character.

There is also the `surround_delete_with_prompt` command, that only asks for a match character, and which simply removes the corresponding nearest pair.

### Command-palette interface

The plugin adds entries to the command palette called `Surround: {Change,Delete} surroundings`.

### Menu interface

The plugin adds menu entries under `Selection/{Change,Delete} surroundings`.

### Key-binding interface

The plugin binds a shortcut, `"ctrl+k", "ctrl+c"` to run the `surround_change_with_prompt` command, or `"ctrl+k", "ctrl+shift+c"` to run the `surround_delete_with_prompt` command. On MacOS, the "super" (command) key is bound instead of the "ctrl" key.

You can also define a keyboard shortcut which runs the commands with particular arguments, by binding a key pattern to the `surround_change` command with the arguments `match` and `replacement` specifying your intended find/replace characters. To delete surroundings, just set the replacement to an empty string.

For example, to add shortcuts to replace `'` with `"` and vice versa, you might add the key bindings:

```
{
    "keys": ["super+k", "super+'"],
    "command": "surround_change",
    "args": { "match": "\"", "replacement": "'" }
},
{
    "keys": ["super+k", "super+shift+'"],
    "command": "surround_change",
    "args": { "match": "'", "replacement": "\"" }
}
```

## Configuration

You can edit the pair mappings, and plugin settings through the menu, at `Sublime Text/Preferences/Package Settings/Surround`.

## Author & Contributors

This is an updated and tweaked version of a plugin by [jcartledge](https://github.com/jcartledge), so thanks to them. I was too lazy to properly contribute to that plugin, so I forked it, sorry.

- [Elliot Marsden](https://github.com/eddiejessup)
- [jcartledge](https://github.com/jcartledge/sublime-surround)

## License

MIT License
