cmake_minimum_required(VERSION 3.16)

project(DwarfController VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt specific settings
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# Find Qt6
find_package(Qt6 REQUIRED COMPONENTS Widgets Network Multimedia)

# Find Protobuf
find_package(Protobuf REQUIRED)

# Protobuf generation
file(GLOB PROTO_FILES "src/proto/*.proto")
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_FILES})

# Include directories
include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(src)

# Source files
set(SOURCES
    src/main.cpp
    src/MainWindow.cpp
    src/MainWindow.h
    ${PROTO_SRCS}
    ${PROTO_HDRS}
)

# Executable
add_executable(DwarfController ${SOURCES})

# Link libraries
target_link_libraries(DwarfController PRIVATE
    Qt6::Widgets
    Qt6::Network
    Qt6::Multimedia
    ${Protobuf_LIBRARIES}
)

# Qt specific settings
set_target_properties(DwarfController PROPERTIES
    WIN32_EXECUTABLE ON
    MACOSX_BUNDLE ON
)
