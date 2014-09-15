**C++NamespaceTool** is a simple C++ namespace refactoring package for [Sublime Text 3][sublime].

## Installation ##

**C++NamespaceTool** can be installed using [Package Control][package_control] with the **Install Package** option.

## Description ##

In C++ programming, writing `using namespace std` is considered a bad practice. The preferred way is to either explicitly state somewhere at the top which functions, classes, and types are used with `using namespace::word` statements or to explicitly type the namespace (usually `std`) at each occurence of the word. Sometimes, starting with one of the options, the programmer may want to convert to the other option. C++NamespaceTool is designed with the goal of automating this task.

## Usage ##

The shortcut is `Ctrl-Shift-R` on all platforms (`Right-click->Refactor namespace` should also appear and do exactly the same work when C++ files are open). When `using` statements are selected, activating the tool will convert the selected `using` statements to inline `namespace::word` format. When inline `namespace::word` items are selected, activating the tool will convert all occurences of the selected items into just `word` and put a `using` statement at the top of the file.

### Example usage: ###

Using the keyboard shortcut:

![](http://myurtoglu.github.io/NamespaceTool/images/refactor_keyboard.gif)

Using the right-click context menu:

![](http://myurtoglu.github.io/NamespaceTool/images/refactor_mouse.gif)

## Configuration ##

You can add namespaces besides *std* (warning: sub-namespaces are not supported at the moment), and file extensions for the right-click menu item to appear (most frequently seen file extensions are already in the configuration file) here: `Preferences -> Package Settings -> C++NamespaceTool->Settings`.

You can also change the shortcut key here: `Preferences -> Package Settings -> C++NamespaceTool->Key Bindings`.

## Contact ##

You can leave bug reports, feature requests, or comments using [the issues section][issues].

## Thanks! ##

Thank you for your interest in this package!

[issues]: https://github.com/myurtoglu/NamespaceTool/issues
[package_control]: http://wbond.net/sublime_packages/package_control
[sublime]: http://www.sublimetext.com/3
