#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>

class Particle {
public:
    double x, y, z;
    double vx, vy, vz;
    double q; // Carga de la partícula en Coulombs
    double m; // Masa de la partícula en kg
    
    Particle(double x0, double y0, double z0, double vx0, double vy0, double vz0, double charge, double mass)
        : x(x0), y(y0), z(z0), vx(vx0), vy(vy0), vz(vz0), q(charge), m(mass) {}
};

class MagneticField {
public:
    double Bx, By, Bz;
    
    MagneticField(double Bx0, double By0, double Bz0)
        : Bx(Bx0), By(By0), Bz(Bz0) {}
};

// Función para definir el campo magnético variable en el tiempo
MagneticField B(double t) {
    double B0 = 1.0; // Amplitud del campo magnético en Tesla
    double omega = 1e10; // Frecuencia angular en rad/s
    return MagneticField(B0 * cos(omega * t), B0 * cos(omega * t), B0 * cos(omega * t));
}

void updatePosition(Particle& p, const MagneticField& B, double dt) {
    // Fuerza de Lorentz
    double Fx = p.q * (p.vy * B.Bz - p.vz * B.By);
    double Fy = p.q * (p.vz * B.Bx - p.vx * B.Bz);
    double Fz = p.q * (p.vx * B.By - p.vy * B.Bx);
    
    // Actualizamos velocidad (m/s)
    p.vx += (Fx / p.m) * dt;
    p.vy += (Fy / p.m) * dt;
    p.vz += (Fz / p.m) * dt;
    
    // Actualizamos posición (m)
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.z += p.vz * dt;
}

int main() {
    // Creamos una partícula genérica (por ejemplo, un electrón)
    double charge = -1.60217662e-19; // Carga de la partícula en Coulombs (electrób)
    double mass = 9.10938356e-31;    // Masa de la partícula en kg (electrón)
    Particle particle(0, 0, 0, 1e6, 1e6, 1e6, charge, mass); // Velocidad inicial en m/s (ajustada)
    
    double dt = 1e-12; // Paso de tiempo en segundos (ajustado)
    int steps = 1000;  // Número de pasos de simulación
    
    // Abrir archivo para guardar datos de trayectoria
    std::ofstream outputFile("trajectory.csv");
    outputFile << "x,y,z,vx,vy,vz,Bx,By,Bz\n"; // Encabezado del archivo CSV
    
    for (int i = 0; i < steps; ++i) {
        double t = i * dt; // Obtenemos el tiempo actual
        MagneticField field = B(t); // Campo magnético variable en el tiempo
        
        // Actualizamos posición y velocidad de la partícula
        updatePosition(particle, field, dt);
        outputFile << particle.x << "," << particle.y << "," << particle.z << ","
                   << particle.vx << "," << particle.vy << "," << particle.vz << ","
                   << field.Bx << "," << field.By << "," << field.Bz << "\n";
        
        // Mostramos estado de la trayectoria cada 100 pasos
        if (i % 100 == 0) {
            std::cout << "Paso " << i << ": (" << particle.x << ", " << particle.y << ", " << particle.z << ")\n";
        }
    }
    
    // Cerramos archivo
    outputFile.close();
    std::cout << "Trayectoria guardada en 'trajectory.csv'\n";
    
    return 0;
}


// COMPILACION: g++ -std=c++11 trajectory.cpp -o trajectory




