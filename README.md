# canvas2canvas

KLayout Python module as a websockets client

NOTE: this is a demonstrator. It shows the basic idea, but lacks fancy styling and 
many potential features. It does not use any JavaScript libraries and only plain
CSS.

## Getting the KLayout Python module

You will need a KLayout Python module with Qt-less canvas enabled.

To build the module yourself, clone KLayout from

```
$ git clone git@github.com:KLayout/klayout.git
```

You will need Linux and the following libraries: curl, zlib, png, expat
and python3.

In the klayout sources, run

```
$ python3 setup.py build
```

Once the respective version (0.28) is available in PyPI, you can simply do

```
pip3 install klayout
```

## Usage

Clone this repository somewhere else:

```
git clone git@github.com:klayoutmatthias/canvas2canvas.git canvas2canvas
```

In this project, start the server:

```
./server.py
```

You may need to point "PYTHONPATH" to the directory where you built the
Python module. In my case this is:

```
export PYTHONPATH=/home/matthias/klayout/master/build/lib.linux-x86_64-3.8
```

In a different window, start a browser (tested with Firefox) 
and load "client.html" from this project, e.g. "firefox client.html".


