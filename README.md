# ADAN

**Spanish**

Algoritmo de Descubrimiento Adaptativo basado en redes Neuronales

**English**

Adaptive Discovering Algorithm based on Neural networks

## Main goal

> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Tech

ADAN is built on top of:

* Python 3.6.4 - Compiled using GNU GCC 7.3.0

And of course ADAN itself is open source with a [public repository] on GitHub.

### Installation

**Important:** This section is still under construction...

### Development

Want to contribute? Great!

Open your favorite Terminal and run:

```sh
$ git clone https://github.com/EDario333/adan.git
```
#### Troubleshooting
Known issues are:
_fatal: Unable to find remote helper for 'https'_

Solution: 
If you built Git from source make sure that you've installed `libcurl4-openssl-dev` (on Debian systems) first. So, try:
`apt-get install libcurl4-openssl-dev`

And then re-install Git.

If the problem persist and you only want to try ADAN locally (highly probabadly you won't make any remote operation) you can:
`git clone git://github.com/EDario333/adan.git`

#### Building for source
_**To-Do**_

### Docker
**Important:** This section is still under construction...

ADAN is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8000, so change this within the Dockerfile if necessary. When ready, simply use the Dockerfile to build the image.

```sh
cd adan
docker build -t xyz/123:${package.json.version}
```
This will create the ADAN image and pull in the necessary dependencies. Be sure to swap out `${package.json.version}` with the actual version of ADAN.

Once done, run the Docker image and map the port to whatever you wish on your host. In this example, we simply map port 8000 of the host to port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart="always" <youruser>/123:${package.json.version}
```

Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8000
```
## Todos

A lot of things :)

In the priority order:
 - Keep with the ADAN's developing
 - Improve the [Tech section](#tech)
 - Finish the [Installation section](#installation)
 - Start to work with the [Building for source section](#building-for-source)
 - Improve the [Docker section](#docker)

License
----
[GNU General Public License v3.0]

## Authors
[PhD. Pilar Pozos-Parra](http://dblp.org/pers/p/Parra:Maria_del_Pilar_Pozos)

[MSc. Edgar Ramirez-deLeon](https://github.com/edario333)

## Colaborators
Anyone?

## Sponsors / Partially funded by
Anyone?

## Supported by
Anyone?

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[GNU General Public License v3.0]: https://www.gnu.org/licenses/gpl-3.0.en.html
[public repository]: https://github.com/EDario333/adan
