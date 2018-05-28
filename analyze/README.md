# Encryption analysis tool
## Environment Requirement
* python3

## Package requirement
* numpy
* matplotlib 
* PIL (Python Image Library)   <br />
Use `pip3 install numpy matplotlib Pillow` to install relative package.
In Windows cmd, use `pip install numpy matplotlib Pillow` to install package.
If you use `Anaconda3` as your running environment, you don't need additional package instalation.

## Analyze image requirement
* Plain image
* cipher image
* cipher image relative to one pixel changed plain image   <br />
You can use `diff_plain.py` to generate one pixel changed plain image.

## How to use
* Linux/MacOS system:
`python3 analyze.py [-h] [-p] [-d] [-c] [-e] [-a]`

* Windows system (Use cmd):
`python analyze.py [-h] [-p] [-d] [-c] [-e] [-a]`

* Windows system (Use Anaconda3 Spyder Editor)
Press`F6`, Find `General Settings > Command line options` to set command line arguments.

* Ex1.
If you want to draw histogram for specific image, type:
`python analyze.py -p`
Then it will ask you specify your image's path, type:
`lena.bmp`

* Ex2.
If you want to do all kinds of analyze, type:
`python analyze.py -a`
Then it will ask you specify some require image's path.

* Help
If you want to know every parameter's function, type:
`python analyze.py -h`

## Reference analysis method
* [Use argv in anaconda](https://groups.google.com/forum/#!topic/spyderlib/znVNGIKYChI)
* A chaotic image encryption scheme owning temp-value feedback. Leo Yu Zhang a, Xiaobo Hu