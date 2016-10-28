Using Markdown in Pagure
========================
Pagure uses [Markdown syntax highlighting](https://daringfireball.net/projects/markdown/syntax)
as the base for formatting comments in issues, pull requests, and in
Markdown files in repositories. For basic formatting, Pagure follows
common Markdown formatting, but it also has some unique syntax for more
advanced formatting. This help page helps demonstrate how to use Markdown
in Pagure.

&nbsp;

## Headers

To create headings, you will use the `#` symbol before the text. The
number of hashes before the text determines the header size.

<pre><code># header1
## header2
### header3</code></pre>

<hr />

# header 1

## header2

### header3

<hr />

&nbsp;

## Styling

You can mark up text with bold, italics, or strikethrough.

* **Style**: Bold
    * Syntax: `** **` or `__ __`
    * Example: `**This is bold text**`
    * Output: **This is bold text**
* **Style**: Italics
    * Syntax: `* *` or `_ _`
    * Example: `_This is italicized text_`
    * Output: _This is italicized text_
* **Style**: Strikethrough
    * Syntax: `~~ ~~`
    * Example: `~~This text is no longer relevant~~`
    * Output: ~~This text is no longer relevant~~
* **Style**: Bold and italics
    * Syntax: `** **` and `_ _`
    * Example: `**This text is the _most important thing ever_**`
    * Output: **This text is the _most important thing ever_**

&nbsp;

## Quoting

You can show text as being quoted with the `>` character.

<pre>Before merging this pull request, remember Clark Kent mentioned this:
> Double-check there's no reference to the Kryptonite library in the
> program since we removed that a few versions ago.</pre>

&nbsp;

Before merging this pull request, remember Clark Kent mentioned this:
> Double-check there's no reference to the Kryptonite library in the
> program since we removed that a few versions ago.

&nbsp;

## Code

You can highlight parts of a line as code or create entire code blocks in
your Markdown documents. Text inside of backticks will not be formatted.

<pre>When running the program for the first time, use `superman --initialize`.</pre>

When running the program for the first time, use `superman --initialize`.

&nbsp;

To format multiple lines of code into its own block, you will need to use
raw HTML with the &lsaquo;pre&rsaquo;&lsaquo;/pre&rsaquo; tags.

<pre>Install the needed system libraries:
&lsaquo;pre&rsaquo;
sudo dnf install git python-virtualenv libgit2-devel \
                 libjpeg-devel gcc libffi-devel redhat-rpm-config
&lsaquo;pre&rsaquo;</pre>

&nbsp;

Install the needed system libraries:
<pre>
sudo dnf install git python-virtualenv libgit2-devel \
                 libjpeg-devel gcc libffi-devel redhat-rpm-config
</pre>

&nbsp;

## Hyperlinks

Need to embed a link to somewhere else? No problem! You can create an in-
line link by wrapping the text in `[ ]` and appending the the URL in
parentheses `( )` immediately after.

`Pagure is used by the [Fedora Project](https://fedoraproject.org).`

Pagure is used by the [Fedora Project](https://fedoraproject.org).

&nbsp;

## Lists

You can make unordered lists spanning multiple lines with either `-` or
`*`.

<pre>* Superman
* Batman
    * Protector of Gotham City!
* Superwoman
* Harley Quinn
    * Something on this list is unlike the others...</pre>

* Superman
* Batman
    * Protector of Gotham City!
* Superwoman
* Harley Quinn
    * Something on this list is unlike the others...

&nbsp;

You can make ordered lists by preceding each line with a number.

<pre>1. Superman
2. Batman
    1. Protector of Gotham City!
    2. He drives the Batmobile!
3. Superwoman
4. Harley Quinn
    1. Something on this list is unlike the others...
    2. Somebody evil lurks on this list!</pre>

1. Superman
2. Batman
    1. Protector of Gotham City!
    2. He drives the Batmobile!
3. Superwoman
4. Harley Quinn
    1. Something on this list is unlike the others...
    2. Somebody evil lurks on this list!

&nbsp;

## Tagging users

You can tag other users on Pagure to send them a notification about an
issue or pull request. To tag a user, use the `@` symbol followed by their
username. Typing the `@` symbol in a comment will bring up a list of users
that match the username. The list searches as you type. Once you see the
name of the person you are looking for, you can click their name to
automatically complete the tag.

`@jflory7, could you please review this pull request and leave feedback?`

[@jflory7](https://pagure.io/user/jflory7), could you please review this
pull request and leave feedback?

&nbsp;

## Tagging issues or pull requests

In a comment, you can automatically link a pull request or issue by its
number. To link it, use the `#` character followed by its number. Like
with tagging users, Pagure will provide suggestions for issues or pull
requests as you type the number. You can select the issue in the drop-down
to automatically tag the issue or pull request.

&nbsp;

## Emoji

Pagure natively supports emoji characters. To use emoji, you can use two
colons wrapped around the emoji keyword (`:emoji:`). Typing a colon by
itself will bring up a list of suggested emoji with a small preview. If
you see the one you're looking for, you can click it to automatically
complete the emoji.

`I reviewed the PR and it looks good to me. :+1: Good to merge! :clapper:`

I reviewed the PR and it looks good to me. :+1: Good to merge! :clapper:

&nbsp;

## Improve this documentation!

Notice anything that can be improved in this documentation? Find a
mistake? You can improve this page! Find it in the official [Pagure
repository](https://pagure.io/pagure/blob/master/f/doc/usage/markdown.md).
