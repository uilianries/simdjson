#include <iostream>

#ifdef SIMDJSON_HEADER_ONLY
#   include "simdjson/simdjson.h"
#   include "simdjson/simdjson.cpp"
#else
#   include "simdjson/jsonparser.h"
#endif

int main() {
  std::string_view p = get_corpus("conanbuildinfo.json");
  ParsedJson pj = build_parsed_json(p);
  if( ! pj.isValid() ) {
    std::cout << "not valid" << std::endl;
  } else {
    std::cout << "valid" << std::endl;
  }
  return EXIT_SUCCESS;
}