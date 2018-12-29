#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_bullet3": [True, False],
        "graphical_benchmark": [True, False],
        "double_precision": [True, False],
        "bt2_thread_locks": [True, False],
        "btSoftMultiBodyDynamicsWorld": [True, False],
        "pybullet": [True, False],
        "pybullet_numpy": [True, False],
        "network_support": [True, False],
    }
    default_options = {
        "shared" : False,
        "fPIC" : True,
        "build_bullet3" : False,
        "graphical_benchmark" : False,
        "double_precision" : False,
        "bt2_thread_locks" : False,
        "btSoftMultiBodyDynamicsWorld" : False,
        "pybullet" : False,
        "pybullet_numpy" : False,
        "network_support" : False,
    }
    
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            bin_path = os.path.join("bin", "test_package")
            if self.settings.os == "Windows":
                self.run(bin_path)
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_path))
            else:
                self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_path))
