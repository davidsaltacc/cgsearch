# CGSearch 

A search engine with a bunch of QOL features for games from "non-steam" sources. I don't know how much I can say here without getting the repository removed, although im pretty sure the functionality alone will not, as all it does is act as a search engine, which doesn't actually host any files.

For a list of supported sites, please visit the search/engines/ folder. Sites that require javascript for their search to function, or ones that are protected by Cloudflare are currently not supported, as we only parse the static html data, although this may be subject to change in the future.

# Contributing

First you always have to clone the repository. Then, depending on what you want to do, you may or may not need to build the project from source. 

## Custom Engines

If you just want to add your own search engine, you can simply install CGSearch on your computer, go to the installation directory and modify the python files in the search/ subfolder. In there, they can be used for messing around without having to build from source - unless you want to do that, anyway. That is described in the next step. If you want to contribute these python files, and have modified them inside the CGSearch installation directory for easy testing, then all you need to do is copy them over to the cloned repository and open a pull request.

To make your own engine, simply look at how one of the existing one works. To know how exactly the results are supposed to be structured, take a look at the result template file in the search/ directory.

If you want to run some python scripts directly, without using the installed CGSearch, what you can do is run pre_build.ps1 in the cloned repository, which will install a small python runtime with all the dependencies, and to test you simply need to run `runtime/python.exe YOUR_FILE.py`. Alternatively, if you do have CGSearch installed and you want a python instance, you can also use the python runtime bundled with it, like `(installation directory)\bin\runtime\python.exe YOUR_FILE.py`.

## Further Contributions

If you want to make modifications to the UI or other parts that don't only touch the search engines, you will have to clone the repository as described in the previous step. A few things are required for that: 1. A Visual Studio 2022 installation with Avalonia support, NSIS installed and in PATH, and have a Folder Publishing Profile set up - that puts the files in `ui\bin\Release\net8.0\win-x64\publish\`. The installer maker will look for the exe and dlls there, but you can also change the properties.txt file to include whatever path it is in for you.

For simple UI testing builds, you may use VS's "Release"/"Debug" builds - BUT, this is IMPORTANT: When in need of a fully usable version, with a functioning search, do not use builds produced by VS's "Release" build - specifically use the publishing profile, it will use the Release, but will also do other neccessary things.

Building with VS as described will automatically download and install the python embeddable runtime and make the installer for you - all you need to worry about is publishing with the folder profile in VS and then running the installer that should have been created.