Dotannoy
========

**Dotannoy** is a command line program that can generate a config for Dota that says a random line from a text file on key press. It also has the ability to download lines from various sites that can be used to for generating configs.


Installation
-----------

You can download the latest version from the [releases](https://github.com/GuitaringEgg/Dotannoy/releases) section. You can also grab the source and run Dotannoy.py directly. The executable is just the scripts packed with PyInstaller for convience.

Dotannoy can be run from anywhere, although storing it directly in Dota's config folder `\steamapps\common\dota 2 beta\dota\cfg` is recommended.

If you do run it from outwidth Dota's config folder, and your Steam install is in a non-standard location, you'll need to tell the program where it's located.

Say Steam was installed at `E:\Steam\steamapps`, you'd use the following to set it:
```
> dotannoy --steamapps E:\Steam\Steamapps
````

Which will store the Steam location in a config file. You are free to run all the commands as normal.


Example Usage
-------------

This is the default behaviour. Bind all the lines in `annoy.txt` to the `P` key, which will say a random line from that file. All saved in `annoy.cfg`
```
> dotannoy
```


Bind all the lines in `jokes.txt` to the `I` key.
```
> dotannoy --input jokes.txt -say_key I
```


Say random summary from Wikipedia articles.
```
> dotannoy --download wikipedia-random
```


Say random jokes from theoatmeal.com and bind `O` to randomise the next line.
```
> dotannoy --download oatmeal-random --ran-key O
```


Force all lines to be used, even if they exceed the say limit in Dota 2.
```
> dotannoy -force
```


To see a full list of available commands, use `-h`

Future
-----------
- Support other source games
- Support other sites
