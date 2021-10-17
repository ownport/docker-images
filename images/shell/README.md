# Shells

## Linux commands alternatives

- [bat](https://github.com/sharkdp/bat) supports syntax highlighting for a large number of programming and markup languages
- [Z](https://github.com/rupa/z) lets you quickly jump around your filesystem. It memorizes the folders that you visit, and after a short learning time, you can move between them using `z path_of_the_folder_name`
- [zoxide](https://github.com/ajeetdsouza/zoxide) is a blazing fast replacement for your `cd` command, inspired by `z` and `autojump`. It keeps track of the directories you use most frequently, and uses a ranking algorithm to navigate to the best match.
- [fd](https://github.com/sharkdp/fd) Like the `find` command but much simpler to use, faster, and comes with good default settings.
- [ripgrep](https://github.com/BurntSushi/ripgrep) In a similar manner to `fd` mentioned above, `ripgrep` is an alternative to the `grep` command - much faster one, with sane defaults and colorized output.
- [exa](https://the.exa.website/) A modern replacement for `ls`.
    - https://github.com/ogham/exa
- [autojump](https://github.com/wting/autojump) a faster way to navigate your filesystem
- [Fasd](https://github.com/clvv/fasd) is a command-line productivity booster. `Fasd` offers quick access to files and directories for POSIX shells. It is inspired by tools like `autojump`, `z` and `v`. `Fasd` keeps track of files and directories you have accessed, so that you can quickly reference them in the command line.
- [broot](https://github.com/Canop/broot) A new way to see and navigate directory trees
    - https://dystroy.org/broot/

## Tools

- [Starship](https://starship.rs/) The minimal, blazing-fast, and infinitely customizable prompt for any shell
- [fzf](https://github.com/junegunn/fzf) It’s a general-purpose tool that lets you find files, commands in the history, processes, git commits, and more using a fuzzy search.
- [NCurses Disk Usage](https://dev.yorhel.nl/ncdu) Ncdu is a disk usage analyzer with an ncurses interface.
- [McFly](https://github.com/cantino/mcfly/) replaces your default ctrl-r shell history search with an intelligent search engine that takes into account your working directory and the context of recently executed commands. McFly's suggestions are prioritized in real time with a small neural network.
- [ranger](https://github.com/ranger/ranger) is a console file manager with VI key bindings. It provides a minimalistic and nice curses interface with a view on the directory hierarchy. It ships with `rifle`, a file launcher that is good at automatically finding out which program to use for what file type]
    - https://ranger.github.io/
- [jq](https://stedolan.github.io/jq/) is a lightweight and flexible command-line JSON processor
- [just](https://github.com/casey/just) is a handy way to save and run project-specific commands
- [Jump](https://github.com/gsamokovarov/jump) integrates with your shell and learns about your navigational habits by keeping track of the directories you visit. It gives you the most visited directory for the shortest search term you type.
- [direnv](https://github.com/direnv/direnv) is an extension for your shell. It augments existing shells with a new feature that can load and unload environment variables depending on the current directory.
- [tmux](https://github.com/tmux/tmux)
- [how2](https://github.com/santinic/how2) finds the simplest way to do something in a unix shell. It's like man, but you can query it in natural language

## Scripting

- [Funky](https://github.com/bbugyi200/funky) takes shell functions to the next level by making them easier to define, more flexible, and more interactive. 

## Monotoring

- [htop](https://htop.dev/)
- [glances](https://nicolargo.github.io/glances/) A top/htop alternative for GNU/Linux, BSD, Mac OS and Windows operating systems. 
    - https://github.com/nicolargo/glances
- vtop

## Editor/IDE

- nvim
- emacs

## Development

- [The Silver Searcher](https://github.com/ggreer/the_silver_searcher) A code searching tool similar to ack, with a focus on speed.

## REST

- [httpie](https://github.com/httpie/httpie) As easy as /aitch-tee-tee-pie/ pie Modern, user-friendly command-line HTTP client for the API era. JSON support, colors, sessions, downloads, plugins & more.
    - https://httpie.io/
- [tinytina-js](https://github.com/VonHeikemen/tinytina-js) Command-line http client. Is like the mix of curl and postman that nobody asked for. 
- [api-test](https://github.com/subeshb1/api-test) A simple bash script to test JSON API from terminal in a structured and organized way
- [Frank](https://github.com/txthinking/frank) is a REST API automated testing tool like Postman but in command line. Auto generate markdown API document
- [Restish](https://github.com/danielgtaylor/restish) is a CLI for interacting with REST-ish HTTP APIs with some nice features built-in, like always having the latest API resources, fields, and operations available when they go live on the API without needing to install or update anything.
    - https://rest.sh/#/

## Git

- [GitUpdate](https://github.com/nikitavoloboev/gitupdate) Commit and push updated files with file names as commit message 
- [Forgit](https://github.com/wfxr/forgit) This tool is designed to help you use git more efficiently. It's lightweight and easy to use
- [Tig](https://github.com/jonas/tig) is an ncurses-based text-mode interface for git. It functions mainly as a Git repository browser, but can also assist in staging changes for commit at chunk level and act as a pager for output from various Git commands.
    - https://jonas.github.io/tig/
- [hub](https://github.com/github/hub) is a command line tool that wraps git in order to extend it with extra features and commands that make working with GitHub easier.
    - https://hub.github.com/
- [lab](https://github.com/lighttiger2505/lab) is a cli client of gitlab like [hub](https://github.com/github/hub).
- [lazygit](https://github.com/jesseduffield/lazygit) A simple terminal UI for git commands, written in Go with the gocui library.

## Python

- [VirtualFish](https://github.com/justinmayer/virtualfish) Fish shell tool for managing Python virtual environments 
- [pipx](https://github.com/pypa/pipx) Install and Run Python Applications in Isolated Environments 

## Containers

- [ctop](https://github.com/bcicen/ctop) Top-like interface for container metrics
- [lazydocker](https://github.com/jesseduffield/lazydocker) The lazier way to manage everything docker

## Databases

- [LiteCLI](https://litecli.com/) A command line interface for SQLite with auto-completion and syntax highlighting.
- [pgcli](https://github.com/dbcli/pgcli) Postgres CLI with autocompletion and syntax highlighting 
- [Record Query](https://github.com/dflemstr/rq) a tool for doing record analysis and transformation 

## Documentation

- [tldr pages](https://tldr.sh/) Simplified and community-driven man pages
- [pandoc](https://pandoc.org/) to convert files from one markup format into another

## Network

- [ngrok](https://github.com/inconshreveable/ngrok) is a reverse proxy that creates a secure tunnel from a public endpoint to a locally running web service. ngrok captures and analyzes all traffic over the tunnel for later inspection and replay.

## Other

- [asciinema](https://asciinema.org/) is a free and open source solution for recording terminal sessions and sharing them on the web

