# [H@B "Productive Command-Line Hacking"](http://www.facebook.com/event.php?eid=298416103509646)

This talk is designed to expose you to a few important Unix tools. We'll be covering grep, sed, and vim. You won't know all there is to know by the time we're done, but you will be a more effective and productive programmer. 

Let's get started. 

### Why Unix?
Here's a Google weeder question: how would you recursively extract up to 50,000 valid phone numbers from a directory containing various types of files?

Browse through CommandLineWorkshop/phone-numbers. There are .log and .html files. Some directories contain sub-directories. The .html files don't seem to make any sense, so parsing them may be hard. The phone numbers aren't homogenous. 

Most interviewees either write gigantic, buggy C programs or give up. There's a better way.

Let's define a phone number like this: "(nnn) nnn nnnn". Now we can use the following regex to match entries: "\([0-9]{3}\) [0-9]{3} [0-9]{4}". Let's use `grep` to test things out.

	$ grep -E "\([0-9]{3}\) [0-9]{3} [0-9]{4}"                                                                                                       
	1234567890 	# Fails.
	123 456 7890 	# Fails.
	123 4567 890 	# Fails.
	(123) 456 7890 	# Works.
	(123) 456 7890 	# Works. (<- Grep prints back matching lines by default.)

Grep scans text and prints back matching results. We used the "-E" flag to enable extended regular expression matching. Grep only prints back the last line because it was the only one that matched our regex.

Check out `man grep`, you'll live longer if you do.

Right now we can match one phone number, which is pretty cool. Matching 50,000 of them isn't much harder:

	$ grep -RE "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers

If you run this command, you'll see a lot of text flying by your screen. You can take things at your own pace by terminating `grep` (Ctl+C) and paging the output with `less`:

	$ grep -RE "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | less

Use the up/down arrow keys or enter to navigate through the text. Press / and type in some text to search through the stream. Press q to quit.

This is pretty interesting. You should think of the pipe symbol as a hose (it makes sense visually). It lets you direct the output of one program into the input of another. `less` can be used by itself, of course:

	$ less phone-numbers/generate.py

Let's revisit that recursive `grep` statement. The '-R' flag makes `grep` walk through every file in the directory hierarchy, which is convenient if you have deeply nested files.

What if we want to print the line numbers of each matching phone number? Easy:

	$ grep -REn "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | less

What if we want to count the number of valid phone numbers? No problem:

	$ grep -RE "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | wc -l

What if we want _just_ the number, not the cruft surrounding it? Simple enough:

	$ grep -REoh "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | less

With one `grep` statement, you can accomplish what a hardened Java veteran may take 1000 lines to implement. The `grep` solution will be faster, too, because it's authors have been optimizing it for decades.

Grep is great for corpus processing. I often use it to find function or structure definitions in my code:

	$ history | grep "grep" | wc -l
	576

(I must have run `history -c` at some point.)

### Do One Thing Well
Unix tools tend to do one thing well. This leaves you free to compose powerful commands by combining smaller, simpler ones. We saw that with `grep` and `wc`, but let's try something more challenging.

What if you wanted to convert every number of the format "(nnn) nnn nnnn" to "nnn-nnn-nnnn"? You could use `sed`, the stream editor (`man sed`!).

Let's take this step by step. We want to extract 3 groups of numbers "(1) 2 3" and reassemble them like this: "1-2-3". Here's how you substitute things in `sed`:

	$ sed 's|foo|bar|'
	foo
	bar
	bar
	bar
	barfoobar
	barbarbar

Substituting a group of numbers is trickier. The brackets we used in our first regex have a special meaning in `sed`, so we need to escape them with backslashes:

	$ sed 's|1\{2\}|22|'
	11
	22
	1
	1
	22
	22
	1111
	2211

This `sed` command replaces a cluster of '1's that repeat exactly two times with '22'. Now let's try matching the first group in a valid phone number:
	
	$ sed 's|(\([0-9]\{3\}\))|"\1"|'
	(12)
	(12)
	(123)
	"123"
	(1234)
	(1234)

We made `sed` be very picky. It will only put quotes around the first group it fully matches. We can specify groups by using escaped parens. If you want to access the kth group, simply do \k. That was the hardest part. The rest is just finding a cluster of 3 numbers, then a cluster of 4. The final command looks like this:

	$ sed 's|(\([0-9]\{3\}\)) \([0-9]\{3\}\) \([0-9]\{4\}\)|\1-\2-\3|'
	(123) 456 7890
	123-456-7890

Now that we can convert one phone number, we can convert all of them and dump the result into a file:

	$ grep -REoh "\([0-9]{3}\) [0-9]{3} [0-9]{4}" phone-numbers | sed 's|(\([0-9]\{3\}\)) \([0-9]\{3\}\) \([0-9]\{4\}\)|\1-\2-\3|' > phone-numbers/output.txt
	$ less output.txt

Et voila.
