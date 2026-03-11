cmake_minimum_required(VERSION 3.10)
project(pinocchio_examples_cpp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find required packages
find_package(pinocchio REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(urdfdom REQUIRED)
find_package(hpp-fcl REQUIRED)

# Include directories
include_directories(
  ${PINOCCHIO_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ${URDFDOM_INCLUDE_DIRS}
  ${HPP_FCL_INCLUDE_DIRS}
)

# Build output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Function to add an example
function(add_pinocchio_example example_name example_source)
  add_executable(${example_name} ${example_source})
  target_link_libraries(${example_name}
    ${PINOCCHIO_LIBRARIES}
    ${EIGEN3_LIBRARIES}
    ${URDFDOM_LIBRARIES}
    ${HPP_FCL_LIBRARIES}
  )
  install(TARGETS ${example_name} DESTINATION bin)
endfunction()

# Kinematics examples
add_pinocchio_example(overview-simple kinematics/overview-simple.cpp)
add_pinocchio_example(overview-urdf kinematics/overview-urdf.cpp)
add_pinocchio_example(overview-SE3 kinematics/overview-SE3.cpp)
add_pinocchio_example(overview-lie kinematics/overview-lie.cpp)
add_pinocchio_example(kinematics-derivatives kinematics/kinematics-derivatives.cpp)
add_pinocchio_example(build-reduced-model kinematics/build-reduced-model.cpp)

# Dynamics examples
add_pinocchio_example(inverse-dynamics dynamics/inverse-dynamics.cpp)
add_pinocchio_example(forward-dynamics-derivatives dynamics/forward-dynamics-derivatives.cpp)
add_pinocchio_example(inverse-dynamics-derivatives dynamics/inverse-dynamics-derivatives.cpp)
add_pinocchio_example(contact-dynamics dynamics/contact-dynamics.cpp)

# Collision examples
add_pinocchio_example(collisions collision/collisions.cpp)
add_pinocchio_example(geometry-models collision/geometry-models.cpp)

# Autodiff examples
add_pinocchio_example(cppad-basic autodiff/cppad-basic.cpp)
add_pinocchio_example(cppad-kinematics autodiff/cppad-kinematics.cpp)

# Other examples
add_pinocchio_example(interpolation-SE3 other/interpolation-SE3.cpp)
add_pinocchio_example(multiprecision other/multiprecision.cpp)

message(STATUS "Pinocchio C++ examples configured successfully!")
message(STATUS "Build directory: ${CMAKE_BINARY_DIR}")
