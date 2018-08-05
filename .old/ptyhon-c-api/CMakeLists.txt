# Based on an example CMakeLists.txt from http://dlib.net/examples/CMakeLists.txt.html
# You can download CMake from http://www.cmake.org

cmake_minimum_required(VERSION 2.8.12)
# Name of the project:
project(peanuts)

# Tell cmake we will need dlib
# IMPORTANT: point the first parameter to an installation of dlib
# You can download it here -> https://github.com/davisking/dlib
add_subdirectory(C:/Users/aleks_000/Desktop/BWSI/CogWorks_2018/dependencies/dlib/dlib dlib_build)

# Tell CMake about the code we want to compile
add_executable(chipmodule chipmodule.cpp)

# Tell CMake that this program, chipmodule, depends on dlib
target_link_libraries(chipmodule dlib::dlib)

# Ask cmake to compile the code:
#
#   cd upgraded-octo-discocito-8
#   mkdir build
#   cd build
#   cmake ..
#   cmake --build . --config Release
#
# If using Visual Studio, call:
#
#   cmake -G "Visual Studio 14 2015 Win64" -T host=x64 ..
#
# Instead of
#
#   cmake ..
#
# You would be able to open the resulting Xcode project