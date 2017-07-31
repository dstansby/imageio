""" 
Console scripts and associated helper methods for imageio.
"""
from __future__ import print_function

import argparse
import os
from os import path as op
import shutil


from . import plugins
from .core import util

# A list of plugins that require binaries from the imageio-binaries
# repository. These plugins must implement the `download` method.
PLUGINS_WITH_BINARIES = ["avbin", "ffmpeg", "freeimage"]


def download_bin(plugin_names=["all"], package_dir=False):
    """ Download binary dependencies of plugins
    
    This is a convenience method for downloading the binaries
    (e.g. `ffmpeg.win32.exe` for Windows) from the imageio-binaries
    repository.
    
    Parameters
    ----------
    plugin_names: list
        A list of imageio plugin names. If it contains "all", all
        binary dependencies are downloaded.
    package_dir: bool
        If set to `True`, the binaries will be downloaded to the
        `resources` directory of the imageio package instead of
        to the users application data directory. Note that this
        might require administrative rights if imageio is installed
        in a system directory.
    """
    if plugin_names.count("all"):
        # Use all plugins
        plugin_names = PLUGINS_WITH_BINARIES
    
    plugin_names.sort()
    print("Ascertaining binaries for: {}.".format(", ".join(plugin_names)))
    
    if package_dir:
        # Download the binaries to the `resources` directory
        # of imageio. If imageio comes as an .egg, then a cache
        # directory will be created by pkg_resources (requires setuptools).
        # see `imageio.core.util.resource_dirs`
        # and `imageio.core.utilresource_package_dir`
        directory = util.resource_package_dir()
    else:
        directory = None
    
    for plg in plugin_names:
        msg = "Plugin {} is not registered for binary download!".format(plg)
        assert plg in PLUGINS_WITH_BINARIES, msg
        mod = getattr(plugins, plg)
        mod.download(directory=directory)


def download_bin_main():
    """ Argument-parsing wrapper for `download_bin` """
    description = "Download plugin binary dependencies"
    phelp = "Plugin name for which to download the binary. "\
            + "If no argument is given, all binaries are downloaded."
    dhelp = "Download the binaries to the package directory "\
            + "(default is the users application data directory). "\
            + "This might require administrative rights."
    example_text = "examples:\n"\
                   + "  imageio_download_bin all\n"\
                   + "  imageio_download_bin ffmpeg\n"\
                   + "  imageio_download_bin avbin ffmpeg\n"
    parser = argparse.ArgumentParser(
        description=description,
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("plugin", type=str, nargs="*", default="all",
                        help=phelp)
    parser.add_argument("--package-dir", dest="package_dir",
                        action="store_true", default=False, help=dhelp)
    args = parser.parse_args()
    download_bin(plugin_names=args.plugin, package_dir=args.package_dir)


def remove_bin(plugin_names=["all"]):
    """ Remove binary dependencies of plugins
    
    This is a convenience method that removes all binaries
    dependencies for plugins downloaded by imageio.
    
    Notes
    -----
    It only makes sense to use this method if the binaries
    are corrupt.
    """
    if plugin_names.count("all"):
        # Use all plugins
        plugin_names = PLUGINS_WITH_BINARIES

    print("Removing binaries for: {}.".format(", ".join(plugin_names)))

    rdirs = util.resource_dirs()

    for plg in plugin_names:
        msg = "Plugin {} is not registered for binary download!".format(plg)
        assert plg in PLUGINS_WITH_BINARIES, msg
    
    for rd in rdirs:
        # plugin name is in subdirectories
        for rsub in os.listdir(rd):
            if rsub in plugin_names:
                shutil.rmtree(op.join(rd, rsub))


def remove_bin_main():
    """ Argument-parsing wrapper for `remove_bin` """
    description = "Remove plugin binary dependencies"
    phelp = "Plugin name for which to remove the binary. "\
            + "If no argument is given, all binaries are removed."
    example_text = "examples:\n"\
                   + "  imageio_remove_bin all\n"\
                   + "  imageio_remove_bin ffmpeg\n"\
                   + "  imageio_remove_bin avbin ffmpeg\n"
    parser = argparse.ArgumentParser(
        description=description,
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("plugin", type=str, nargs="*", default="all",
                        help=phelp)
    args = parser.parse_args()
    remove_bin(plugin_names=args.plugin)


if __name__ == "__main__":
    download_bin_main()
