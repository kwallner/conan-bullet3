from conans import CMake, ConanFile, tools
import os
import shutil
import platform


class Bullet3Conan(ConanFile):
    name = "bullet3"
    version = "2.87"
    _md5 = "7566fc00d925a742e6f7ec7ba2d352de"
    description = "Bullet Physics SDK: real-time collision detection and multi-physics simulation for VR, games, visual effects, robotics, machine learning etc."
    url = "https://github.com/kwallner/conan-bullet3"
    homepage = "https://github.com/bulletphysics/bullet3"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "ZLIB"
    exports = ["LICENSE.txt"]
    exports_sources = ["CMakeLists.txt", "%s.tar.gz" % version]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    settings = "os", "arch", "compiler", "build_type"
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
    no_copy_source = True

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        if os.path.isfile("%s.tar.gz" % self.version):
            tools.unzip("%s.tar.gz" % self.version)
        else:
            tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), self._md5)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def requirements(self):
        #if self.options.pybullet:
        #    self.requires.add("cpython/3.6.4@bincrafters/stable")
        pass

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_BULLET3"] = self.options.build_bullet3
        if platform.system() == "Windows":
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True
        cmake.definitions["INSTALL_LIBS"] = True
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["USE_GRAPHICAL_BENCHMARK"] = self.options.graphical_benchmark
        cmake.definitions["USE_DOUBLE_PRECISION"] = self.options.double_precision
        cmake.definitions["BULLET2_USE_THREAD_LOCKS"] = self.options.bt2_thread_locks
        cmake.definitions["USE_SOFT_BODY_MULTI_BODY_DYNAMICS_WORLD"] = self.options.btSoftMultiBodyDynamicsWorld
        cmake.definitions["BUILD_PYBULLET"] = self.options.pybullet
        if self.options.pybullet:
            cmake.definitions["BUILD_PYBULLET_NUMPY"] = self.options.pybullet_numpy
        cmake.definitions["BUILD_ENET"] = self.options.network_support
        cmake.definitions["BUILD_CLSOCKET"] = self.options.network_support
        cmake.definitions["BUILD_CPU_DEMOS"] = False
        cmake.definitions["BUILD_OPENGL3_DEMOS"] = False
        cmake.definitions["BUILD_BULLET2_DEMOS"] = False
        cmake.definitions["BUILD_EXTRAS"] = False
        cmake.definitions["BUILD_UNIT_TESTS"] = False
        cmake.definitions["CMAKE_DEBUG_POSTFIX"] = ""
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["USE_MSVC_RUNTIME_LIBRARY_DLL"] = "MD" in self.settings.compiler.runtime
        cmake.configure()
        cmake.build()
        cmake.install()
        # Remove unused cmake stuff
        shutil.rmtree(os.path.join(self.package_folder, "lib", "cmake"))

    def package(self):
        self.copy("LICENSE.txt", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        libs = []
        if self.options.build_bullet3:
            libs += [
                "Bullet2FileLoader",
                "Bullet3Collision",
                "Bullet3Dynamics",
                "Bullet3Geometry",
                "Bullet3OpenCL_clew",
            ]
        libs += [
            "BulletDynamics",
            "BulletCollision",
            "LinearMath",
            "BulletSoftBody",
            "Bullet3Common",
            "BulletInverseDynamics",
        ]

        self.cpp_info.includedirs = ["include/bullet"]
        self.cpp_info.libs = libs

        self.env_info.BULLET_ROOT = self.package_folder
