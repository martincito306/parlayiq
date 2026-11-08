import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PARLAYIQ — Plataforma de Inteligencia Deportiva y Optimización Cuantitativa",
  description: "Análisis estadístico profesional de fútbol, Poisson Dixon-Coles, Player Props, Same Game Parlay Monte Carlo y Auditoría Histórica.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" className="dark">
      <body className="min-h-screen bg-[#080B12] text-[#F8FAFC] antialiased selection:bg-emerald-500 selection:text-black">
        {children}
      </body>
    </html>
  );
}
