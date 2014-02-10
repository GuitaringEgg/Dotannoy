Dotannoy
========

**Dotannoy** is a command line program that can generate a config for Dota that says a random line from a text file on key press. It also has the ability to download various data from sites that can be used to for generating configs.


Installation
-----------

Dotannoy can be run from anywhere, although storing it directly in Dota's config folder `\steamapps\common\dota 2 beta\dota\cfg` is recommended.

Example Usage
-------------

Bind all the lines in `annoy.txt` to the `P` key, which will say a random. All saved in `annoy.cfg`
```
> dotannoy
```


Bind all the lines in `jokes.txt` to the `I` key.
```
> dotannoy --input jokes.txt -say_key I
```


Say random summarys from Wikipedia articles.
```
> dotannoy --download wikipedia-random
```


Say random jokes from anti-jokes.com and bind `O` to randomise the next line.
```
> dotannoy --download anti-joke-random --ran-key O
```


Set the location of steamapps and force all lines to be used, even if they exceed the say limit in Dota 2.
```
> dotannoy --steamapps E:\steam\steamapps -force
```


To see a full list of available commands, use `-h`

