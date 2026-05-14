#include <cmath>
#include <iostream>

double approximate_distance(double left, double right) {
    return std::abs(left - right);
}

int main() {
    std::cout << approximate_distance(0.42, 0.17) << std::endl;
    return 0;
}

