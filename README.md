# CGSearch 

A search engine with a bunch of QOL features for games from "non-steam" sources. I don't know how much I can say here without getting the repository removed, although im pretty sure the functionality alone will not, as all it does is act as a search engine, which doesn't actually host any files.

For a list of supported sites, please visit the search/engines/ folder. Sites that require javascript for their search to function, or ones that are protected by Cloudflare are currently not supported, as we only parse the static html data, although this may be subject to change in the future.

## Disclaimer

We do not host any files ourselves. We don't provide any illegaly uploaded files, we only provide an engine to simplify the use of sites providing those files. We don't host the files nor the sites - and we do not encourage piracy.

# Contributing

First you always have to clone the repository. Then, depending on what you want to do, you may or may not need to build the project from source. 

## Custom Engines

If you just want to add your own search engine, you can simply install CGSearch on your computer, go to the installation directory and modify the python files in the search/ subfolder. In there, they can be used for messing around without having to build from source - unless you want to do that, anyway. That is described in the next step. If you want to contribute these python files, and have modified them inside the CGSearch installation directory for easy testing, then all you need to do is copy them over to the cloned repository and open a pull request.

To make your own engine, simply look at how one of the existing one works. The main important part is that it defines the `generator` and `engine_meta` fields, and the structure of the results it yields.

If you want to run some python scripts directly, without using the installed CGSearch, what you can do is run `post_build.ps1 onlyRuntime` in the cloned repository, which will install a small python runtime with all the dependencies, and to test you simply need to run `runtime/python.exe YOUR_FILE.py`. Alternatively, if you do have CGSearch installed and you want a python instance, you can also use the python runtime bundled with it, like `(installation directory)\bin\runtime\python.exe YOUR_FILE.py`.

For Debugging your engine - you will have to add it to the list of all engines in main.py, and to be able to debug easily without launching the whole application, you can launch `path\to\python.exe main.py Debug` - because when launching it with the `Debug` flag, it will just ask you for a search query, and the engine to give the search query to. You don't need to enter the full engine ID - a part of it works too, as long as its unique from others. This will just use that specific engine to look for the query and print out the results.

## Further Contributions

If you want to make modifications to the UI or other parts that don't only touch the search engines, you will have to clone the repository as described in the previous step. A few things are required for that: 1. A Visual Studio 2022 installation with Avalonia support, NSIS installed and in PATH, Optionally ImageMagick and in PATH (only used for creating a better quality .ico file, but is not needed), and have a Folder Publishing Profile set up - standard release builds are not enough if you want an installer and a distributable version to be generated.

For simple UI testing builds, you may use VS's "Release"/"Debug" builds - but, as mentioned above, when in need of a fully distributable version, do not use builds produced by VS's "Release" build - specifically use the publishing profile.

Building with VS using the standard Debug/Release builds will download the python runtime if not present and copy over all the python files, so the search works. Again, this does NOT mean, you should just pop the outputted file into a zip and ship it production-ready. 