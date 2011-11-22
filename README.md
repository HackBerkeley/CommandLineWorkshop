# [H@B "Productive Command-Line Hacking"](http://www.facebook.com/event.php?eid=298416103509646)

### Why Unix?
Here's a Google weeder question: recursively extract 50,000 phone numbers from a directory containing various types of files.

Browse through sh-hacking/phone-numbers. There are .log and .html files. Some directories contain sub-directories. The .html files don't seem to make any sense, so parsing them may be hard. The phone numbers are non-homogenous.

Most interviewees either write gigantic, buggy C programs or give up immediately. There's a better way.

Let's define a phone number like this: "(nnn) nnn nnnn". Now we can use the following regex to match entries: "\([0-9]{3}\) [0-9]{3} [0-9]{4}". Let's use `grep` to test things out.

	$ grep -E "\([0-9]{3}\) [0-9]{3} [0-9]{4}"                                                                                                       
	1234567890 	# Fails.
	123 456 7890 	# Fails.
	123 4567 890 	# Fails.
	(123) 456 7890 	# Works.
	(123) 456 7890 	# Works. (<- Grep prints back matching lines by default.)

Grep scans text and prints back matching results. We used the "-E" flag to enable extended regular expression matching. You can tell that the first three lines didn't match the regex, but that the fourth one did (as expected).

Check out `man grep`, you'll live much longer if you do.

Right now we can match one phone number, which is pretty cool. Matching 50,000 of them isn't much harder:

	$ grep -RE "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers

If you run this command, you'll see a lot of text flying by your screen. You can take things at your own pace by terminating grep (Ctl+C) and paging the output with `less`:

	$ grep -RE "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | less

Use the up/down arrow keys or enter to navigate through the text. Press / and type in some text to search through the stream. Press q to quit.

This is pretty interesting. You should think of the pipe symbol as a hose (it makes sense visually). It lets you direct the output of one program into the input of another. `less` can be used by itself, of course:

	$ less generate.py

Let's revisit that recursive `grep` statement. The '-R' flag makes grep walk through every file in the directory hierarchy, which is convenient when you have deeply nested files. What if we want to print the line numbers of each matching phone number? Easy:

	$ grep -REn "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | less

What if we want _just_ the number, not the cruft surrounding it? Simple enough:

	$ grep -REoh "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | less

What if we want to count the number of matching numbers? No problem:

	$ grep -RE "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | wc -l

