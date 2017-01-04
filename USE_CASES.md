# UC001 - Replacing a word with another

Replacing every matching word to a static one.

```
$ ls -AF
input

$ cat input
This is a line that is nice..
This is another line that is also nice..
Here comes the third nice one.
And the fourth nice line :D

$ regx -p nice -a p1=fancy

$ ls -AF
input .regx/

$ cat input
This is a line that is fancy..
This is another line that is also fancy..
Here comes the third fancy one.
And the fourth fancy line :D
```


# UC002 - Replacing a word in a caapture group

Replacing a capture group in a match.

```
$ ls -AF
input

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.

$ regx -p (\w+)\s+book -a p1.1=Colorful

$ ls -AF
input .regx/

$ cat input
Nice card.
Colorful book.
Colorful book.
Red card.
Purple stain.
Colorful book.
```

# UC003 - Rolling back the changes

A rollback mechanism is provided to revert the changes step by step. One step equals to one `regx` command execution.

```
$ ls -AF
input

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.

$ regx -p (\w+)\s+book -a p1.1=Colorful

$ ls -AF
input .regx/

$ cat input
Nice card.
Colorful book.
Colorful book.
Red card.
Purple stain.
Colorful book.

$ regx status
[1] - 1 file modified
[0] - original state

# by default, diff compares the current state to the original state, but it is possible to compare any two states
$ regx diff
1 file modified on 2016.01.12. 23:45:43
./input
2,3c2,3
< Green book.
< Red book.
---
> Colorful book.
> Colorful book.
6c6
< Black book.
---
> Colorful book.

$ regx rollback 0

$ regx status
[0] - original state

$ regx diff
Nothing was changed.

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.
```

# UC004 - Sending matching parts to stdout

Write matching parts to the standard output. If no target specified, the source will be printed to the standard output, and the files remain untouched.

```
$ ls -AF
input

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.

$ regx -p (\w+)\s+book -a p1.1
Green
Red
Red
Black

$ ls -AF
input

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.
```

# UC005 - Formatting the output

You can format the output with a very simple syntax. If there is no equal sign in the action, the result will be sent to the standard output. If you want to use the equal sign, you have to escape it. There are modifiers you can use to manipulate the pattern's content.

```
$ ls -AF
input

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.

$ regx -p (\w+)\s+book -a "The color of the book is {p1.1.lower}."
The color of the book is green.
The color of the book is red.
The color of the book is red.
The color of the book is black.

$ ls -AF
input

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.
```

# UC006 - Conditional execution

You can create conditions to determine when to execute the action.

```
$ ls -AF
input

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.

$ regx -p (\w+)\s+book -a "if p1.1.lower == green: "
The color of the book is green.
The color of the book is red.
The color of the book is red.
The color of the book is black.

$ ls -AF
input

$ cat input
Nice card.
Green book.
Red book.
Red card.
Purple stain.
Black book.
```


