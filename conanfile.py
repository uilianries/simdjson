#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration


class SimdjsonConan(ConanFile):
    name = "simdjson"
    description = "Parsing gigabytes of JSON per second"
    topics = ("conan", "simdjson", "json", "json-parser")
    url = "https://github.com/lemire/simdjson"
    homepage = url
    author = "Daniel Lemire <lemire@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE"]
    exports_sources = ["*"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "header_only": [True, False]}
    default_options = {"shared": False, "fPIC": True, "header_only": False}
    _build_subfolder = "build_subsfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        if self.options.header_only:
            self.settings.clear()
            del self.options.shared
            del self.options.fPIC
        else:
            compiler_version = Version(self.settings.compiler.version.value)
            if (self.settings.compiler == "gcc" and compiler_version < "7.0") or \
                (self.settings.compiler == "clang" and compiler_version < "4.0") or \
                (self.settings.compiler == "Visual Studio" and compiler_version < "15") or \
                (self.settings.compiler == "apple-clang" and compiler_version < "9.0"):
                raise ConanInvalidConfiguration("simdjson requires C++17")
            elif (self.settings.os != "Windows" and self.settings.arch == "x86"):
                raise ConanInvalidConfiguration("simdjson does not support 32-bits")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["SIMDJSON_BUILD_STATIC"] = not self.options.shared
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        tools.replace_in_file("CMakeLists.txt", "project(simdjson)", """project(simdjson)
        include(conanbuildinfo.cmake)
        conan_basic_setup()""")
        if not self.options.header_only:
            cmake = self._configure_cmake()
            cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses")
        if self.options.header_only:
            dst_folder = os.path.join("include", "simdjson")
            self.copy(pattern="simdjson.cpp", dst=dst_folder, src="singleheader")
            self.copy(pattern="simdjson.h", dst=dst_folder, src="singleheader")
        else:
            cmake = self._configure_cmake()
            cmake.install()

    def package_id(self):
        if self.options.header_only:
            self.info.header_only()

    def package_info(self):
        if not self.options.header_only:
            self.cpp_info.libs = tools.collect_libs(self)
            if self.settings.os == "Linux":
                self.cpp_info.libs.append("m")
