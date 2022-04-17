A Python script to capture the NHK Radio streaming service (Radiru-Radiru).

# License

BSD-3-Clause

# Requirements
 - requests

# Usage

1. A list of available `site_id` and `program_name` are printed running the script without arguments lists.
```zsh
% python radiru2.py
```
2. Save the output to a text file or inspect the output to find `site_id`.
3. Edit the output or create a text file containg a list of `site_id`.
4. Run the script with text files of `site_id`. For example
```zsh
% python radiru2.py music.txt lang.txt
```
