# copypastor

Copy & paste your stuff between devices, simple and fast way. Safely share your clipboard.

![img](https://download.rz1.pl/copypastor/copypastor-diag.png)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine. 

*tldr:* go to [Installing](#installing) & [HOW MAY I USE IT?](#how-may-i-use-it)  

### Prerequisites

You need at least **Python3** - that's all. Rest is in `requirements.txt` (installed automatically).

Oh, one more thing: ***nix** systems only (including MacOS), I don't work with Windows so... maybe you could add it?

And one more - your devices have to be in the **same network**.

### Installing

- `pip3 install copypastor` (recommended)


- clone code & `pip3 install .` (in app root directory)
- clone code & `python3 setup.py install` (little deprecated)

### Configuration

Default config after installation is your $HOME location, usually:
`/home/yourmom/.config/copypastor/config.py`

This is standard *python* config, you can change there things like:
```
- SERVER_PORT
- SERVER_HOST
- REMOTE_PORT
- REMOTE_HOST
- AUTH_KEY (currently not ciphered)
```
and also key bindings:
```
- ACTIVATE_CLIENT -> KeyCode(char='c') -> to some other [key combination is allowed]
- ACTIVATE_SERVER -> KeyCode(char='s') -> to some other [key combination is allowed]
```
## Deployment (CLI usage)

copypastor is *cli-app-only*, dead simple. After installing just try commands below. 

One important thing to remember: **you need to start it where your X's are** *(or `EXPORT DISPLAY` them)* 

- `copypastor` - running default mode, you can choose between client/server mode by (default) keys **'C'** or **'S'**  
- `copypastor --server` - server mode only, listening on port and waiting for connection
- `copypastor --client` - client mode only, connecting to specified host (*$HOME/.config/copypastor/config.py*)
- `copypastor --debug` - just like default but with more CLI info
- `copypastor --help` - not important at all ;)
- `copypastor --version` - in case I would ever bump it up


## HOW MAY I USE IT? 
#### (how author is using it)

On 1st device (let's say *a Ubuntu laptop*) I'm starting in CLI:

**copypastor --server** to run server-mode

![screenshot](https://download.rz1.pl/copypastor/copypastor-server.png)

- Now copy some text on this Ubuntu to system clipboard (CTRL+C somewhere: `"has logged off"`)

On the other one (let's say *a Macbook*) I'm starting in CLI:

**copypastor --client** to run client-mode, **then paste from clipboard** and... *voilà*. <br>I've just pasted this text from *Ubuntu clipboard*.

![screenshot](https://download.rz1.pl/copypastor/copypastor-client.png)

### [extra stuff]
OR (even better, extremely ergonomic):

- Create system/app key shortcut bind **so you can paste it fast anywhere**, for ex. [iCanHazShortcut](https://github.com/deseven/iCanHazShortcut)

![screenshot](https://download.rz1.pl/copypastor/haz-copypastor.png)


## TODO:
1. **DotEnv** instead standard *config.py*
2. **Threads** for app modes (so you could easy change it while running)
3. **Pathlib** for in-place paths instead current import construction
4. Securing secrets (connection token)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/venomen/copypastor/tags). 

## Authors

* **Dawid Deręgowski** - *currently the only one* - [Venomen](https://github.com/venomen)

See also the list of [contributors](https://github.com/venomen/copypastor/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details