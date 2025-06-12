#include <algorithm>
#include <cassert>
#include <fstream>
#include <functional>
#include <iostream>

#include "domino_cube.hpp"
#include "generator.hpp"
#include "state_count.hpp"

constexpr unsigned table_size = DominoCube::N_ESL * DominoCube::N_CO;
std::array<DomiNode, table_size> table;

auto unassigned = DomiNode{};
auto filler = std::function<DomiNode(DomiNode&)>([](DomiNode &node) -> DomiNode { return node; });

int main() {

  table.fill(unassigned);

  // This function fills the table with the entire EO case data
  generator<DomiNode>(table, filler, unassigned, EOFB_HTM_Moves);

  DominoCube cube;
  for (unsigned k = 0; k < table.size(); ++k) {
    auto &dr_case = table[k];
    // Making sure everything looks normal
    cube.set_solved();
    cube.apply(dr_case.path);
    assert(dr_case.state == cube);
  }

  {
    // Write data to file
    std::ofstream solution_file("full_data.csv");
    for (auto node : table) {
      assert(node != unassigned);
      solution_file << dr_coord(node.state) << ",";
      for (Cubie c = ULF; c <= DLB; ++c) {
        solution_file << static_cast<unsigned>(node.state.co[c]);
      }
      solution_file << ",";
      for (Cubie e = UF; e <= DL; ++e) {
        solution_file << static_cast<unsigned>(node.state.esl[e]);
      }
      solution_file << "," << node.depth << "," << node.path << "\n";
    }
  }
}
