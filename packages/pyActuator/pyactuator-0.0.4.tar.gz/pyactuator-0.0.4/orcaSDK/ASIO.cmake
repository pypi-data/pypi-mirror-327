if(POLICY CMP0135)
  cmake_policy(SET CMP0135 NEW)
endif()

include(ExternalProject)
ExternalProject_Add(
	asio-repo
	URL https://github.com/chriskohlhoff/asio/archive/refs/tags/asio-1-32-0.zip	
	SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/dependencies
	CONFIGURE_COMMAND ""
	BUILD_COMMAND ""
	INSTALL_COMMAND ""
)

add_library(asio INTERFACE)
add_dependencies(asio asio-repo)
target_include_directories(asio INTERFACE dependencies/asio/include)

export(TARGETS asio
	NAMESPACE asio::
	FILE "${CMAKE_CURRENT_BINARY_DIR}/asioConfig.cmake"
)