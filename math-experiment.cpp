#include <iostream>
#include <cmath>
#include <functional>

// Define the scalar function f(x, y, z)
double f(double x, double y, double z) {
    return x * x + y * y + z * z + x * y * z;
}

// Compute partial derivative with respect to x using central difference
double partial_x(std::function<double(double, double, double)> func,
                 double x, double y, double z, double h = 1e-6) {
    return (func(x + h, y, z) - func(x - h, y, z)) / (2.0 * h);
}

// Compute partial derivative with respect to y using central difference
double partial_y(std::function<double(double, double, double)> func,
                 double x, double y, double z, double h = 1e-6) {
    return (func(x, y + h, z) - func(x, y - h, z)) / (2.0 * h);
}

// Compute partial derivative with respect to z using central difference
double partial_z(std::function<double(double, double, double)> func,
                 double x, double y, double z, double h = 1e-6) {
    return (func(x, y, z + h) - func(x, y, z - h)) / (2.0 * h);
}

int main() {
    double x, y, z;
    std::cout << "Enter point (x y z): ";
    std::cin >> x >> y >> z;

    double df_dx = partial_x(f, x, y, z);
    double df_dy = partial_y(f, x, y, z);
    double df_dz = partial_z(f, x, y, z);

    std::cout << "\nPartial derivatives at (" << x << ", " << y << ", " << z << "):\n";
    std::cout << "df/dx = " << df_dx << "\n";
    std::cout << "df/dy = " << df_dy << "\n";
    std::cout << "df/dz = " << df_dz << "\n";

    return 0;
}