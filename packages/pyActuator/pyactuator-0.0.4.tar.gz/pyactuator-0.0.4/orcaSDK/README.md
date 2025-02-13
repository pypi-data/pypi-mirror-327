# orcaSDK

## Introduction
Welcome to the orcaSDK repo! The goal of the SDK is to help users who want to create custom software for controlling their Orca series linear motor. 

Not all use cases require custom software for controlling an Orca motor. It's possible that a tool already exists that handles your use case. Other options include:

- The Orca motor's built in GUI accessible through [IrisControls](https://irisdynamics.com/products/software).
- Our [MATLAB](https://irisdynamics.com/hubfs/Website/Downloads/Orca/Approved/UG230704_Orca_Series_Modbus_RTU_with_MATLAB.pdf) and [LabVIEW](https://irisdynamics.com/hubfs/Website/Downloads/Orca/Approved/UG230713_Orca_Series_Modbus_RTU_with_LabVIEW.pdf) packages
- One of our SmartHubs.

The benefits of using the SDK include:
- High speed serial communication with the motor
- Programmatic control over the motor using every operational mode available

If after considering your options custom software seems like the appropriate solution, then this repo is for you! The SDK is a C++ library designed to provide an easy to use and understand abstraction for your motor. The SDK also contains C++ implementations of a few commonly used tools. 

Currently, these tools are only available for applications running on Windows. 

## Prerequisites
To use the SDK you will need the following tools:

### Software
- [A Git client](https://git-scm.com/downloads). Our tutorials assume a command-line client.
- A C++ build system. For Windows your most appropriate option is likely MSBuild, which comes packaged with the IDE we recommend, [Microsoft Visual Studio](https://visualstudio.microsoft.com/).
- [CMake](https://cmake.org/) 
    
### Hardware
- An Orca series linear motor, and [any additional required components](https://irisdynamics.com/hubfs/Website/Downloads/Orca/Approved/UG220206_Orca_Series_Quickstart_Guide.pdf). A quick checklist of the dependencies includes:
    - An appropriate power supply
    - A cable splitter
    - An rs422 cable
    - An rs485 cable

### Knowledge
- Some basic programming knowledge, while not expressly required, will be very helpful. These tutorials will assume that you have written a (possibly very simple) program before. Experience with C++ is particularly useful.

## Setting Up Hardware and Testing Your Motor

Before continuing onto any software development, make sure that you have read through and followed the steps in the Orca Series Quickstart Guide, which can be found on [our downloads page](https://irisdynamics.com/downloads). We recommend testing your motors functionality through IrisControls, also hosted on our downloads page, before beginning to operate your motor through the SDK.

### Windows

Windows users will need to update a setting on their RS422 cable. Each cable has a built in latency of 16ms by default. For the RS485 cable, this is fine, but the SDK requires that this latency setting is reduced as much as possible. This allows for high speed communication with your motor. To update this setting, follow these steps:
 - Ensure your cables are connected to your computer
 - Open Device Manager
 - Navigate to "Ports (COM & LPT)" and expand the dropdown menu
 - Right click on the COM port for your RS422 cable and select "Properties"
    - If you do not know which COM port number corresponds to your RS422 cable, try unplugging and plugging back in your cable. The COM port you're looking for should disappear and reappear in the dropdown options
 - Under the "Port Settings" tab of the properties window, select "Advanced"
 - Set the "Latency Timer (msec)" option to a value of 1
 - Select Ok to confirm your selections

Keep a note of what the COM port number for your RS422 cable is. You will need it for each time you want to connect to your motor through the SDK.

## Clone the Repository

To set up this project, first clone this repo using whatever git client you have:

```
git clone git@github.com:IrisDynamics/orcaSDK.git
```
or
```
git clone https://github.com/IrisDynamics/orcaSDK.git
```

## Building the SDK

We recommend building the SDK using CMake. The SDK aims to support standard integration with CMake projects as a config-file package. To begin, open a command-line in the root directory of the cloned repository. Enter the following commands:

```
mkdir build
cd build
cmake ..
```

If everything works fine, the cmake command should identify a local C++ compiler and use it to configure a project, ready to be built. Now run the following command from inside the build directory

```
cmake --build .
```

If no errors are reported, the library will be built and is ready to be consumed by your application.

### (Optional) Install the SDK to your local system

If you'd like to install the SDK to your system to allow for easy reuse, you'll need to execute one additional command. First, open another command line, this time with administrator permissions. Then navigate once again to the build directory and execute the following command.

```
cmake --install .
```

## Building an Application using the SDK

The goal for this section is to illustrate how to create and compile a basic project that uses the orcaSDK. The goal is to get to the point of successful compilation, not for detailed use of the SDK. For tutorials and example projects with such use cases, we have created a separate repo, which we link to at the end of this README. Before going through those tutorials, however, we will assume you have followed the steps listed here for how to create a basic application.

### Create a CMakeLists.txt file

The basic unit of projects using CMake is the CMakeLists.txt file. To begin, create a file called CMakeLists.txt in the folder in which you'd like to create your application. Open the new file with a text editor of your choice and add the following text:

```CMakeLists.txt
cmake_minimum_required(VERSION 3.23)

project(basicOrcaSDKProj)
```

These two lines are required for any C++ project built using CMake. 

cmake_minimum_required() indicates the minimum CMake version that can be used to build the application. It also enables CMake features up to the version listed and changes some default behaviours. 

project() creates a CMake project and assigns it a name. For the purpose of building an application not meant to be shared, the details of this command isn't of much concern.

Now let's update the CMakeLists.txt file to add an application.

```CMakeLists.txt
...

add_executable(basicOrcaSDKApp
    main.cpp
)
```

This new command defines an application target which will result in an executable (.exe) when the project is built. Right now it depends on the source file main.cpp. We have not defined this file yet, and will save that until the next step.

Finally we add the commands which find and link the orcaSDK to the executable target.

```CMakeLists.txt
...

find_package(orcaSDK REQUIRED)
target_link_libraries(basicOrcaSDKApp PRIVATE orcaSDK::core)
```

find_package() searches CMake's known install paths for any package with a matching name. The REQUIRED parameter tells CMake to stop executing immediately if it failes to find the package. If you chose to build the SDK but not install it, this command must be modified to include the path to your build directory.

```
find_package(orcaSDK REQUIRED PATHS <path-to-your-orcaSDK-build-directory>)
```

target_link_libraries() indicates to CMake that the target listed as the first parameter is a client of the target described after. In this case, the basicOrcaSDKApp target is a client of the orcaSDK::core target. orcaSDK::core is the name of the core library of the SDK. The PRIVATE parameter indicates that the library is only meant to be consumed by the client target and to not propagate its settings further.

At this point we have the most simple CMakeLists.txt file describing an application which makes use of the SDK. At this point your CMakeLists.txt file should look something like this:

```CMakeLists.txt
cmake_minimum_required(VERSION 3.23)

project(basicOrcaSDKProj)

add_executable(basicOrcaSDKApp
    main.cpp
)

find_package(orcaSDK REQUIRED)
target_link_libraries(basicOrcaSDKApp PRIVATE orcaSDK::core)
```

Next let's create a very simple main.cpp which makes use of the SDK, and build it to test if our system is working.

```main.cpp
#include <iostream>
#include "actuator.h"

int main()
{
    orcaSDK::Actuator motor{ "MotorName" };
    std::cout << "Hello World\n";
    return 0;
}
```

For now don't worry about the contents of this source file.

## Compile and Run Your Application

Building the application can be done in a few ways. We recommend interacting with your project through Visual Studio. But you can also build your app using the command line.

### Visual Studio

To build a CMake app though Visual Studio follow these steps:
 - If using Visual Studio, open the app, and on the project selection window, select the option "Open a local folder". 
 - Select the folder that contains your CMakeLists.txt file. Visual Studio should recognize the project as a CMake project upon opening and configure itself appropriately. 
 - To interact with your project, right click on any item in the Solution Explorer, and select "Switch to CMake Targets View". 
 - To build your application. Expand the dropdown menu for your project and right click on your application. Either select "Set as Startup Item" then click the play button in the top, or select "Debug". Either will result in running your app.

### Command Line

If building your app through the command line, simply use the same commands as when building the library

```
mkdir build
cd build
cmake ..
cmake --build .
```

If the cmake commands complete without displaying error messages, then you're done! The resulting executable should be placed in either the Debug or Release directory generated in the build directory.

## What's Next?

Take a look at our [Tutorial Repo](https://github.com/IrisDynamics/orcaSDK_tutorials) for tutorials on how to handle some of the most common use cases for Orca motors.