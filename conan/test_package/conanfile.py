#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "json"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["SIMDJSON_HEADER_ONLY"] = self.options["simdjson"].header_only
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["CONAN_CXX_FLAGS"] = "/arch:AVX2"
        else:
            cmake.definitions["CONAN_CXX_FLAGS"] = "-mavx2 -mbmi -mbmi2 -mpclmul"
        cmake.configure()
        cmake.build()

    def test(self):
        bin_path = os.path.join("bin", "test_package")
        self.run(bin_path, run_environment=True)
